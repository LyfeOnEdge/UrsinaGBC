import pyboy

COMMAND_PREFIX = ","

COMMAND_FLAG = False
MESSAGE_FLAG = not COMMAND_FLAG
FRAMES_PER_ACTION = 6
FRAMES_BETWEEN_ACTIONS = 6


class INPUT_ENUM:
	UP 					= 1
	DOWN 				= 2
	LEFT 				= 3
	RIGHT 				= 4
	A 					= 5
	B 					= 6
	SELECT 				= 7
	START 				= 8

	string = {
		UP 					: "Pressed Up",
		DOWN 				: "Pressed Down",
		LEFT 				: "Pressed Left",
		RIGHT 				: "Pressed Right",
		A 					: "Pressed A",
		B 					: "Pressed B",
		SELECT 				: "Pressed Select",
		START 				: "Pressed Start",
	}

	action_string = {
		pyboy.WindowEvent.PRESS_ARROW_UP		: "Pressed Up",
		pyboy.WindowEvent.PRESS_ARROW_DOWN		: "Pressed Down",
		pyboy.WindowEvent.PRESS_ARROW_LEFT		: "Pressed Left",
		pyboy.WindowEvent.PRESS_ARROW_RIGHT		: "Pressed Right",
		pyboy.WindowEvent.PRESS_BUTTON_A		: "Pressed A",
		pyboy.WindowEvent.PRESS_BUTTON_B		: "Pressed B",
		pyboy.WindowEvent.PRESS_BUTTON_SELECT	: "Pressed Select",
		pyboy.WindowEvent.PRESS_BUTTON_START	: "Pressed Start",
		pyboy.WindowEvent.RELEASE_ARROW_UP		: "Released Up",
		pyboy.WindowEvent.RELEASE_ARROW_DOWN	: "Released Down",
		pyboy.WindowEvent.RELEASE_ARROW_LEFT	: "Released Left",
		pyboy.WindowEvent.RELEASE_ARROW_RIGHT	: "Released Right",
		pyboy.WindowEvent.RELEASE_BUTTON_A		: "Released A",
		pyboy.WindowEvent.RELEASE_BUTTON_B		: "Released B",
		pyboy.WindowEvent.RELEASE_BUTTON_SELECT	: "Released Select",
		pyboy.WindowEvent.RELEASE_BUTTON_START	: "Released Start",
	}

	COMMAND_MAP = {
		"u"				: 	UP,
		"d"				: 	DOWN,
		"l"				: 	LEFT,
		"r"				: 	RIGHT,
		"a"				: 	A,
		"b"				: 	B,
		"s"				: 	SELECT,
		"p"				: 	START,
	}

	ACTIONS = {
		UP		:	(pyboy.WindowEvent.PRESS_ARROW_UP,pyboy.WindowEvent.RELEASE_ARROW_UP),
		DOWN	:	(pyboy.WindowEvent.PRESS_ARROW_DOWN,pyboy.WindowEvent.RELEASE_ARROW_DOWN),
		LEFT	:	(pyboy.WindowEvent.PRESS_ARROW_LEFT,pyboy.WindowEvent.RELEASE_ARROW_LEFT),
		RIGHT	:	(pyboy.WindowEvent.PRESS_ARROW_RIGHT,pyboy.WindowEvent.RELEASE_ARROW_RIGHT),
		A		:	(pyboy.WindowEvent.PRESS_BUTTON_A,pyboy.WindowEvent.RELEASE_BUTTON_A),
		B		:	(pyboy.WindowEvent.PRESS_BUTTON_B,pyboy.WindowEvent.RELEASE_BUTTON_B),
		SELECT	:	(pyboy.WindowEvent.PRESS_BUTTON_SELECT,pyboy.WindowEvent.RELEASE_BUTTON_SELECT),
		START	:	(pyboy.WindowEvent.PRESS_BUTTON_START,pyboy.WindowEvent.RELEASE_BUTTON_START),
	}
	def __init__(self):
		pass


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