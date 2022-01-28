import os, time, shutil
import ursina
import pyboy
from PIL import Image
from panda3d.core import InputDevice, Texture as PandaTexture
from modules.constants import *
from modules.irc_parser import handle_input
from collections import deque

if os.path.isfile("secrets.py"):
	from modules.twitch_integrator import TwitchIntegrator

os.makedirs("saves", exist_ok=True)
ursina.Text.default_font = "assets/OpenSans-Bold.ttf"

BACKUP_TIME = 5*60
MESSAGE_TIMEOUT = 99999999 #Meh, looks too empty with slow chat
MAX_MESSAGES = 15
MAX_COMMANDS = 10
PRESS_DURATION = 0.1
DISABLE_IRC = False


class ScreenMessage:
	def __init__(self, message, received_time):
		self.message, self.received_time = message, received_time

class Controller(ursina.Entity):
	def __init__(self, gameboy, *args, **kwargs):
		self.gameboy = gameboy
		scale = kwargs.pop('scale')
		ursina.Entity.__init__(self, *args, parent=ursina.camera.ui, scale=(scale*0.975,0.45), model=ursina.Quad(radius=0.1), position=kwargs.pop('position')+ ursina.Vec2(0.0125,-0.0125), color=ursina.color.black66, **kwargs)	
		d_pad_center = self.position + (0.275*scale, -0.34*scale)
		button_pad_center = self.position + (0.725*scale,-0.34*scale)
		start_select_center = self.position + (0.5*scale, -0.24*scale)
		self.up_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0,0.07*scale,0), texture="assets/d_pad.png",rotation_z=90,model="quad",scale=0.05,z=-5)
		self.down_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0,-0.07*scale,0), texture="assets/d_pad.png",rotation_z=270,model="quad",scale=0.05,z=-5)
		self.left_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(-0.07*scale,0,0), texture="assets/d_pad.png",rotation_z=0,model="quad",scale=0.05,z=-5)
		self.right_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0.07*scale,0,0), texture="assets/d_pad.png",rotation_z=180,model="quad",scale=0.05,z=-5)
		self.start_button=ursina.Entity(parent=ursina.camera.ui, position=button_pad_center+(0,0.085*scale,0), texture="assets/start_button.png",model="quad",scale=0.05,z=-5)
		self.select_button=ursina.Entity(parent=ursina.camera.ui, position=button_pad_center+(-0.085*scale,0,0), texture="assets/select_button.png",model="quad",scale=0.05,z=-5)
		self.a_button=ursina.Entity(parent=ursina.camera.ui, position=button_pad_center+(0,-0.085*scale,0), texture="assets/a_button.png",model="quad",scale=0.05,z=-5)
		self.b_button=ursina.Entity(parent=ursina.camera.ui, position=button_pad_center+(0.085*scale,0,0), texture="assets/b_button.png",model="quad",scale=0.05,z=-5)
		self.screen=ursina.Entity(parent=ursina.camera.ui, position=self.position+(0.5*self.scale.x,0.158*self.scale.y),model=ursina.Quad(aspect=(0.9*self.scale.x)/(0.59*self.scale.y)),scale=(0.9*self.scale.x,0.59*self.scale.y),color=ursina.color.black,z=-6)
		self.label=ursina.Entity(parent=ursina.camera.ui, position=start_select_center, texture="assets/lyfe_purple_square.png",model="quad",scale=0.075,z = -5,)
		self.button_press_map = {
			pyboy.WindowEvent.PRESS_ARROW_UP		: self.up_button,
			pyboy.WindowEvent.PRESS_ARROW_DOWN		: self.down_button,
			pyboy.WindowEvent.PRESS_ARROW_LEFT		: self.left_button,
			pyboy.WindowEvent.PRESS_ARROW_RIGHT		: self.right_button,
			pyboy.WindowEvent.PRESS_BUTTON_A		: self.a_button,
			pyboy.WindowEvent.PRESS_BUTTON_B		: self.b_button,
			pyboy.WindowEvent.PRESS_BUTTON_SELECT	: self.select_button,
			pyboy.WindowEvent.PRESS_BUTTON_START	: self.start_button,
		}
		self.button_release_map = {
			pyboy.WindowEvent.RELEASE_ARROW_UP		: self.up_button,
			pyboy.WindowEvent.RELEASE_ARROW_DOWN	: self.down_button,
			pyboy.WindowEvent.RELEASE_ARROW_LEFT	: self.left_button,
			pyboy.WindowEvent.RELEASE_ARROW_RIGHT	: self.right_button,
			pyboy.WindowEvent.RELEASE_BUTTON_A		: self.a_button,
			pyboy.WindowEvent.RELEASE_BUTTON_B		: self.b_button,
			pyboy.WindowEvent.RELEASE_BUTTON_SELECT	: self.select_button,
			pyboy.WindowEvent.RELEASE_BUTTON_START	: self.start_button,
		}
		self.command_que = deque()

	def add_commands(self, user, timeline): 
		self.command_que.extend(timeline)

	def _update(self):
		if self.command_que:
			action = self.command_que.popleft()
			if action:
				for g in self.gameboy.games:
					if self.button_press_map.get(action):
						self.button_press_map.get(action).color=ursina.rgb(145,70,255)
					elif self.button_release_map.get(action):
						self.button_release_map.get(action).color=ursina.color.white
					g.game.send_input(action)

				self.gameboy.handle_command(f"{INPUT_ENUM.action_string[action]}")

