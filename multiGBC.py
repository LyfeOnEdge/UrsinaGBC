import os, time
import ursina
import pyboy
from PIL import Image
from panda3d.core import InputDevice, Texture as PandaTexture

if os.path.isfile("secrets.py"):
	from twitch_integrator import TwitchIntegrator

os.makedirs("saves", exist_ok=True)
ursina.Text.default_font = "assets/OpenSans-Bold.ttf"

BACKUP_TIME = 10*60
MESSAGE_TIMEOUT = 99999999 #Meh, looks too empty with slow chat
MAX_MESSAGES = 15
MAX_COMMANDS = 10
PRESS_DURATION = 0.1

class INPUT_ENUM:
	UP 					= 1
	DOWN 				= 2
	LEFT 				= 3
	RIGHT 				= 4
	A 					= 5
	B 					= 6
	SELECT 				= 7
	START 				= 8
	HOLD_UP 			= 10
	HOLD_DOWN 			= 20
	HOLD_LEFT 			= 30
	HOLD_RIGHT 			= 40
	HOLD_A 				= 50
	HOLD_B 				= 60
	HOLD_SELECT 		= 70
	HOLD_START 			= 80
	HOLD_RELEASE_UP 	= 100
	HOLD_RELEASE_DOWN 	= 200
	HOLD_RELEASE_LEFT 	= 300
	HOLD_RELEASE_RIGHT 	= 400
	HOLD_RELEASE_A 		= 500
	HOLD_RELEASE_B 		= 600
	HOLD_RELEASE_SELECT = 700
	HOLD_RELEASE_START 	= 800

	string = {
		UP 					: "Pressed Up",
		DOWN 				: "Pressed Down",
		LEFT 				: "Pressed Left",
		RIGHT 				: "Pressed Right",
		A 					: "Pressed A",
		B 					: "Pressed B",
		SELECT 				: "Pressed Select",
		START 				: "Pressed Start",
		HOLD_UP 			: "Held Up",
		HOLD_DOWN 			: "Held Down",
		HOLD_LEFT 			: "Held Left",
		HOLD_RIGHT 			: "Held Right",
		HOLD_A 				: "Held A",
		HOLD_B 				: "Held B",
		HOLD_SELECT 		: "Held Select",
		HOLD_START 			: "Held Start",
		HOLD_RELEASE_UP 	: "Released Up",
		HOLD_RELEASE_DOWN 	: "Released Down",
		HOLD_RELEASE_LEFT 	: "Released Left",
		HOLD_RELEASE_RIGHT 	: "Released Right",
		HOLD_RELEASE_A 		: "Released A",
		HOLD_RELEASE_B 		: "Released B",
		HOLD_RELEASE_SELECT : "Released Select",
		HOLD_RELEASE_START 	: "Released Start",
	}
	def __init__(self):
		pass

