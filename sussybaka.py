### sussy baka discord bot ###

#for command stock
import numpy
import pandas
import yfinance
from prettytable import PrettyTable
import asyncio

#for multiple commands
import random
import time
import cleverbotfree

#for bot functionality
import os
from os import path
import discord
from discord.ext.commands import Bot
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = Bot(command_prefix='baka ')

### COMMANDS ###

#bot info v.0.1
@bot.command(name='info',
             description="gives ur lil sussy baka ass the information",
             help="gives ur lil sussy baka ass the information"
             )
async def getInfo(context):
    await context.send('sussy baka bot v. 0.2.0\ni love you')

#bot yes/no v.0.1
@bot.command(name='yes/no',
             description="ask sussy baka bot a yes/no question",
             brief="ask sussy baka bot a yes/no question",
             aliases=['y/n', '8ball']
             )
async def ynQuestion(context):
    f = open("./etc/ynqResponse.txt","r")
    responses = f.read().split("','")
    f.close()
    await context.send(context.message.author.mention + " " + random.choice(responses))

#bot talk
@bot.command(name='conversation',
             description="have the bot talk to you",
             brief="have the bot talk to your depressed, lonely, female-deprived life",
             aliases=['talk', 'imlonely', 'chat']
             )
@commands.cooldown(1,120,commands.BucketType.default)
async def chat(context):           
    async with cleverbotfree.async_playwright() as p_w:
        c_b = await cleverbotfree.CleverbotAsync(p_w)
        await context.send("hello baka")
        while True:
            try:
                msg = await bot.wait_for('message', check=lambda message: message.author == context.author, timeout=30) # 30 seconds to reply
                user_input = msg.content
            except:
                await context.send("reply faster baka, i'm leaving")
                break
            
            if user_input == 'quit':
                await context.send("fuck you too, baka.")
                break
            
            response = await c_b.single_exchange(user_input)
            try:
                await context.send(response)
            except:
                await context.send("i didn't understand what you said, baka. try again.")
        await c_b.browser.close()
@chat.error
async def chat_error(context,error):
    if isinstance(error, commands.CommandOnCooldown):
        await context.send('I\'m have recently had a conversation... ask me to talk again in {:.2f}s.'.format(error.retry_after))
        
#bot say v.0.1
#bot says something. soundboard ig?
@bot.command(name='say',
             description="the bot says something. baka say \"[arg]\"",
             brief="bot says smth. baka say \"baka\" for example",
             )
@commands.cooldown(1,60,commands.BucketType.user)
async def botSay(context, arg):
    try:
        cn = context.author.voice.channel
    except:
        await context.send("you're not in a voice channel, little baka.")
        return
    
    sound = arg.lower()
    source = f"./audio/{sound}.mp3"
    vc = await cn.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source=source))
    while vc.is_playing():
       await asyncio.sleep(1)
    vc.stop()
    await vc.disconnect()
    
@botSay.error
async def botSay_error(context,error):
    if isinstance(error, commands.CommandOnCooldown):
        await context.send('I\'m tired baka... ask me to talk again in {:.2f}s.'.format(error.retry_after))

#bot genshinsim v.0.1
#barebones genshin gacha roll, no pity functionality yet.
@bot.command(name='genshinRoll',
             description="simulates a genshin roll. baka gRoll [char/weapon]",
             help = "simulates a genshin roll you gacha-addicted mongrel",
             aliases=['gRoll','genshin']
             )
@commands.cooldown(1, 5, commands.BucketType.user)
async def genshinRoll(context, arg):
    if arg == "char" or arg == "character" or arg == "c":
        probTable = [6, 26, 25, 943]
        rollTable = ["5starC", "4starC", "4starW", "3star"]
        result = random.choices(rollTable, weights = probTable, k = 1)
        for r in result:
            
            f = open(f"./gData/g{r}.txt","r")
            responses = f.read().split(",")
            f.close()
            
            await context.send("Congratulations, " + context.message.author.mention + ". You got a " + random.choice(responses) + ".")
    elif arg == "weapon" or arg == "w":
        probTable = [7, 30, 30, 933]
        rollTable = ["5starW", "4starC", "4starW", "3star"]
        result = random.choices(rollTable, weights = probTable, k = 1)
        for r in result:
            
            f = open(f"./gData/g{r}.txt","r")
            responses = f.read().split(",")
            f.close()
            
            await context.send("Congratulations, " + context.message.author.mention + ". You got a " + random.choice(responses) + ".")
    else:
        await context.send("you little baka, " + arg + " is not a valid roll type. type in baka gRoll c or something u little baka.")
@genshinRoll.error #prevent command spam
async def genshinRoll_error(context,error):
    if isinstance(error, commands.CommandOnCooldown):
        await context.send('Baka... you can\'t roll again for {:.2f}s.'.format(error.retry_after))

#bot stock info v.0.2.1
#formatting change
@bot.command(name='stock',
             description="ask sussy baka bot the price of a stock. make sure to input the ticker symbol.",
             brief="ask sussy baka bot about stocks. e.g.: baka stock [ticker name]",
             aliases=['stockprice','stocks'],
             )
async def stockPrice(context, arg):
    
    data = yfinance.download(tickers=arg, period='1d', interval='1d') #downloads data over interval of 1d

    if data.size == 0: #does stock exist? yfinance returns no data if stock doesn't exist.
        await context.send("what the fuck baka put in a real stock jeez")
        return
    else:
        table = PrettyTable(["Open", "High", "Low", "Close", "Adj. Close", "Volume"])
        body = []
        for val in data.iloc[0]:
            body.append(str(round(val,2)))

        table.add_row(body)
        
        await context.send("here's the price of " + arg + " stock my little pogchamp\nretrieval time: " + str(data.index[0]) + "\n`" + table.get_string() + "`")




### EVENTS ###

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    await bot.change_presence(activity = discord.Game('ara ara my little pogchamp'))
    
    print(
        f'{bot.user} is connected to:\n'
        f'{guild.name}(id: {guild.id})'
        )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'among us' in message.content.lower():
        await message.channel.send('Among us? Why don\'t you get among some bitches?')

    await bot.process_commands(message)


bot.run(TOKEN)