class GameBoy(ursina.Entity):
	def __init__(self, name, file, color_palette, *args, **kwargs):
		self.title = name
		self.file = file
		self.color_palette = color_palette
		self.game = pyboy.PyBoy(file,window_type="headless",color_palette=color_palette)
		self.screen = self.game.botsupport_manager().screen()
		scale = kwargs.pop('scale')
		self.backer = ursina.Entity(
			parent=ursina.camera.ui,
			scale=(scale*0.975,0.45),
			position=kwargs.get('position')+(0.0125,-0.0125),
			origin=(-0.5,0),
			model='quad',
			color=ursina.color.black66
		)
		ursina.Entity.__init__(self,
			*args,
			parent=ursina.camera.ui,
			model='quad',
			scale=0.9*scale,
			texture=ursina.Texture(self.game.screen_image().convert("RGBA")),
			rotation_z=180,
			double_sided=True,
			rotation_y=180,
			**kwargs,)
		self.label = ursina.Text(
			parent=ursina.camera.ui,
			position = kwargs.get('position'),
			text=name,
			origin=(0,0),
		)
		self.label.position -= (-scale*0.975/2,-.1900,1)
		self.filtering=None
		self.position += (0.05*scale+0.00625,-0.05*scale,0)
		self.last_frame = None
		self.remaking = False
	def update(self):
		if self.remaking: return
		self.game.tick()
		f = self.screen.raw_screen_buffer() #Although this is a bit slow to call when the screen is updating every frame that is rarely the case
		if not f == self.last_frame: #This prevents an unneeded redraw if the frame data hasn't changed
			self.texture._texture.setRamImageAs(self.game.screen_image().convert("RGBA").tobytes(), "RGBA")
			self.last_frame = f
	def remake(self):
		self.remaking = True
		del self.game
		del self.screen
		self.game = pyboy.PyBoy(self.file,window_type="headless",color_palette=self.color_palette)
		self.screen = self.game.botsupport_manager().screen()
		self.remaking = False
