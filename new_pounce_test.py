from discord.ext import commands
import asyncio
import time

#change token
token = 'ODE3NzM3NTM2MzEwNDc2ODIx.YEN3bQ.SXXDk7rw87AT_zDMmR1KleTrSy4'
bot = commands.Bot(command_prefix='!')

allowed = [False,False]
answered = [False,False]
countdown = 0
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
    allowed = [True,True]
    answered = [False,False]
    countdown = int(arg)
    t1 = time.time()
    messages =[]
    for id in channel_ids:
        messages.append(await bot.get_channel(id).send(min([(countdown//5+1)*5,int(arg)])))
    count_1=0
    count_2=0
    while countdown > 1:
        countdown = int(arg) - (time.time() - t1)

        if answered[0] == True and count_1==0:
            allowed[0] = False
            countdown = int(arg)
            count_1=1
        if answered[1] == True and count_2==0:
            allowed[1] = False
            countdown = int(arg)
            count_2=1
            
        else:
            for message in messages:
                await message.edit(content=(int(countdown)//5+1)*5)
    else:
        for message in messages:
            await message.edit(content='TimeUp')
        allowed = [False,False]
        countdown = int(arg)
        answered = [False,False]

@bot.command(name='ans', help="Write your pounce answer by mentioning !ans and then your answer")
async def answer(ctx):
    global allowed
    global answered
    global answers
    index=channel_ids.index(ctx.channel.id)
    if allowed[index] == True:
        answer = ctx.message.content[5:]
        answers[str(ctx.channel)] = answer
        await ctx.send(f"Seen. Your answer is {answer}")
        answered[index] = True
        allowed[index] = False
    else:
        await ctx.message.reply('Pounce closed')

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
