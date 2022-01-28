import pyboy
from .constants import *
# irc_control syntax

## Single Command
### !c

## MultiCommand
# eg = ".u 6.d 4.l 2.r 3"
# eg = ".u.d 4.l .r 3"

def handle_input(msg):
	msg = santize_input(msg)
	if classify_message(msg) is COMMAND_FLAG:
		parsed_command = parse_command(msg)
		if parsed_command == -1: return parsed_command
		timeline = generate_input_timeline_from_parsed_commands(parsed_command)
		return COMMAND_FLAG, timeline
	else:
		return MESSAGE_FLAG, msg

def classify_message(msg):
	if msg.startswith(COMMAND_PREFIX):
		return COMMAND_FLAG
	else:
		return MESSAGE_FLAG

def santize_input(msg): return msg.strip()

def parse_command(command):
	try:
		command=command[1:].lower().strip(COMMAND_PREFIX)
		print(f"Parsing command {command}")
		if COMMAND_PREFIX in command:
			command = command.split(COMMAND_PREFIX)
		else:
			command = [command]
		parsed = []
		for c in command:
			c = c.strip()
			parsed.append(c)
		return parsed
	except Exception as e:
		print(f"Error parsing command {command}")
		return -1

def generate_input_timeline_from_parsed_commands(inputs):
	timeline = []
	for i in inputs:
		if i in ('', ' '): continue
		if not INPUT_ENUM.COMMAND_MAP.get(i):
			print(f"Ignoring unknown command {i}")
			continue
		timeline.append(INPUT_ENUM.ACTIONS[INPUT_ENUM.COMMAND_MAP[i]][0])
		for _ in range(int(FRAMES_PER_ACTION)): timeline.append([]) #Empty frames for wait
		timeline.append(INPUT_ENUM.ACTIONS[INPUT_ENUM.COMMAND_MAP[i]][1]) #Unpress button
		for _ in range(FRAMES_PER_ACTION): timeline.append([])
	return timeline