class MultiGameboy(ursina.Ursina):
	def __init__(self):
		ursina.Ursina.__init__(self)
		tile_scale = (ursina.camera.aspect_ratio-0.05)/4
		self.controller = Controller(self, scale=tile_scale,position=ursina.Vec2(-0.25*ursina.camera.aspect_ratio,-0.25), origin=(-0.5,0))
		self.next_backup = time.time() + BACKUP_TIME
		self.messages = []
		self.last_messages = []
		self.commands = []
		self.last_commands = []
		self.loading = False
		self.backup_timer = time.time() + BACKUP_TIME
		
		if os.path.isfile("secrets.py") and not DISABLE_IRC:
			self.twitch_integrator = TwitchIntegrator(self.handle_message, self.controller.add_commands, self.save, self.load, self.backup)
		
		self.games = [
			#(0xf8e8f8,0xf8e070,0xd0a000,0x181010) #Cyan
			#(0xf8e8f8,0xe0a078,0xa87048,0x181010) #Light Blue
			GameBoy('Pokemon Red', 'roms/Pokemon Red.gb',(0xf8e8f8,0x50a0f8,0x3050d0,0x101018), scale=tile_scale, position=ursina.Vec2(-0.5*ursina.camera.aspect_ratio,0.25+0.025), origin=(-0.5,0)),
			GameBoy('Pokemon Green', 'roms/Pokemon Green.gb',(0xf8e8f8,0x80d0a0,0x58a048,0x101018), scale=tile_scale, position=ursina.Vec2(-0.25*ursina.camera.aspect_ratio,0.25+0.025), origin=(-0.5,0)),
			GameBoy('Pokemon Blue', 'roms/Pokemon Blue.gb',(0xf8e8f8,0xd8a090,0xb87858,0x101018), scale=tile_scale, position=ursina.Vec2(0*ursina.camera.aspect_ratio,0.25+0.025), origin=(-0.5,0)),
			GameBoy('Pokemon Yellow', 'roms/Pokemon Yellow.gb',(0xf8e8f8,0x70e0f8,0x00a0d0,0x101018), scale=tile_scale, position=ursina.Vec2(0.25*ursina.camera.aspect_ratio,0.25+0.025), origin=(-0.5,0)),
			GameBoy('Pokemon Gold', 'roms/Pokemon Gold.gb',(0xf8f8f8,0x50b8a0,0x285858,0x181818), scale=tile_scale, position=ursina.Vec2(-0.5*ursina.camera.aspect_ratio,-0.25), origin=(-0.5,0)),
			GameBoy('Pokemon Silver', 'roms/Pokemon Silver.gb',(0xf8e8f8,0xAAAAAA,0x777777,0x181010), scale=tile_scale, position=ursina.Vec2(0.25*ursina.camera.aspect_ratio,-0.25), origin=(-0.5,0)),
		]
		for g in self.games:
			g.game.set_emulation_speed(0)
		self.load()
		# for g in self.games: g.game.set_emulation_speed(0)
		background = ursina.Entity(parent=ursina.camera.ui, add_to_scene_entities=False, eternal=True)
		for g in self.games:
			g.backer.reparent_to(background)
		ignore = [e for e in ursina.scene.entities if not e.parent is background]
		background.combine(ignore=ignore)
		for g in self.games: ursina.destroy(g.backer)

		self.gamepad = ursina.gamepad.input_handler.gamepad

		self.chat = ursina.Entity(
			parent=ursina.camera.ui,
			scale=self.controller.scale,
			position=self.controller.position+(0.25*ursina.camera.aspect_ratio,0,0),
			origin=(-0.5,0),
			model=ursina.deepcopy(self.controller.model),
			color=ursina.color.black66
		)
		self.chat_label = ursina.Text(
			parent=ursina.camera.ui,
			position = self.chat.position+(0.5*tile_scale,0.5*tile_scale,-10),
			text="Twitch Chat",
			origin=(0,0.5),
		)
		self.chat_backer = ursina.Entity(
			parent=ursina.camera.ui,
			scale=self.controller.scale*(0.9,0.8625,1),
			position=self.controller.position+(0.2625*ursina.camera.aspect_ratio,-0.0125,0),
			origin=(-0.5,0),
			model=ursina.deepcopy(self.controller.model),
			color=ursina.color.black
		)
		self.chat_backer.set_scissor((-0.5,-0.495,-0.5),(1,0.5,0.5))
		self.chat_bubbles=[]
		self.command_bubbles=[]
		# for i in range(10): self.handle_message(str(i))
	def update(self):
		if self.backup_timer < time.time():
			self.backup()
			self.backup_timer = time.time()+BACKUP_TIME
		if self.loading: return
		self.controller._update()
		for g in self.games: 
			g.update()
		for m in self.messages.copy():
			if time.time() > m.received_time + MESSAGE_TIMEOUT:
				self.messages.remove(m)
		if not self.messages == self.last_messages:
			for b in self.chat_bubbles: ursina.destroy(b)
			self.chat_bubbles = []
			previous_bubble = None
			for m in reversed(self.messages):
				if previous_bubble:
					bubble = ursina.Text(
						parent=self.chat_backer,
						scale=previous_bubble.scale,
						position=previous_bubble.position+(0,previous_bubble.height+0.02,0),
						origin=(-0.5,-0.5),
						font="assets/JetBrainsMono-Medium.ttf",
						text=m.message,
						wordwrap=18,
						z=-1,
					)
				else:
					bubble = ursina.Text(
						parent=self.chat_backer,
						scale=(0.75/self.chat_backer.scale.x,0.75/self.chat_backer.scale.y,0.75),
						position=self.chat.position-(-0.05*ursina.camera.aspect_ratio*self.chat.scale.x,(0.425)*self.chat.scale.y,1),
						origin=(-0.5,-0.5),
						font="assets/JetBrainsMono-Medium.ttf",
						text=m.message,
						wordwrap=18,
						z=-1,
					)
				previous_bubble = bubble
				self.chat_bubbles.append(bubble)
			self.last_messages = self.messages.copy()
		previous_bubble = None
		for c in self.commands.copy():
			if time.time() > c.received_time + MESSAGE_TIMEOUT:
				self.commands.remove(c)
		if not self.commands == self.last_commands:
			for b in self.command_bubbles: ursina.destroy(b)
			self.command_bubbles = []
			previous_bubble = None
			for c in reversed(self.commands):
				if previous_bubble:
					bubble = ursina.Text(
						parent=self.controller.screen,
						scale=previous_bubble.scale,
						position=previous_bubble.position+(0,previous_bubble.height+0.02,0),
						origin=(-0.5,-0.5),
						font="assets/JetBrainsMono-Medium.ttf",
						text=c.message,
						wordwrap=25,
						z=-1,
					)
				else:
					bubble = ursina.Text(
						parent=self.controller.screen,
						scale=(0.75/self.controller.screen.scale.x,0.75/self.controller.screen.scale.y,0.75),
						position=self.controller.screen.position-(0.5*self.controller.scale.x,0.5*self.controller.scale.y,0),
						origin=(-0.5,-0.5),
						font="assets/JetBrainsMono-Medium.ttf",
						text=c.message,
						wordwrap=25,
						z=-1,
					)
				previous_bubble = bubble
				self.command_bubbles.append(bubble)
			self.last_commands = self.commands.copy()

	def input(self, key):
		return
		self.controller.handle_input(key)

	def handle_message(self, message):
		if len(self.messages)+1>=MAX_MESSAGES: self.messages.pop(0)
		self.messages.append(ScreenMessage(message, time.time()))

	def handle_command(self, command):
		if len(self.commands)+1>=MAX_COMMANDS: self.commands.pop(0)
		self.commands.append(ScreenMessage(command, time.time()))

	def save(self,backup=False):
		for g in self.games:
			g.game.send_input(pyboy.WindowEvent.STATE_SAVE)

	def backup(self):
		for g in self.games:
			g.game.send_input(pyboy.WindowEvent.STATE_SAVE)
			shutil.copyfile(g.file+".state", f"saves/{g.title}__{str(time.time())}__.state")

	def load(self):
		print("Loading")
		self.loading = True
		for g in self.games:
			g.game.send_input(pyboy.WindowEvent.STATE_LOAD)

		self.loading = False

game = MultiGameboy()
update = game.update
# ursina.window.vsync=60
ursina.window.exit_button.enabled=False
ursina.window.fps_counter.scale *= 0.5
ursina.window.fps_counter.position += ursina.Vec3(0,0.02,0)
game.run()