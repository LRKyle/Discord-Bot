import os
import discord
import random
import requests
import asyncio

from _thread import *
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands 
from youtube_dl import YoutubeDL
from urllib.request import Request, urlopen

# ~~~~ Current Bugs ~~~~
# NONE!
# Squidward partying!

# ~~~~ Possible Addons ~~~~
#1. Revamp the google function to get actual google stats
#2. Make a stocks command! #Possibly combine with the google command
#3. Spotify stats too if possible
#4. Make it so the queue countdowns
#5. Able to play playlists


def PauseCalled():
  global PauCalled
  if (PauCalled == True):
    PauCalled = False
  else:
    PauCalled = True

PauCalled = False

def LoopCalled():
  global LoCalled
  if (LoCalled == True):
    LoCalled = False
  else:
    LoCalled = True

LoCalled = False

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
                
        global FFMPEG_OPTS
        FFMPEG_OPTS = {
          'before_options':
          '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
          'options': '-vn'
        }
        nextSong.append(source)
        songQueue.append(info['title'])
        songDuration.append(info['duration'])


        if not voice.is_playing() and PauCalled == False: 
            await ctx.send(f"Now playing: **{info['title']}**")
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS), after=lambda e: print('Song played.', e))
        else:
            await ctx.send(f"**{info['title']}** is added to the queue!")
           
        for nSong in nextSong:
          while voice.is_playing():
            await asyncio.sleep(1)
            print('WUSAYANAME GIRLFRIEND')
            #Just needed to fill a line
          while LoCalled == True:
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS), after=lambda e: print('done', e))
            while voice.is_playing():
               print('WHAT IS YOUR NAME WHAT DO YOU BRING?')
               await asyncio.sleep(1)

          if len(nextSong) == 1:
            return

          else:
            songQueue.pop(0)
            songDuration.pop(0)
            nextSong.pop(0)
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS), after=lambda e: print('done', e))
            await ctx.send(f"Now playing: **{nextSong}**")

        
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
            await ctx.send(f"`[{qNum + 1}] {qTitle} \n Duration: {convert(songDuration[qNum])}`")

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
async def skip(ctx, *, amount = None):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if (voice == None):
    await ctx.send("No music is currently playing.")
    return

  if amount is None:
    voice.stop()

  if int(amount) <= len(nextSong):
      if amount == str:
          return
      nextSong.pop(int(amount) - 1)
      songQueue.pop(int(amount) - 1)
      voice.stop()

  else:
      await ctx.send('The amount exceeds the about of songs in queue.')
  PauCalled == False

#Clear Function
@bot.command()
async def clear(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if (voice == None):
        await ctx.send("I'm in not currently in a VC!\nuse the join command to make me join!")

    songQueue.clear()
    songDuration.clear()
    nextSong.clear()
    voice.stop()
    await ctx.send("**The Song List has been cleared all of the music**")
    PauCalled == False    

#Loop Function - In Progress #Just append the current song :skull:
@bot.command(aliases=['unloop'])
async def loop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if (voice == None):
        await ctx.send("I'm in not currently in a VC!\nuse the join command to make me join!")

    LoopCalled()
    await ctx.send(f"{info['title']} is being looped. Do the loop command again to disable the loop it.")

bot.run('YOUR TOKEN HERE')





#C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64\python.exe -m pip install --upgrade pip