COMMAND_MAP = {
	"up"			: 	INPUT_ENUM.UP,
	"u"				: 	INPUT_ENUM.UP,
	"down"			: 	INPUT_ENUM.DOWN,
	"d"				: 	INPUT_ENUM.DOWN,
	"left"			: 	INPUT_ENUM.LEFT,
	"l"				: 	INPUT_ENUM.LEFT,
	"right"			: 	INPUT_ENUM.RIGHT,
	"r"				: 	INPUT_ENUM.RIGHT,
	"a"				: 	INPUT_ENUM.A,
	"b"				: 	INPUT_ENUM.B,
	"select"		: 	INPUT_ENUM.SELECT,
	"sel"			: 	INPUT_ENUM.SELECT,
	"start"			: 	INPUT_ENUM.START,
	"hold_up"		:  	INPUT_ENUM.HOLD_UP,
	"hu"			:  	INPUT_ENUM.HOLD_UP,
	"hold_down"		: 	INPUT_ENUM.HOLD_DOWN,
	"hd"			: 	INPUT_ENUM.HOLD_DOWN,
	"hold_left"		: 	INPUT_ENUM.HOLD_LEFT,
	"hl"			: 	INPUT_ENUM.HOLD_LEFT,
	"hold_right"	: 	INPUT_ENUM.HOLD_RIGHT,
	"hr"			: 	INPUT_ENUM.HOLD_RIGHT,
	"hold_a"		: 	INPUT_ENUM.HOLD_A,
	"ha"			: 	INPUT_ENUM.HOLD_A,
	"hold_b"		: 	INPUT_ENUM.HOLD_B,
	"hb"			: 	INPUT_ENUM.HOLD_B,
	"hold_select"	: 	INPUT_ENUM.HOLD_SELECT,
	"hsel"			: 	INPUT_ENUM.HOLD_SELECT,
	"hold_start"	:	INPUT_ENUM.HOLD_START,
	"hs"			:	INPUT_ENUM.HOLD_START,
	"release_up"	:  	INPUT_ENUM.HOLD_RELEASE_UP,
	"ru"			:  	INPUT_ENUM.HOLD_RELEASE_UP,
	"release_down"	: 	INPUT_ENUM.HOLD_RELEASE_DOWN,
	"rd"			: 	INPUT_ENUM.HOLD_RELEASE_DOWN,
	"release_left"	: 	INPUT_ENUM.HOLD_RELEASE_LEFT,
	"rl"			: 	INPUT_ENUM.HOLD_RELEASE_LEFT,
	"release_right"	: 	INPUT_ENUM.HOLD_RELEASE_RIGHT,
	"rr"			: 	INPUT_ENUM.HOLD_RELEASE_RIGHT,
	"release_a"		: 	INPUT_ENUM.HOLD_RELEASE_A,
	"ra"			: 	INPUT_ENUM.HOLD_RELEASE_A,
	"release_b"		: 	INPUT_ENUM.HOLD_RELEASE_B,
	"rb"			: 	INPUT_ENUM.HOLD_RELEASE_B,
	"release_select": 	INPUT_ENUM.HOLD_RELEASE_SELECT,
	"rsel"			: 	INPUT_ENUM.HOLD_RELEASE_SELECT,
	"release_start"	:	INPUT_ENUM.HOLD_RELEASE_START,
	"rs"			:	INPUT_ENUM.HOLD_RELEASE_START,
}

KEYMAP = {
	"gamepad dpad up": pyboy.WindowEvent.PRESS_ARROW_UP,
	"gamepad dpad up up": pyboy.WindowEvent.RELEASE_ARROW_UP,
	"w" : pyboy.WindowEvent.PRESS_ARROW_UP,
	"w up" : pyboy.WindowEvent.RELEASE_ARROW_UP,
	"gamepad dpad down": pyboy.WindowEvent.PRESS_ARROW_DOWN,
	"gamepad dpad down up": pyboy.WindowEvent.RELEASE_ARROW_DOWN,
	"s" : pyboy.WindowEvent.PRESS_ARROW_DOWN,
	"s up" : pyboy.WindowEvent.RELEASE_ARROW_DOWN,
	"gamepad dpad left": pyboy.WindowEvent.PRESS_ARROW_LEFT,
	"gamepad dpad left up": pyboy.WindowEvent.RELEASE_ARROW_LEFT,
	"a" : pyboy.WindowEvent.PRESS_ARROW_LEFT,
	"a up" : pyboy.WindowEvent.RELEASE_ARROW_LEFT,
	"gamepad dpad right": pyboy.WindowEvent.PRESS_ARROW_RIGHT,
	"gamepad dpad right up": pyboy.WindowEvent.RELEASE_ARROW_RIGHT,
	"d" : pyboy.WindowEvent.PRESS_ARROW_RIGHT,
	"d up" : pyboy.WindowEvent.RELEASE_ARROW_RIGHT,
	"gamepad a": pyboy.WindowEvent.PRESS_BUTTON_A,
	"gamepad a up": pyboy.WindowEvent.RELEASE_BUTTON_A,
	"e": pyboy.WindowEvent.PRESS_BUTTON_A,
	"e up": pyboy.WindowEvent.RELEASE_BUTTON_A,
	"gamepad b": pyboy.WindowEvent.PRESS_BUTTON_B,
	"gamepad b up": pyboy.WindowEvent.RELEASE_BUTTON_B,
	"r": pyboy.WindowEvent.PRESS_BUTTON_B,
	"r up": pyboy.WindowEvent.RELEASE_BUTTON_B,
	"gamepad back": pyboy.WindowEvent.PRESS_BUTTON_SELECT,
	"gamepad back up": pyboy.WindowEvent.RELEASE_BUTTON_SELECT,
	"t": pyboy.WindowEvent.PRESS_BUTTON_SELECT,
	"t up": pyboy.WindowEvent.RELEASE_BUTTON_SELECT,
	"gamepad start": pyboy.WindowEvent.PRESS_BUTTON_START,
	"gamepad start up": pyboy.WindowEvent.RELEASE_BUTTON_START,
	"q": pyboy.WindowEvent.PRESS_BUTTON_START,
	"q up": pyboy.WindowEvent.RELEASE_BUTTON_START,
}

