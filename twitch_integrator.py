import sys, time, socket, secrets
from direct.stdpy import thread

global command_cooldown
command_cooldown = []
message = ' '
user = ' '

HELP_MESSAGES = [
	"All commands must be prefixed by '!' || Alternate upper/lower to bypass rate limit || Abbrv commands are in parenthesis ||",
	"(u)p | (d)own | (l)eft | (r)ight | (a) | (b) | (sel)ect | (s)tart | (hu) hold_up | (hd) hold_down | (hl) hold_left | (hr) hold_right | (ha) hold_a | (hb) hold_b | (hs) hold_start | (hsel) hold_select | (ru) release_up | (rd) release_down | (rl) release_left | (rr) release_right | (ra) release_a | (rb) release_b | (rs) release_start | (rsel) release_select",
]

class TwitchIntegrator():
	def __init__(self, message_handler, command_handler):
		self.server = "irc.twitch.tv"
		self.port = 6667
		self.password = secrets.PASS
		self.bot = secrets.BOT
		self.channel = secrets.CHANNEL
		OWNER = secrets.OWNER
		self.message_handler = message_handler
		self.command_handler = command_handler
		self.irc = socket.socket()
		self.irc.connect((self.server, self.port))
		self.irc.send((	"PASS " + self.password + "\n" +
					"NICK " + self.bot + "\n" +
					"JOIN #" + self.channel + "\n").encode())
		self.joinchat( )
		thread.start_new_thread(function=self.update, args='')

	def handle_input(self):
		global user
		global message
		
		if message.lower() == 'w':
			pass
		message=''  
		return

	def joinchat(self):
		loading = True
		while loading:
			readbuffer_join = self.irc.recv(1024)
			readbuffer_join = readbuffer_join.decode()                
			for line in readbuffer_join.split("\n")[0:-1]:                    
				loading = self.loadingComplete(line)
		print("Joined chat")

	def loadingComplete(self, line):
		if("End of /NAMES list" in line):
			return False
		else:
			return True

	def getUser(self, line):
		global user
		colons = line.count(":")
		colonless = colons-1
		separate = line.split(":", colons)
		user = separate[colonless].split("!", 1)[0]
		return user

	def getMessage(self, line):
		global message
		try:
			colons = line.count(":")
			message = (line.split(":", colons))[colons]
		except:
			message = ""
		return message

	def sendMessage(self, message):
		messageTemp = "PRIVMSG #" + self.channel + " :" + message
		self.irc.send((messageTemp + "\n").encode())

	def console(self, line):
		if "PRIVMSG" in line:
			return False
		else:
			return True

	def update(self):
		global user
		while True:
			try:
				readbuffer = self.irc.recv(1024).decode()
			except:
				readbuffer = ""
			for line in readbuffer.split("\r\n"):
				if line == "":
					continue
				if "PING :tmi.twitch.tv" in line:
					msgg = "PONG :tmi.twitch.tv\r\n".encode()
					self.irc.send(msgg)
					continue
				else:
					user = self.getUser(line)
					message = self.getMessage(line).strip()
					if user == "" or user == " ":
						continue
					
					if message.startswith("!"):
						if message == "!help": #Not a handled command
							for m in HELP_MESSAGES:
								self.sendMessage(m)
							continue
						self.command_handler(user.title(), message.strip("!"))
					else:
						self.message_handler(user.title() + "|" + message)
						thread.start_new_thread(function=self.handle_input, args='')