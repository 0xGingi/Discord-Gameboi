import os
import discord, platform, asyncio
import random, time
import subprocess
from PIL import ImageGrab
import io
from pynput.keyboard import Key, Controller
from dotenv import load_dotenv
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
client = discord.Client(intents=intents)
token = os.getenv('DISCORD_TOKEN')

loadedrom = os.getenv('LOADED_ROM')
pathtorom = os.getenv('PATH_TO_ROM') or os.getcwd()
pathtorom += "/" + loadedrom

msg = None
ch = None
UpdateLimit = 3
CurrentUpdate = 0
keyboard = Controller()

movtime = 0.25
emotes = {"LeftArrow": "\u2B05", "DownArrow": "\u2B07", "UpArrow": "\u2B06", "RightArrow": "\u27A1", "AButton": "\U0001F170", "BButton": "\U0001F171", "Start": "\u25B6", "Select": "\U0001F502", "Save": "\U0001F4BE", "Load": "\U0001F504"}
def IsValidReaction(react):
	global emotes
	for emote in emotes:
		if (react == emotes[emote]):
			return True
	return False
	
def GetWindowCoords():
	outs = str(subprocess.check_output(["wmctrl", "-lG"]))[2:-1].split("\\n")
	for f in outs:
		if (f.find("Gambatte SDL") != -1):
			f2 = f.split(" ")
			f = []
			for elem in f2:
				if (elem != ""):
					f.append(elem)

			# Brut
			X1 = int(f[2])
			Y1 = int(f[3]) - 26
			X2 = X1 + int(f[4]) - 1
			Y2 = Y1 + int(f[5])
			return (X1, Y1, X2, Y2)
	return None

new_reaction = False	
frame_without_reaction = 0
async def UpdateFrame():
    global msg
    global CurrentUpdate
    global UpdateLimit
    global new_reaction
    global frame_without_reaction
    while True:
        if ch is not None and frame_without_reaction < 5:
            print ("Updating Frame...")
            await SendImage(True)
            frame_without_reaction += 1
            if not new_reaction:
                await asyncio.sleep(0)
            else:
                new_reaction = False
                frame_without_reaction = 0
        else:
            await asyncio.sleep(0.5)

async def SendImage(react=False):
    global msg
    global ch
    global emotes
    global image_ch
    coords = GetWindowCoords()
    os.system("wmctrl -a 'Gambatte SDL'")
    im = ImageGrab.grab(bbox=(coords[0], coords[1], coords[2], coords[3]))  # X1,Y1,X2,Y2

    with BytesIO() as buf:
        im.save(buf, format='JPEG')
        buf.seek(0)
        image_msg = await image_ch.send(file=discord.File(buf, filename='frame.jpg'))

    image_url = image_msg.attachments[0].url

    if msg is None:
        msg = await ch.send(image_url)
    else:
        await msg.edit(content=image_url)

    if react:
        reactions = [emotes["AButton"], emotes["BButton"], emotes["LeftArrow"], emotes["DownArrow"], emotes["UpArrow"], emotes["RightArrow"], emotes["Start"], emotes["Select"], emotes["Save"], emotes["Load"]]
        await asyncio.gather(*(msg.add_reaction(reaction) for reaction in reactions))


@client.event
async def on_ready():
	global image_ch
	image_ch_id = int(os.getenv('SPAM_CHANNEL_ID'))
	image_ch = client.get_channel(image_ch_id)
	print('All good! Name: ' + client.user.name)
	asyncio.ensure_future(UpdateFrame())
	
	await client.change_presence(activity=discord.Game(name='gameboi start'))

async def SendKey(k, movkey=False):
	global keyboard
	global movtime
	keyboard.press(k)
	if (movkey == False):
		await asyncio.sleep(0.25)
	else:
		await asyncio.sleep(movtime)
		
	keyboard.release(k)
	
@client.event
async def on_reaction_add(reaction, user):
    global msg
    global emotes
    global new_reaction
    global frame_without_reaction
    if reaction.message.author == client.user and user != client.user:
        reaction_emoji = str(reaction)
        if IsValidReaction(reaction_emoji):
            print ("Input Received: " + reaction_emoji)
            os.system("wmctrl -a 'Gambatte SDL'")
            
            if reaction_emoji == emotes["LeftArrow"]:
                await SendKey(Key.left, True)
            elif reaction_emoji == emotes["DownArrow"]:
                await SendKey(Key.down, True)
            elif reaction_emoji == emotes["UpArrow"]:
                await SendKey(Key.up, True)
            elif reaction_emoji == emotes["RightArrow"]:
                await SendKey(Key.right, True)
            elif reaction_emoji == emotes["AButton"]:
                await SendKey("d")
            elif reaction_emoji == emotes["BButton"]:
                await SendKey("c")
            elif reaction_emoji == emotes["Start"]:
                await SendKey(Key.enter)
            elif reaction_emoji == emotes["Select"]:
                await SendKey(Key.shift_r)
            elif reaction_emoji == emotes["Save"]:
                await SendKey(Key.f5)
            elif reaction_emoji == emotes["Load"]:
                await SendKey(Key.f8)
            
            await reaction.remove(user)
            new_reaction = True
            frame_without_reaction = 0

@client.event
async def on_message(message):
	global msg
	global ch
	global CurrentUpdate
	global movtime
	
	if message.author == client.user:
		return
	
	if (message.content == "gameboi start"):
		if (GetWindowCoords() == None):
			os.system("gambatte_sdl " + pathtorom + " --scale 2 &")
			
		while (GetWindowCoords() == None):
			time.sleep(0.1)
		
		if (ch != message.channel):
			ch = message.channel
			msg = None
			CurrentUpdate = 0
	elif (message.content == "gameboi stop"):
		await msg.delete()
		ch = None
	elif (message.content == "gameboi loadrom"):
		pass
	elif (message.content[:8] == "gameboi time"):
		inp = message.content[9:]
		movtime = float(inp)
		if (ch != None and message.channel == ch):
			await ch.send("Setting movement speed as: **" + str(inp) + "** (Default: 0.25)")

while True:
	try:
		client.run(token)
		client.close()
	except Exception as e:
		print (e)
