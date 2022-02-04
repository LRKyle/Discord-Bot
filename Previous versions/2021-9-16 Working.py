import os
import discord
import random
import requests
import asyncio


from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL

#Metal Cup Drink
client = discord.Client();
bot = commands.Bot(command_prefix='!', case_insensitive=True)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}


SplitResp = []
songQueue = []
numQueue = []

DoujinMax = 371497;
tagNum = 0;
num = 0
queueNum = len(songQueue)
NNum = 0
#a = NNum.array('d', [1.1, 3.5, 4.5])

RandRep = ["I'm doing great {message.author.nick}, How about you?", "I'm doing amazing! You?", "I'm doing decently, how are you? ", "I'm doing good :smile:, you? ", "I am just living life, How have have you been doing?"]

RandRepH = ["That's good to hear!", "That's nice to hear", "That's nice", "Ah, I'm happy to hear that!", "Damn, that's good"]

RandRepS =["Really? That hurts to hear", "That's sad", ":damn:", "hold that, bozo", "**Damn**"]


  
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
  if message.author == client.user:
    return

  #Responses
  msg = message.content
  RandRep = [f"I'm doing great {message.author.nick}, How about you?", "I'm doing amazing! You? {message.author.nick}", "I'm doing decently, how are you? ", "I'm doing good :smile:, you? ", "I am just living life, How have have you been doing?"]

  if msg.startswith('~How are'):
    RandRepR = random.randint(0, 4)
    await message.channel.send(RandRep[RandRepR]);
    
    if msg.startswith("I'm doing good") or msg.startswith("I'm good") or msg.startswith("I'm g") or msg.startswith('good'):
      RandRepR = random.randint(0, 4)
      await message.channel.send(RandRepH[RandRepR]);

    if msg.startswith("~I'm doing bad") or msg.startswith("!I'm bad") or msg.startswith("!I'm b") or msg.startswith('bad') or msg.startswith('Terrible') or msg.startswith('unlucky'):
      RandRepR = random.randint(0, 4)
      await message.channel.send(RandRepS[RandRepR]);

    if msg.startswith("~I miss "):
      await message.channel.send(":monkey:")

  if msg.startswith("top 1 sus"):
    await message.channel.send("Buggin, it's Joel")
  
  if msg.startswith("~Omori"):
    await message.author.send('Go play Omori bro')

  await bot.process_commands(message)

  

@bot.command(aliases=['doujinshi'])
async def doujin(ctx, arg):
  print("The user asked for doujin number " + arg + "\n")
  if int(arg) > DoujinMax:
    await ctx.channel.send('The number is too high! Redo the command!');

  if int(arg) < DoujinMax  :
    Embed = discord.Embed(
    title = 'Doujinshi Deliverer!',
    description = (f'[**Your doujin!**](https://nhentai.net/g/{arg}/)'),
    color = discord.Color.from_rgb(255, 0, 0))
    #Embed.set_image(url="https://c.tenor.com/7fuoqpm9DtwAAAAd/please-dont-bully-me-anime.gif")
    await ctx.channel.send(embed = Embed)

@bot.command(aliases=['RDoujin', 'random', 'randdoujin', 'rdoujinishi'])
async def rand(ctx):
  RandDoujin = random.randint(0,369677)
  print(f"The random doujin that the user got was {RandDoujin}")
  Embed = discord.Embed(
  title = 'Randomize Doujin!',
  description = f'[:tada:**Your mysterious doujin!**:tada:](https://nhentai.net/g/{RandDoujin}/)',
  color = discord.Color.from_rgb(101, 67, 33))
  Embed.set_image(url="https://c.tenor.com/7fuoqpm9DtwAAAAd/please-dont-bully-me-anime.gif")
  await ctx.channel.send(embed = Embed)

@bot.command(aliases = ['char', 'character'])
async def tag(ctx, *, arg):
    if ' ' in arg:
      SplitResp = arg.split(' ')
      JoinedResp = ('+'.join(SplitResp))
      await ctx.channel.send(f'The tag/character you searched for is!\nhttps://nhentai.net/search/?q={JoinedResp}')
    else:
      await ctx.channel.send(f'The tag/character you searched for is!\nhttps://nhentai.net/search/?q={arg}')

