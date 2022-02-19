import os
import discord
import random
import requests
import asyncio
#import time

from _thread import *
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL


# ~~~~ Current Bugs ~~~~
#Rewrite the entire play function -This is a part of fixing everything lmao

#Create the loop function
#Revamp the google function to get actual google stats
#Make a stocks command! #Possibly combine with the google command
#Spotify stats too if possible
#Use the Paucalled variable to figure out how to pause the timer! I got an idea of using a if statement
#The clear function only works properly if there is more than one song. :pensive:

#It only counts down the queue, once another song is added.

def PauseCalled():
  global PauCalled
  if (PauCalled == True):
    PauCalled = False
  else:
    PauCalled = True
PauCalled = False

#Metal Cup Drink
client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True)

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {'format': 'bestaudio'}

splitResp = []
songQueue = []
songDuration = []
numQueue = []
nextSong = []
nextPlaylistSong = []
DoujinMax = 386430
tagNum = 0
num = 0


RandRep = [
    "I'm doing great {message.author.nic}, How about you?",
    "I'm doing amazing! You?", "I'm doing decently, how are you? ",
    "I'm doing good :smile:, you? ",
    "I am just living life, How have have you been doing?"
]

RandRepH = [
    "That's good to hear!", "That's nice to hear", "That's nice",
    "Ah, I'm happy to hear that!", "Damn, that's good"
]

RandRepS = [
    "Really? That hurts to hear", "That's sad", ":damn:", "hold that, bozo",
    "**Damn**"
]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(
      activity=discord.Activity(type=discord.ActivityType.watching,
      name="Kyle struggle with errors with Zion"))

@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    #Responses
    msg = message.content
    RandRep = [
        f"I'm doing great {message.author}, How about you?",
        f"I'm doing amazing! You? {message.author}",
        "I'm doing decently, how are you? ", "I'm doing good :smile:, you? ",
        "I am just living life, How have have you been doing?"
    ]
  
    if msg.startswith('~How are'):
        RandRepR = random.randint(0, 4)
        await message.channel.send(RandRep[RandRepR])

        if msg.startswith("I'm doing good") or msg.startswith(
                "I'm good") or msg.startswith("I'm g") or msg.startswith(
                    'good'):
            RandRepR = random.randint(0, 4)
            await message.channel.send(RandRepH[RandRepR])

        if msg.startswith("~I'm doing bad") or msg.startswith(
                "!I'm bad") or msg.startswith("!I'm b") or msg.startswith(
                    'bad') or msg.startswith('Terrible') or msg.startswith(
                        'unlucky'):
            RandRepR = random.randint(0, 4)
            await message.channel.send(RandRepS[RandRepR])

        if msg.startswith("~I miss "):
            await message.channel.send(":monkey:")
          
    await bot.process_commands(message)


@bot.command(aliases=['doujinshi'])
async def doujin(ctx, arg):
    print("The user asked for doujin number " + arg + "\n")
    if int(arg) > DoujinMax:
        await ctx.channel.send('The number is too high! Redo the command!')

    if int(arg) < DoujinMax:
        Embed = discord.Embed(
            title='Doujinshi Deliverer!',
            description=(f'[**Your doujin!**](https://nhentai.net/g/{arg}/)'),
            color=discord.Color.from_rgb(255, 0, 0))
        #Embed.set_image(url="https://c.tenor.com/7fuoqpm9DtwAAAAd/please-dont-bully-me-anime.gif")
        await ctx.channel.send(embed=Embed)


@bot.command(aliases=['RDoujin', 'randd', 'randdoujin', 'rdoujinishi'])
async def rand(ctx):
    RandDoujin = random.randint(0, 374191)
    print(f"The random doujin that the user got was {RandDoujin}")
    Embed = discord.Embed(
        title='Randomize Doujin!',
        description=
        f'[:tada:**Your mysterious doujin!**:tada:](https://nhentai.net/g/{RandDoujin}/)',
        color=discord.Color.from_rgb(101, 67, 33))
    Embed.set_image(
        url=
        "https://c.tenor.com/7fuoqpm9DtwAAAAd/please-dont-bully-me-anime.gif")
    await ctx.channel.send(embed=Embed)


@bot.command(aliases=['RHentai', 'randhentai', 'randh'])
async def hrand(ctx):
    RandHentai = random.randint(0, 99999999999999)
    print(f"The random hentai that the user got was {RandHentai}")
    Embed = discord.Embed(
        title='Randomize Hanime Page!',
        description=
        f'[:monkey:**Hanime randomized!**:monkey:](https://hanime.tv/browse/random?r={RandHentai})',
        color=discord.Color.from_rgb(101, 67, 33))
    Embed.set_image(
        url="https://c.tenor.com/Fl6m3zSv3XgAAAAd/monkey-spinning.gif")
    await ctx.channel.send(embed=Embed)

