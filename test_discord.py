from discord.ext import commands
from discord import embeds
import asyncio

token = 'ODE3NzM3NTM2MzEwNDc2ODIx.YEN3bQ.SXXDk7rw87AT_zDMmR1KleTrSy4'

bot=commands.Bot(command_prefix='!')

allowed=True
countdown=10
answered=False
answers={}
channels=['team-1','team-2']
@bot.command(name='start')
@commands.has_role('Test_QM')
async def trial(ctx):
    global allowed
    global countdown
    global answered
    global answers
    answers={}
    allowed=True
    answered = False
    message=await ctx.send(str(countdown))
    print(type(message))
    while countdown>1:
        if answered == True:
            allowed = False
            countdown = 10
            answered = False
            break
        await asyncio.sleep(0.9)
        await message.edit(content=str(countdown-1))
        countdown=countdown-1
    else:
        await ctx.send('TimeUp')
        allowed = False
        countdown = 10
        answered = False
        
@bot.command(name='ans')
async def answer(ctx):
    global allowed
    global answered
    global answers
    if allowed == True:
        answer=ctx.message.content[5:]
        answers[str(ctx.channel)]=answer
        await ctx.send(f"Seen. Your answer is {answer}")
        answered = True
    else:
        await ctx.message.reply('Pounce closed')

@bot.command(name='fetch')
@commands.has_role('Test_QM')
async def fetch_answers(ctx):
    global answers
    message=''
    for i in answers.keys():
        message=message+i+'        '+answers[i]+'\n'
    await ctx.send(message)
    
bot.run(token)
