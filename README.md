# Discord Gameboi

* Requires Linux + X11

* Requires Gambatte (https://github.com/0xGingi/gambatte) 

You will need to install:
- `sudo apt-get install wmctrl libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev`
- `pip install pynput discord.py asyncio python-dotenv pillow`
- `wget https://github.com/0xGingi/gambatte/releases/download/v1/gambatte_sdl`
- `chmod +x gambatte_sdl`
- `sudo mv gambatte_sdl /usr/bin/`

Place gambatte_sdl executable in /usr/bin or add the location to your path


* Takes screenshot of emulator every 1 second & whenever a user reacts
* Emoji reactions for all emulator buttons, including Save/Load State
* Press fastforward reaction then another button reaction to temporarily speedup that button press
* Sends all images to the channel you put in .env (Only If using main.py)
* Use webserver and update discord message with link to image (Only If using main2.py)
* updates message with images from that channel or link
```
gameboi start - start the emulator
gameboi stop - stops the emulator
```


![image](https://github.com/0xGingi/Discord-Gameboi/assets/104647854/d3e851f9-8f5c-4cd8-8157-142c4e26cc83)
