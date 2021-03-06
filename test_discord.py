from discord.ext import commands
import asyncio

token = 'ODE3NzM3NTM2MzEwNDc2ODIx.YEN3bQ.SXXDk7rw87AT_zDMmR1KleTrSy4'

bot=commands.Bot(command_prefix='!')

""" @client.event
async def on_message(message):
    channels=['nik_test']
    if str(message.channel) in channels:
        if message.content.find('!try') != -1:
            countdown=10
            
            timer.content=str(countdown)
            await message.channel.send(timer)
            

 """
allowed=True
countdown=10
answered=False
@bot.command(name='try')
async def trial(ctx):
    global allowed
    global countdown
    global answered
    allowed=True
    answered = False
    message=await ctx.send(str(countdown))
    while countdown>1:
        if answered == True:
            allowed = False
            countdown = 10
            answered = False
            break
        await asyncio.sleep(1)
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
    if allowed == True:
        answer=ctx.message.content[5:]
        await ctx.send(f"seen. your answer is {answer}")
        answered = True
    else:
        await ctx.send('Answer closed')


bot.run(token)
