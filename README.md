run `pip install -r requirements.txt`

For Twitch Integration create secrets.py using secrets_default.py as a template

Xbox controller must be plugged in at app start to be enabled

I recommend putting roms in ./roms, but there is no autodetection so it's not required

Currently games must be assigned manually in the MultiGameboy object in multiGBC.py, see below

Comment out any gameboys you don't need, update the names / files / pallets etc to match the games you wish to load

```py
self.games = [
	GameBoy(NAME, GAME_FILE, GAME_PALLETE, scale="!DON'T CHANGE!", position="!DON'T CHANGE!", origin="!DON'T CHANGE!"),
	GameBoy('Pokemon Red', 'roms/Pokemon Red.gb',(0xf8e8f8,0x50a0f8,0x3050d0,0x101018), ...),
]
```

### Controls:

	wasd = up left down right
	
	e = a
	
	r = b
	
	t = select
	
	q = start
	
### Known issues:

Games become laggggggy when using both irc and controller/keyboard input, needs investigation
I think I'm using save states wrong... Errors on state load a lot. Disabled for now.

### Todo:

spam button option

mini irc scripting language to make things less tedius
