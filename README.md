run `pip install -r requirements.txt`
For Twitch Integration create secrets.py using secrets_default.py as a template
Xbox controller must be plugged in at app start to be enabled
Roms must be put in ./roms
Currently games must be assigned manually in the MultiGameboy object in multiGBC.py, see below
Comment out any gameboys you don't need, update the names / files / pallets etc to match the games you wish to load
```py
self.games = [
	GameBoy(NAME, GAME_FILE, GAME_PALLETE, scale="!DON'T CHANGE!", position="!DON'T CHANGE!", origin="!DON'T CHANGE!"),
	GameBoy('Pokemon Red', 'roms/Pokemon Red.gb',(0xf8e8f8,0x50a0f8,0x3050d0,0x101018), ...),
]
```