class ScreenMessage:
	def __init__(self, message, received_time):
		self.message, self.received_time = message, received_time

class Controller(ursina.Entity):
	def __init__(self, gameboy, *args, **kwargs):
		scale = kwargs.pop('scale')
		ursina.Entity.__init__(self, *args, parent=ursina.camera.ui, scale=(scale*0.975,0.45), model=ursina.Quad(radius=0.1), color=ursina.color.black66, **kwargs)
		self.position += (0.0125,-0.0125)
		self.gameboy = gameboy
		d_pad_center = self.position + (0.275*scale, -0.34*scale)
		button_pad_center = self.position + (0.725*scale,-0.34*scale)
		start_select_center = self.position + (0.5*scale, -0.24*scale)
		self.up_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0,0.07*scale,0), texture="assets/d_pad.png",rotation_z=90,model="quad",scale=0.05,z=-5)
		self.down_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0,-0.07*scale,0), texture="assets/d_pad.png",rotation_z=270,model="quad",scale=0.05,z=-5)
		self.left_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(-0.07*scale,0,0), texture="assets/d_pad.png",rotation_z=0,model="quad",scale=0.05,z=-5)
		self.right_button=ursina.Entity(parent=ursina.camera.ui, position=d_pad_center+(0.07*scale,0,0), texture="assets/d_pad.png",rotation_z=180,model="quad",scale=0.05,z=-5)
		
		self.inputs = {}

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

		self.actions = {
			INPUT_ENUM.UP					:	(pyboy.WindowEvent.PRESS_ARROW_UP,pyboy.WindowEvent.RELEASE_ARROW_UP),
			INPUT_ENUM.DOWN					:	(pyboy.WindowEvent.PRESS_ARROW_DOWN,pyboy.WindowEvent.RELEASE_ARROW_DOWN),
			INPUT_ENUM.LEFT					:	(pyboy.WindowEvent.PRESS_ARROW_LEFT,pyboy.WindowEvent.RELEASE_ARROW_LEFT),
			INPUT_ENUM.RIGHT				:	(pyboy.WindowEvent.PRESS_ARROW_RIGHT,pyboy.WindowEvent.RELEASE_ARROW_RIGHT),
			INPUT_ENUM.A					:	(pyboy.WindowEvent.PRESS_BUTTON_A,pyboy.WindowEvent.RELEASE_BUTTON_A),
			INPUT_ENUM.B					:	(pyboy.WindowEvent.PRESS_BUTTON_B,pyboy.WindowEvent.RELEASE_BUTTON_B),
			INPUT_ENUM.SELECT				:	(pyboy.WindowEvent.PRESS_BUTTON_SELECT,pyboy.WindowEvent.RELEASE_BUTTON_SELECT),
			INPUT_ENUM.START				:	(pyboy.WindowEvent.PRESS_BUTTON_START,pyboy.WindowEvent.RELEASE_BUTTON_START),
			INPUT_ENUM.HOLD_UP				:	(pyboy.WindowEvent.PRESS_ARROW_UP,None),
			INPUT_ENUM.HOLD_DOWN			:	(pyboy.WindowEvent.PRESS_ARROW_DOWN,None),
			INPUT_ENUM.HOLD_LEFT			:	(pyboy.WindowEvent.PRESS_ARROW_LEFT,None),
			INPUT_ENUM.HOLD_RIGHT			:	(pyboy.WindowEvent.PRESS_ARROW_RIGHT,None),
			INPUT_ENUM.HOLD_A				:	(pyboy.WindowEvent.PRESS_BUTTON_A,None),
			INPUT_ENUM.HOLD_B				:	(pyboy.WindowEvent.PRESS_BUTTON_B,None),
			INPUT_ENUM.HOLD_SELECT 			:	(pyboy.WindowEvent.PRESS_BUTTON_SELECT, None),
			INPUT_ENUM.HOLD_START			:	(pyboy.WindowEvent.PRESS_BUTTON_START, None),
			INPUT_ENUM.HOLD_RELEASE_UP		:	(pyboy.WindowEvent.RELEASE_ARROW_UP,None),
			INPUT_ENUM.HOLD_RELEASE_DOWN	:	(pyboy.WindowEvent.RELEASE_ARROW_DOWN,None),
			INPUT_ENUM.HOLD_RELEASE_LEFT	:	(pyboy.WindowEvent.RELEASE_ARROW_LEFT,None),
			INPUT_ENUM.HOLD_RELEASE_RIGHT	:	(pyboy.WindowEvent.RELEASE_ARROW_RIGHT,None),
			INPUT_ENUM.HOLD_RELEASE_A		:	(pyboy.WindowEvent.RELEASE_BUTTON_A,None),
			INPUT_ENUM.HOLD_RELEASE_B		:	(pyboy.WindowEvent.RELEASE_BUTTON_B,None),
			INPUT_ENUM.HOLD_RELEASE_SELECT	:	(pyboy.WindowEvent.RELEASE_BUTTON_SELECT,None),
			INPUT_ENUM.HOLD_RELEASE_START	:	(pyboy.WindowEvent.RELEASE_BUTTON_START,None),
		}

		self.overrides = {
			INPUT_ENUM.HOLD_UP		:	INPUT_ENUM.UP,
			INPUT_ENUM.HOLD_DOWN	:	INPUT_ENUM.DOWN,
			INPUT_ENUM.HOLD_LEFT	:	INPUT_ENUM.LEFT,
			INPUT_ENUM.HOLD_RIGHT	:	INPUT_ENUM.RIGHT,
			INPUT_ENUM.HOLD_A		:	INPUT_ENUM.A,
			INPUT_ENUM.HOLD_B		:	INPUT_ENUM.B,
			INPUT_ENUM.HOLD_SELECT	:	INPUT_ENUM.SELECT,
			INPUT_ENUM.HOLD_START	:	INPUT_ENUM.START,
		}

	def handle_command(self, user, command):
		command = command.strip().lower()
		event = COMMAND_MAP.get(command)
		if event:
			self.gameboy.handle_command(f"{user} {INPUT_ENUM.string[event]}")
			self.handle_event(event)

	def handle_event(self, event):
		action = self.actions.get(event)
		for g in self.gameboy.games:
			g.game.send_input(action[0])
			if self.button_press_map.get(action[0]):
				self.button_press_map.get(action[0]).color=ursina.rgb(145,70,255)
			elif self.button_release_map.get(action[0]):
				self.button_release_map.get(action[0]).color=ursina.color.white
		if not action[1] == None:
			self.inputs[event] = time.time() + PRESS_DURATION #Reset timer for stop action, this way multiple of the same command just resets the walk action
		else:
			if self.overrides.get(event):
				if self.inputs.get(self.overrides[event]):
					self.inputs.pop(self.overrides[event]) #Prevents a losing button holds due to the stop actions triggering

	def handle_input(self, key):
		if KEYMAP.get(key):
			action = KEYMAP[key]
			print(f"R {key} - S {action}")
			for g in self.gameboy.games:
				g.game.send_input(action)
			if self.button_press_map.get(action):
				self.button_press_map.get(action).color=ursina.rgb(145,70,255)
			elif self.button_release_map.get(action):
				self.button_release_map.get(action).color=ursina.color.white
		else:
			print(f"Unmapped key {key}") 

	def _update(self):
		for event in self.inputs.keys():
			if self.inputs[event] < time.time():
				for g in self.gameboy.games:
					action = self.actions[event][1]
					if self.button_press_map.get(action):
						self.button_press_map.get(action).color=ursina.rgb(145,70,255)
					elif self.button_release_map.get(action):
						self.button_release_map.get(action).color=ursina.color.white
					g.game.send_input(action)