@bot.command(aliases=['char', 'character'])
async def tag(ctx, *, arg):
    if ' ' in arg:
        splitResp = arg.split(' ')
        JoinedResp = ('+'.join(splitResp))
        await ctx.channel.send(
            f'The tag/character you searched for is!\nhttps://nhentai.net/search/?q={JoinedResp}'
        )
    else:
        await ctx.channel.send(
            f'The tag/character you searched for is!\nhttps://nhentai.net/search/?q={arg}'
        )


@bot.command()
async def google(ctx, *, arg):
    JoinedResp = arg
    if " " in arg:
        splitResp = arg.split(' ')
        JoinedResp = ('+'.join(splitResp))
    Embed = discord.Embed(
        title='Your Google Search',
        description=
        f'[**`Your search result!`**:mag_right:](https://www.google.com/search?q={JoinedResp}&ei=yAozYeGyIuyOwbkP34iDqAw&oq={JoinedResp}&gs_lcp=Cgdnd3Mtd2l6EAMyCgguELEDEEMQkwIyCwguELEDEMcBEKMCMggIABCABBCxAzIICC4QgAQQsQMyBQguEIAEMggIABCABBCxAzIICAAQgAQQsQMyCwguEIAEEMcBEK8BMggIABCABBCxAzIICAAQgAQQsQM6DggAEOoCELQCENkCEOUCOgcILhBDEJMCOgQIABBDOgQILhBDOhEILhCABBCxAxCDARDHARDRAzoOCC4QgAQQsQMQxwEQ0QM6EQguEIAEELEDEIMBEMcBEKMCOg4ILhCABBCxAxDHARCjAjoFCAAQgAQ6DQguEMcBENEDEEMQkwI6EAguELEDEIMBEMcBEKMCEEM6CgguELEDEIMBEEM6CAgAEIAEEMkDOgUIABCSAzoHCC4QsQMQQzoHCAAQsQMQQ0oECEEYAFDdyh9Y9dIfYOjUH2gBcAJ4AIABzwGIAZUHkgEFMi40LjGYAQCgAQGwAQjAAQE&sclient=gws-wiz&ved=0ahUKEwjhtqu60eTyAhVsRzABHV_EAMUQ4dUDCA4&uact=5)',
        color=discord.Color.from_rgb(27, 30, 35))
    await ctx.channel.send(embed=Embed)


#Join Function
@bot.command(aliases=['j'])
async def join(ctx):
    connected = ctx.author.voice
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    bot_connection = ctx.guild.voice_client
    if connected and voice == None:
        channel = ctx.author.voice.channel
        await channel.connect()
    if not voice == None:
        await bot_connection.move_to(ctx.author.voice.channel)
    if not connected:
        await ctx.channel.send("You aren't currently in the voice channel.")
        await ctx.channel.send("https://c.tenor.com/c6rLwFIEvDcAAAAC/touhou-b7touhou.gif")

      
#Leave Function
@bot.command(aliases=['l'])
async def leave(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients)
    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\nuse the join command to make me join!"
        )
    if (ctx.guild.voice_client):  #If in the VC
        await ctx.channel.send('Farewell!')
        await ctx.channel.send(
            'https://c.tenor.com/h240kSCuz2cAAAAS/hanako-yashiro.gif')
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.channel.send(
            "I'm not currently in a voice channel, use the join(!join) command to make me join!"
        )
  
#DM Function - Small Bug that the dm function can't take more than two people but that's fine 
@bot.command(pass_context=True, aliases=['message'])
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "I'm watching. :eye::eye:"
    await user.send(message)