@bot.command()
async def google(ctx, *,arg):
    JoinedResp = arg
    if " " in arg:
      SplitResp = arg.split(' ')
      JoinedResp = ('+'.join(SplitResp))
    Embed = discord.Embed(
    title = 'Your Google Search',
    description = f'[**`Your search result!`**:mag_right:](https://www.google.com/search?q={JoinedResp}&ei=yAozYeGyIuyOwbkP34iDqAw&oq={JoinedResp}&gs_lcp=Cgdnd3Mtd2l6EAMyCgguELEDEEMQkwIyCwguELEDEMcBEKMCMggIABCABBCxAzIICC4QgAQQsQMyBQguEIAEMggIABCABBCxAzIICAAQgAQQsQMyCwguEIAEEMcBEK8BMggIABCABBCxAzIICAAQgAQQsQM6DggAEOoCELQCENkCEOUCOgcILhBDEJMCOgQIABBDOgQILhBDOhEILhCABBCxAxCDARDHARDRAzoOCC4QgAQQsQMQxwEQ0QM6EQguEIAEELEDEIMBEMcBEKMCOg4ILhCABBCxAxDHARCjAjoFCAAQgAQ6DQguEMcBENEDEEMQkwI6EAguELEDEIMBEMcBEKMCEEM6CgguELEDEIMBEEM6CAgAEIAEEMkDOgUIABCSAzoHCC4QsQMQQzoHCAAQsQMQQ0oECEEYAFDdyh9Y9dIfYOjUH2gBcAJ4AIABzwGIAZUHkgEFMi40LjGYAQCgAQGwAQjAAQE&sclient=gws-wiz&ved=0ahUKEwjhtqu60eTyAhVsRzABHV_EAMUQ4dUDCA4&uact=5)',
    color = discord.Color.from_rgb(27, 30, 35))
    await ctx.channel.send(embed = Embed)

#Join Function
@bot.command(aliases = ['j'])
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
    await ctx.channel.send("ayo? yo ass ain't in the voice channel")
    await ctx.channel.send("https://c.tenor.com/c6rLwFIEvDcAAAAC/touhou-b7touhou.gif")

#Leave Function
@bot.command(aliases = ['l'])
async def leave(ctx):
  if (ctx.guild.voice_client):#If in the VC 
    await ctx.channel.send('Farewell!');
    await ctx.channel.send('https://c.tenor.com/h240kSCuz2cAAAAS/hanako-yashiro.gif');
    await ctx.guild.voice_client.disconnect()
  else: 
    await ctx.channel.send("I'm not currently in a voice channel, use the join(!join) command to make me join!")

#DM Function
@bot.command(pass_context=True, aliases=['message'])
async def dm(ctx, user: discord.User, *, message=None):
  message = message or "I'm watching. :eye::eye:"
  await user.send(message)

def search(query):
  with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
    try: requests.get(query)
    except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    else: info = ydl.extract_info(query, download=False)
  return (info, info['formats'][0]['url'])

#Play Function
@bot.command(name='play', aliases=['sing','p'], description="Use Ears")
async def play(ctx, *, query):
  voice = get(bot.voice_clients, guild=ctx.guild)

  def search(query):
    global info
    global SNum 
    #Solves a problem I'll explain later
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
      try: requests.get(query)
      except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][1]
      else: info = ydl.extract_info(query, download=False)
    return (info, info['formats'][0]['url'])    
  search(query)

  FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',   'options': '-vn'}
  video, source = search(query)

  if(voice == None):
    await ctx.send("I'm in not currently in a VC!\nuse the join command to make me join!")


  if not voice.is_playing():
    await ctx.send(f"Now playing: {info['title']}")

    voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    songQueue.append(info['title'])

  else: 
    await ctx.send(f"{info['title']} is added to the queue!")
    songQueue.append(info['title'])
    await asyncio.sleep(info['duration'])

    print(f"\nNow playing:{info['title']}\n")
    ctx.send("Now playing: **{info['title']}**")

    voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    await ctx.send(f"Now playing: **{info['title']}**")


  
  NNum+1

#Queue Function
@bot.command(aliases = ['q'])
async def queue(ctx):
  global queueNum
  global NNum

  voice = discord.utils.get(ctx.bot.voice_clients)
  queueNum = len(songQueue)

  for NNum,SNum in enumerate(songQueue):
    await ctx.send(f"`[{NNum}] {SNum} \n`")

  if(voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")
    return

#Resume Function
@bot.command()
async def resume(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  elif(voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")
  else:
    await ctx.send("The audio is not paused.") 

#Skip Function
@bot.command(aliases = ['s'])
async def skip(ctx, *,  arg): 
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if int(arg) == 0:
    print('rip bozo')
    voice.stop(songQueue[num])
  if not arg:
    print('You really are dumb my nigga, where is the arg?')
  elif(voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")  
  else:
    songQueue.pop(int(arg))
    if(int(arg) > len(songQueue)):
      ctx.send("Fucc is wrong with you my nigga, damn")

#Pause Function
@bot.command()
async def pause(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  elif(voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")
  else:
    await ctx.send("Currently no audio is playing.")

#Clear Function
@bot.command()
async def clear(ctx):
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
  voice.stop()
  await ctx.send("I cleared all of the music")
  songQueue.clear()
  await ctx.send(len(songQueue))
  if(voice == None):
    await ctx.send("I'm in not currently in a VC!\n use the join command to make me join!")
  

bot.run(os.environ['token'])

#Stylize/rework everything to make it cute and shit


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