class GameBoy(ursina.Entity):
	def __init__(self, name, file, color_palette, *args, **kwargs):
		self.title = name
		self.file = file
		self.color_palette = color_palette
		self.game = pyboy.PyBoy(file,window_type="headless",color_palette=color_palette)
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
		self.screen = self.game.botsupport_manager().screen()
		self.last_frame = None
	def update(self):
		self.game.tick()
		f = self.screen.raw_screen_buffer() #Although this is a bit slow to call when the screen is updating every frame that is rarely the case
		if not f == self.last_frame: #This prevents an unneeded redraw if the frame data hasn't changed
			self.texture._texture.setRamImageAs(self.game.screen_image().convert("RGBA").tobytes(), "RGBA")
			self.last_frame = f

class MultiGameboy(ursina.Ursina):
	def __init__(self):
		ursina.Ursina.__init__(self)
		tile_scale = (ursina.camera.aspect_ratio-0.05)/4
		# self.background = ursina.Entity(parent=ursina.camera.ui, scale=1, model='quad', texture="pikachu_thicc.jpg", z=-5,color=ursina.color.white33)
		self.controller = Controller(self, scale=tile_scale,position=ursina.Vec2(-0.25*ursina.camera.aspect_ratio,-0.25), origin=(-0.5,0))
		self.next_backup = time.time() + BACKUP_TIME
		self.messages = []
		self.last_messages = []
		self.commands = []
		self.last_commands = []
		
		if os.path.isfile("secrets.py"):
			self.twitch_integrator = TwitchIntegrator(self.handle_message, self.controller.handle_command)
		
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
		# if time.time() > self.next_backup:
		# 	self.save(backup=True)
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
		self.controller.handle_input(key)

	def handle_message(self, message):
		if len(self.messages)+1>=MAX_MESSAGES: self.messages.pop(0)
		self.messages.append(ScreenMessage(message, time.time()))

	def handle_command(self, command):
		if len(self.commands)+1>=MAX_COMMANDS: self.commands.pop(0)
		self.commands.append(ScreenMessage(command, time.time()))

	def save(self,backup=False):
		return #BROKEN
		for g in self.games:
			with open(f"saves/{g.title}.state_backup" if backup else f"saves/{g.title}.state", 'wb+') as f:
				g.game.save_state(f)

	def load(self):
		return #BROKEN
		for g in self.games:
			with open(f"saves/{g.title}.state", 'rb') as f:
				g.game.stop(save=False)
				g.game = pyboy.PyBoy(g.file,window_type="headless",color_palette=g.color_palette)
				g.game.load_state(f)

game = MultiGameboy()
update = game.update
ursina.window.vsync=60
ursina.window.exit_button.enabled=False
ursina.window.fps_counter.scale *= 0.5
ursina.window.fps_counter.position += ursina.Vec3(0,0.02,0)
game.run()