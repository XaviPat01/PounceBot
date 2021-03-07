from discord.ext import commands
from discord import embeds
import asyncio
import time

#change token
token = 'ODE3NzQwMjEyMzQ4MTI1Mjc0.YEN56w.GbX1VzaBWZo-KkoDnBsdRlDXGLg'

bot = commands.Bot(command_prefix='!')

allowed = True
countdown = 0
answered = False
answers = {}

#----------------
text_channel_dict={}
channel_ids=[]
@bot.command(name='new')
async def get_channel_ids(ctx):
    global text_channel_dict
    global channel_ids
    text_channel_dict = {}
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if 'team' in channel.name.lower():
                text_channel_dict[channel.name] = channel.id
    print(text_channel_dict.values())
    channel_ids = text_channel_dict.values()
#-----------------


@bot.command(name='start')
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
        messages.append(await bot.get_channel(id).send(min([(countdown//5+1)*5,int(arg)])))
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
            break
        else:
            for message in messages:
                await message.edit(content=(int(countdown)//5+1)*5)
    else:
        for message in messages:
            await message.edit(content='TimeUp')
        allowed = False
        countdown = int(arg)
        answered = False


@bot.command(name='ans', help="Write your pounce answer by mentioning !ans and then your answer")
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


@bot.command(name='fetch', help="To see the pounce answers of each team.")
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