#Play Function - Pain. #You can make a loop by just repeating NextSong[0] without poping it. Just make an aliases, loop
@bot.command(name='play', aliases=['p'], description="Use Ears")
async def play(ctx, *, query=None):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if (voice == None):
      await ctx.send("I'm in not currently in a VC!\nuse the join command to make me join!")
    
    else:  
      if (query == None and PauCalled == True):
        await ctx.send("Resuming...")
        voice.resume()
        PauseCalled()

      if(query == None):
        return
        await ctx.send('GOD IS GOOD, GOD IS GREAT!')
          
      else:
        def search(query):
          global info
          with YoutubeDL({'format': 'bestaudio'}) as ydl:
            try:
              requests.get(query)
            except:
              info = ydl.extract_info(f"ytsearch:{query}",
              download=False)['entries'][1]
            else:
              info = ydl.extract_info(query, download=False)
          return (info, info['formats'][0]['url'])
      
        video, source = search(query)
        nextSong.append(source)
        global FFMPEG_OPTS
        FFMPEG_OPTS = {
          'before_options':
          '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
          'options': '-vn'
        }
        
        songQueue.append(info['title'])
        songDuration.append(info['duration'])

        if not voice.is_playing() and PauCalled == False: #Current error, the code is a bit off time wise, despite using the same timer...
            await ctx.send(f"Now playing: **{info['title']}**")
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS), after=lambda e: print('Song played.', e))
        else:
            await ctx.send(f"**{info['title']}** is added to the queue!")
      for nSong in nextSong:
            while voice.is_playing():
                if(PauCalled == False):
                    await asyncio.sleep(1)
                    songDuration[0] = songDuration[0] - 1
                if(PauCalled == True): 
                    await asyncio.sleep(1)
                    songDuration[0] = songDuration[0]
                print(f'you doing Mr. Biggs? {songDuration[0]}')

            songQueue.pop(0)
            songDuration.pop(0)
            nextSong.pop(0)
            if len(nextSong) == 0:
                print("Chicken nugget")
                return
            else:
                voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS), after=lambda e: print('done', e))
                await ctx.send(f"Now playing: **{info['title']}**")

#Queue Function - Works
@bot.command(aliases=['q'])
async def queue(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients)
  
    if (voice == None):
        await ctx.send(
        "I'm in not currently in a VC!\nuse the join command to make me join!")
    await ctx.send('`Song List:`')

    def convert(secs):
        secs = secs % (24 * 3600)
        hours = secs // 3600
        secs %= 3600
        mins = secs // 60
        secs %= 60
        return "%02d:%02d:%02d" % (hours, mins, secs)

    for qNum, qTitle in enumerate(songQueue):
        if (qNum == 0):
            await ctx.send(
                f"`[{qNum + 1}] {qTitle} \n Duration: {convert(songDuration[qNum])}`"
            )
        else:
            await ctx.send(
                f"`[{qNum + 1}] {qTitle} \n Duration: {convert(songDuration[qNum])}`")

#Pause Function - Works
@bot.command()
async def pause(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  PauseCalled()
  if (voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")

  if voice.is_playing():
    voice.pause()

  elif (voice == None):
    await ctx.send(
    "I'm in not currently in a VC!\n use the join command to make me join!")
  else:
    await ctx.send("Currently no audio is playing.")
                   
#Skip Function - Works
@bot.command(aliases=['s'])
async def skip(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if (voice == None):
    await ctx.send("No music playing, bozo")

  if voice.is_playing():
    songQueue.pop(0)
    songDuration.pop(0)
    voice.stop()
    await ctx.send(f"Now playing: **{info['title']}**")
    await ctx.send(f"This is the length f{len(nextSong)}")
    nextSong.pop(0)
    voice.play(FFmpegPCMAudio(str(nextSong[0]), **FFMPEG_OPTS),after=lambda e: print('done', e))
  PauCalled == False

#Clear Function - Semi-Work
@bot.command()
async def clear(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if (voice == None):
        await ctx.send("I'm in not currently in a VC!\nuse the join command to make me join!")
    voice.stop()
    songDuration.clear()
    songQueue.clear()
    nextSong.clear()
    await ctx.send("**The Song List has been cleared all of the music**")

#Loop Function - In Progress
#@bot.command()
#async def loop(ctx):
#voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#if not voice.is_playing:

#songQueue.append(nextSong[0])
#voice.play(FFmpegPCMAudio(songQueue[0], **FFMPEG_OPTS),after=lambda e: print('done', e))

bot.run('ODc3NDIwMTc3MzU1MDYzMjk3.YRyXNw.O87yegqE0WeHVv-tZMdPEiaTfoo')

#bot.run(os.environ['RToken'])
#token = os.environ['RToken']
#bot.run(os.getenv("token"))

'''async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')+'''
'''Saved Embed example
Embed = discord.Embed(
    title = 'Your random doujin!',
    description = f'[:tada:**Your mysterious doujin!**:tada:](https://nhentai.net/g/{RandDoujin}/)'),
    color = discord.Color.from_rgb(101, 67, 33)
  )
  Embed.set_image(url="https://c.tenor.com/7fuoqpm9DtwAAAAd/please-dont-bully-me-anime.gif")

  await ctx.channel.send(embed = Embed)'''


#C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe -m pip install --upgrade pip