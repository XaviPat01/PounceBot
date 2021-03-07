from discord.ext import commands
from discord import embeds
import discord
import asyncio
import requests
import time

#change token
token = 'ODE3NzQ3MjMwODM5Nzk5ODA4.YEOAdA.tBU1Hmr9tZkPsBSkFrmCNylpF8o'

bot = commands.Bot(command_prefix='!')

allowed = True
countdown = 0
answered = False
answers = {}

#----------------
# Function to get the channel ids of team text channels from the discord server

text_channel_dict={}
channel_ids=[]
@bot.command(name='new',help="Initialize the connections to the team channels")
@commands.has_role("Test_QM")
async def get_channel_ids(ctx):
    global text_channel_dict
    global channel_ids
    text_channel_dict = {}
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if 'team' in channel.name.lower():
                text_channel_dict[channel.name] = channel.id
    await ctx.send('Connections with teams established')
    # print(text_channel_dict.values())
    channel_ids = list(text_channel_dict.values())
    print(channel_ids)
#-----------------

qnset=[]
@bot.command(name="questions",help="To add the .txt file containing qns to be displayed on discord")
@commands.has_role("Test_QM")
async def qnreg(ctx):
    global qnset
    attachment_url = ctx.message.attachments[-1].url
    file_request = requests.get(attachment_url)
    contents=(file_request.text.split("\n"))
    await ctx.send("Qns registered")
    qnset=contents
    print(qnset)

    """ for i in range(0,len(contents)):
        qndisplay=f'Q{i+1}\n{contents[i]}'
        await ctx.send(qndisplay) """


@bot.command(name="show",help="To send the question to every team channel, !show [question number]")
@commands.has_role('Test_QM')
async def qnshow(ctx,qno):
    for id in channel_ids:
        await bot.get_channel(id).send(qnset[int(qno)-1])

#Function to start buzzer timer
        
@bot.command(name='start',help="Start the timer !start [time(in seconds)]")
@commands.has_role('Test_QM')
async def trial(ctx, arg):
    global allowed
    global countdown
    global answered
    global answers
    answers = {}
    allowed = True
    answered = False
    countdown = int(arg)
    t1 = time.time()

    messages =[]
    for id in channel_ids:
        messages.append(await bot.get_channel(id).send(min([(countdown//5+1)*5,int(arg)])))     #Time left will decrease by intervals of 5
    #message = await bot.get_channel(817940087206707240).send(countdown)
    #print(type(message))
    while countdown > 1:
        countdown = int(arg) - (time.time() - t1)
        print(countdown, answered, allowed)
        if answered == True:
            allowed = False
            countdown = int(arg)
            answered = False
            print("Answer received.")
            await ctx.send("Buzzer closed. A team has answered. Enter !fetch")
            break
        else:
            for message in messages:
                await message.edit(content=(int(countdown)//5+1)*5)
    else:
        for message in messages:
            await message.edit(content='TimeUp')
        await ctx.send("Time's Up!")
        allowed = False
        countdown = int(arg)
        answered = False

#Function using which teams can send their answer

@bot.command(name='ans', help="Write your answer by mentioning !ans and then your answer")
async def answer(ctx):
    global allowed
    global answered
    global answers
    if allowed == True:
        answer = ctx.message.content[5:]
        answers[str(ctx.channel)] = answer
        await ctx.send(f"Seen. Your answer is {answer}")
        answered = True
    else:
        await ctx.message.reply('Buzzer closed')


@bot.command(name='fetch', help="To see the answer of the team who buzzed first")
@commands.has_role('Test_QM')
async def fetch_answers(ctx):
    global answers
    message = ''
    for i in answers.keys():
        message = message + i + '        ' + answers[i] + '\n'
    if message == '':
        await ctx.send("No team answered")
    else:
        await ctx.send(message)


bot.run(token)


