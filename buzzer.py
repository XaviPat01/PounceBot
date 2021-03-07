from discord.ext import commands
from discord import embeds
import asyncio
#change token
token = 'ODE3NzQwMjEyMzQ4MTI1Mjc0.YEN56w.GbX1VzaBWZo-KkoDnBsdRlDXGLg'

bot = commands.Bot(command_prefix='!')

allowed = True
countdown = 0
answered = False
answers = {}
#manual input of ids
channels = ['team-1', 'team-2']
channel_ids = [817940087206707240, 817940251623555142]


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
    messages =[]
    for id in channel_ids:
        messages.append(await bot.get_channel(id).send(countdown))
    #message = await bot.get_channel(817940087206707240).send(countdown)
    #print(type(message))
    while countdown > 1:
        print(countdown, answered, allowed)
        if answered == True:
            allowed = False
            countdown = int(arg)
            answered = False
            print("Answer received.")
            break
        else:
            await asyncio.sleep(0.9)
            countdown -= 1
            for message in messages:
                await message.edit(content=countdown)
    else:
        for id in channel_ids:
            await bot.get_channel(id).send('TimeUp')
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
        await ctx.send("No team pounced")
    else:
        await ctx.send(message)


bot.run(token)

