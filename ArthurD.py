import os
import discord
import random
from discord.ext import commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv
from contextlib import contextmanager
import shutil
import asyncio

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# check the .env file for the token of our bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#set the prefix for commands such as "play", "join", "leave" etc.
BOT_PREFIX = '#'

bot = commands.Bot(command_prefix=BOT_PREFIX)

# initiating the bot
@bot.event
async def on_ready():
    print(f'{bot.user.name} has come for the good sauce!')

# for the given aliases, let the bot join to the voice channel the user is currently in
@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Joined {channel}")

    await ctx.send(f"{bot.user.name} has found the good sauce!")

# for the given aliases, let the bot leave to the voice channel the user is currently in
@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Left {channel}")
        await ctx.send(f"{bot.user.name} consumed the good sauce and left!")
    else:
        print(f"I am not in a voice channel!")
        await ctx.send(f"{bot.user.name} couldn't consume the good sauce because there was non!")

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def queue_checker():
        queue = os.path.isdir("./queue_folder")
        if queue is True:
            DIR = os.path.abspath(os.path.realpath("queue_folder"))
            queue_length = len(os.listdir(DIR))
            still_queue = queue_length - 1
            try:
                first_file = os.listdir(DIR) [0]
            except:
                print("No more songs in queue.\n")
                song_queue.clear()
                return
            main_loc = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("queue_folder") + "\\" + first_file)
            if queue_length != 0:
                print(f"Song finished, playing next in queue.\n")
                print(f"Queue length: {still_queue}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_loc)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: queue_checker())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                song_queue.clear()
                return
        else:
            song_queue.clear()
            print("No song was queued before the current one ended playing.\n")

    song_check = os.path.isfile("song.mp3")
    try:
        if song_check:
            os.remove("song.mp3")
            song_queue.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to remove the song file, but it is currently being played.")
        await ctx.send("A song is currently playing, use the '"  + BOT_PREFIX + "stop' command, then try again.")
        return

    queue = os.path.isdir("./queue_folder")
    try:
        qfolder = "./queue_folder"
        if queue is True:
            print("Old queue folder is removed.")
            shutil.rmtree(qfolder)
    except :
        print("There is no old queue folder.")

    await ctx.send("Fetchin' that tune for you feller!")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading the song now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"The file has been renamed to {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: queue_checker())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    new_name = name.rsplit("-", 2)
    await ctx.send(f"Playing: {new_name}")
    print("playing\n")

@bot.command(pass_context=True, aliases=['hb', 'headban'])
async def headbang(ctx):
    with cd("~/Documents/ArthurD/png_gif"):
        await ctx.send(file=discord.File('hbc.gif'))

@bot.command(pass_context=True, aliases=['25', 'colorad'])
async def colorado(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("The bastards hung me in the spring of twenty-five, but I am still alive...")
        voice.play(discord.FFmpegPCMAudio("highwayman.mp3"), after=lambda e: print(f"Aniki has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await asyncio.sleep(220)
        await message.delete()

@bot.command(pass_context=True, aliases=['ani', 'anik'])
async def aniki(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("Hold on there, feller! You have been blessed by the Aniki!")
        voice.play(discord.FFmpegPCMAudio("aniki.mp3"), after=lambda e: print(f"Aniki has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await asyncio.sleep(263)
        await message.delete()

@bot.command(pass_context=True, aliases=['nab', 'nabe'])
async def naber(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("Hey, naber?")
        voice.play(discord.FFmpegPCMAudio("hey_naber.mp3"), after=lambda e: print(f"Howdy has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await asyncio.sleep(2)
        await message.delete()

@bot.command(pass_context=True, aliases=['ay', 'ayli'])
async def zawarudo(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("Durdurun dünyayı inecek var!")
        voice.play(discord.FFmpegPCMAudio("za_warudo.mp3"), after=lambda e: print(f"Za Warudo has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.15
        await asyncio.sleep(4)
        await message.delete()

@bot.command(pass_context=True, aliases=['le', 'lenn'])
async def lenny(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("HAHAAAAAA FOUND YOU, LENNY!")
        voice.play(discord.FFmpegPCMAudio("lenny.mp3"), after=lambda e: print(f"Lenny has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.27
        await asyncio.sleep(3)
        await message.delete()

@bot.command(pass_context=True, aliases=['cen', 'cena'])
async def cenap(ctx):
    with cd("~/Documents/ArthurD/predefined_songs"):
        voice = get(bot.voice_clients, guild=ctx.guild)
        message = await ctx.send("barıt qoxulu o yollar, o yollar, \nseni bes ne vaxt qaytarar, qaytarar. \nsenden teselli, bir zabit mündiri, \nbir cüt ulduzlu, aylı paqonlar. \n\nhay ver mene cenab leytenant, \nhay ver mene leytenant. \nxoş müjdeli bir savaşdan, \npay ver mene leytenant, \n\no gün gelecek qem yeme, qem yeme. \no, vaxt dönecem men sene, men sene. \nhele yad eldedi yurdumuz-yuvamız , \nbitib tükenmeyib o, qan davamız. \n\nhay ver mene cenab leytenant, \nhay ver mene leytenant. \nxoş müjdeli bir savaşdan, \npay ver mene leytenant, \n\nqisas, son qisas, yetmeyib, yetmeyib, \nsavaş, son savash, bitmeyib, bitmeyib. \nsenger yanındakı çaxdığın ocağın, \nodun henirtisi hele keçmeyib. \n\nhay ver mene cenab leytenant, \nhay ver mene leytenant.\nxoş müjdeli bir savaşdan, \npay ver mene leytenant.")
        voice.play(discord.FFmpegPCMAudio("cenap_leytenant.mp3"), after=lambda e: print(f"Cenap Leytenant has finished playing."))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await asyncio.sleep(297)
        await message.delete()

@bot.command(pass_context=True, aliases=['pa', 'paus'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print(f"Music paused.")
        voice.pause()
        message = await ctx.send(f"Feller paused the tune!")
        await asyncio.sleep(10)
        await message.delete()
    else:
        print(f"There is no music to pause.")
        message = await ctx.send(f"There is no tune to pause, feller!")
        await asyncio.sleep(10)
        await message.delete()

@bot.command(pass_context=True, aliases=['re', 'resu'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print(f"Music is already playing.")
        message = await ctx.send(f"Don\'t you hear the tune, feller?")
        await asyncio.sleep(10)
        await message.delete()
    else:
        print(f"Music is resumed.")
        voice.resume()
        message = await ctx.send(f"Here you go, feller!")
        await asyncio.sleep(10)
        await message.delete()

@bot.command(pass_context=True, aliases=['st', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    song_queue.clear()
    if voice and voice.is_playing():
        print(f"Music is stopped.")
        voice.stop()
        message = await ctx.send(f"Feller stopped the tune!")
        await asyncio.sleep(10)
        await message.delete()
    else:
        print(f"There is no music to stop.")
        message = await ctx.send(f"There is no tune to stop, feller!")
        await asyncio.sleep(10)
        await message.delete()

song_queue = {}

@bot.command(pass_context=True, aliases=['qu', 'queu'])
async def queue(ctx, url: str):
    queue = os.path.isdir("./queue_folder")
    if queue is False:
        os.mkdir("queue_folder")
    DIR = os.path.abspath(os.path.realpath("queue_folder"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in song_queue:
            q_num += 1
        else:
            add_queue = False
            song_queue[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("queue_folder") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'quiet': True,
        'outtmpl': queue_path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading the song now\n")
        ydl.download([url])
    await ctx.send("Adding to the queue.")
    print("Song added to the queue.")

@bot.command(pass_context=True, aliases=['iasip'])
async def alwaysunny(ctx):

    iasip_quotes = [
        'I’m the trash man!',
        'I immersed myself in the culture. Tasting the cuisine. But mostly doing cocaine.',
        'I don’t wanna be his friend, I wanna shoot him in the face.',
        'I’m not an executioner. I’m the best goddamn bird lawyer in the world.',
        'I drank three bottles of champagne and hung out with a stray dog all night under a bridge.',
        'Science is a liar sometimes.',
        'Fight milk! The first alcoholic dairy-based protein drink for bodyguards!',
        'I am the golden god.',
        'I’ll give ya fifty bucks if you drink soup outta my shoe. And take your top off.',
        'He got it from a gay guy in the 80s',
    ]

    response = random.choice(iasip_quotes)
    message = await ctx.send(response)
    await asyncio.sleep(10)
    await message.delete()

bot.run(TOKEN)
