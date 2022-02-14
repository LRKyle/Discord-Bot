import os
import discord
import random
import requests
import asyncio

from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL

#Current Bugs
#When you use the pause function, it pauses the song but not the song timer. This can be fixed by pausing it too
#Create the loop function
#Make resume function obsetele make it so you can resume the song by using the play function


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
        f"I'm doing great {message.author.nick}, How about you?",
        "I'm doing amazing! You? {message.author.nick}",
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

    if msg.startswith("top 1 sus") or msg.startswith("Top 1"):
        await message.channel.send("Buggin, it's Joel")

    if msg.startswith("~Omori"):
        await message.author.send('Go play Omori bro')

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
        await ctx.channel.send("ayo? yo ass ain't in the voice channel")
        await ctx.channel.send(
            "https://c.tenor.com/c6rLwFIEvDcAAAAC/touhou-b7touhou.gif")


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


#DM Function
@bot.command(pass_context=True, aliases=['message'])
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "I'm watching. :eye::eye:"
    await user.send(message)


#Play Function
@bot.command(name='play', aliases=['p'], description="Use Ears")
async def play(ctx, *, query):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\nuse the join command to make me join!"
        )

    #Normal Play Function
    if not 'https://www.youtube.com/playlist?list=' in query:

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

        if not voice.is_playing():
            await ctx.send(f"Now playing: **{info['title']}**")
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS),
                       after=lambda e: print('done', e))
            songQueue.append(info['title'])
            songDuration.append(info['duration'])

            while not songDuration[0] == 0:
                await asyncio.sleep(1)
                songDuration[0] = songDuration[0] - 1

        else:
            await ctx.send(f"**{info['title']}** is added to the queue!")
            songQueue.append(info['title'])
            songDuration.append(info['duration'])
            await asyncio.sleep(songDuration[0])
            songQueue.pop(0)
            songDuration.pop(0)
            voice.play(FFmpegPCMAudio(nextSong[0], **FFMPEG_OPTS),
                       after=lambda e: print('done', e))
            await ctx.send(f"Now playing: **{info['title']}**")

    #Playlist Play Function
    if 'https://www.youtube.com/playlist?list=' in query:

        def search(query):
            global info
            global source
            with YoutubeDL({'format': 'bestaudio'}) as ydl:
                try:
                    requests.get(query)
                    print("The first")
                except:
                    info = ydl.extract_info(f"ytsearch:{query}",
                                            download=False)['entries'][1]
                else:
                    info = ydl.extract_info(query, download=False)
            return (info, info['entries'][0]["formats"][0]['url'])

        video, source = search(query)

        if 'entries' in nextPlaylistSong:
            for i in nextPlaylistSong['entries']:
                URL = i['formats'][0]['url']
                nextSong.append(URL)
                await ctx.send(f"Now playing: **{i['title']}** ")
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                songQueue.append(i['title'])
                songDuration.append(i['duration'])

                while not songDuration[0] == 0:
                    await asyncio.sleep(1)
                    songDuration[0] = songDuration[0] - 1

            #await ctx.send('**Note:** The playlist songs will show up in the queue has they are being played. This means you are able to play a song in the middle of the playlist.')


#Queue Function - Semi Work
@bot.command(aliases=['q'])
async def queue(ctx):
    voice = discord.utils.get(ctx.bot.voice_clients)
    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\nuse the join command to make me join!"
        )
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
                f"`[{qNum + 1}] {qTitle} \n Duration: {convert(songDuration[qNum])}`"
            )


#Resume Function - Works
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\nuse the join command to make me join!"
        )
    if voice.is_paused():
        voice.resume()
    elif (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\n use the join command to make me join!"
        )
    else:
        await ctx.send("The audio is not paused.")


#Pause Function - Works Bug: If you pause and play another song, the song will override the previous one in additon to messing up the queue.
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\n use the join command to make me join!"
        )

    if voice.is_playing():
        voice.pause()
    elif (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\n use the join command to make me join!"
        )
    else:
        await ctx.send("Currently no audio is playing.")


#Loop Function - In Progress
#@bot.command()
#async def loop(ctx):
#voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#if not voice.is_playing:

#songQueue.append(nextSong[0])
#voice.play(FFmpegPCMAudio(songQueue[0], **FFMPEG_OPTS),
#after=lambda e: print('done', e))


#Skip Function - Work
@bot.command(aliases=['s'])
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if (voice == None):
        await ctx.send("No music playing, bozo")

    if voice.is_playing():
        await ctx.send("elmo")
        songQueue.pop(0)
        songDuration.pop(0)
        voice.stop()
        await ctx.send(f"Now playing: **{info['title']}**")
        await ctx.send(f"This is the length f{len(nextSong)}")
        nextSong.pop(0)
        voice.play(FFmpegPCMAudio(str(nextSong[0]), **FFMPEG_OPTS),
                   after=lambda e: print('done', e))


#Clear Function - Work
@bot.command()
async def clear(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if (voice == None):
        await ctx.send(
            "I'm in not currently in a VC!\nuse the join command to make me join!"
        )

    voice.stop()
    songDuration.clear()
    songQueue.clear()
    await ctx.send("**The Song List has been cleared all of the music**")


bot.run(os.environ['token'])

