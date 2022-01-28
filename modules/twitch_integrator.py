import sys, time, socket, secrets
from direct.stdpy import thread
from .irc_parser import handle_input
from .constants import *
global command_cooldown
command_cooldown = []
message = ' '
user = ' '


HELP_MESSAGE =	f"Start your command and separate each input with '{COMMAND_PREFIX}' eg: {COMMAND_PREFIX}u{COMMAND_PREFIX}u{COMMAND_PREFIX}a{COMMAND_PREFIX}r{COMMAND_PREFIX}a{COMMAND_PREFIX}a{COMMAND_PREFIX}b || (u)p | (d)own | (l)eft | (r)ight | (a) | (b) | (s)elect | (p)ause"


class TwitchIntegrator():
	def __init__(self, message_handler, command_handler, save_func, load_func, backup_func):
		self.server = "irc.twitch.tv"
		self.port = 6667
		self.password = secrets.PASS
		self.bot = secrets.BOT
		self.channel = secrets.CHANNEL
		self.save_func, self.load_func, self.backup_func = save_func, load_func, backup_func
		self.owner = OWNER = secrets.OWNER
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
		print(messageTemp)
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
					if message == f"{COMMAND_PREFIX}help": #Not a normally handled command
						self.sendMessage(HELP_MESSAGE)
						continue
					if message == f"{COMMAND_PREFIX}save" and user==self.owner: #Not a normally handled command
						self.save_func()
						continue
					if message == f"{COMMAND_PREFIX}load" and user==self.owner: #Not a normally handled command
						self.load_func()
						continue
					if message == f"{COMMAND_PREFIX}backup" and user==self.owner: #Not a normally handled command
						self.backup_func()
						continue
					handled = handle_input(message)
					if handled == -1:
						self.sendMessage(f"@{user} - unrecognized command {message}")
						continue
					flag, data = handled
					if flag is COMMAND_FLAG:
						self.command_handler(user.title(), data)
					elif flag is MESSAGE_FLAG:
						self.message_handler(user.title() + "|" + message)