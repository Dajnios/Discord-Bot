#Imports 

import discord
from discord.ext import commands
import datetime
import pytz
import openai

#Assigning a character to a command call
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#OpenAI Key
openai.api_key = "your OpenAI key"

#Start information
@client.event
async def on_ready():
    print('Online')
    print(client.user.name)

#Poll
@client.command()
async def poll(ctx,choice1,choice2,*,topic,):
    embed = discord.Embed(title= topic, description=f":one: {choice1}\n\n:two: {choice2}",)
    embed.set_footer(text="Created by your bot name")
    message = await ctx.send(embed = embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await ctx.message.delete()

#Time when user joins server
@client.command()
async def time(ctx):
    member = ctx.guild.get_member(ctx.message.author.id)
    joined_at = member.joined_at.astimezone(pytz.utc)
    now = datetime.datetime.now(pytz.utc)
    time_on_server = now - joined_at
    days = time_on_server.days
    await ctx.send(f'{member.name} spend {days} days on this server.')

#Activity
@client.command()
async def time2(ctx):
    member = ctx.guild.get_member(ctx.message.author.id)
    last_activity = member.activity
    if last_activity is not None:
        now = datetime.datetime.utcnow()
        time_online = now - last_activity
        seconds = time_online.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24
        await ctx.send(f'{member.name} spend {days} days, {hours % 24} hours and {minutes % 60} minutes online.')
    else:
        await ctx.send(f'{member.name} there is currently no activity on the server..')

#Status
@client.command()
async def time3(ctx, nickname: str):
    member = discord.utils.get(ctx.guild.members, name=nickname)
    if member is None:
        await ctx.send(f'User with nickname not found. {nickname}.')
    else:
        last_online = member.raw_status
        if last_online == "online":
            await ctx.send(f'{member.name} is currently online.')
        elif last_online == "offline":
            await ctx.send(f'{member.name} is offline and it is not possible to calculate the time they spent online since the last login..')
        elif last_online is not None:
            last_activity = datetime.datetime.strptime(last_online, "%Y-%m-%dT%H:%M:%S.%f%z")
            now = datetime.datetime.utcnow()
            time_online = now - last_activity
            seconds = time_online.total_seconds()
            minutes = seconds // 60
            hours = minutes // 60
            days = hours // 24
            await ctx.send(f'{member.name} spend {days} days, {hours % 24} hours and {minutes % 60} minutes online.')
        else:
            await ctx.send(f'{member.name} has not been seen on the server recently.')

#OpenAI
@client.command()
async def ai(ctx, *, input_text):
    if ctx.author == client.user:
        return

    response = openai.Completion.create(engine="text-davinci-002", prompt=input_text, max_tokens=1500#you can change that if you want)

    await ctx.send(response.choices[0].text)

#OP.GG
@client.command()
async def opgg(ctx,*summonerNames):
    names = ', '.join(summonerNames)
    url = f'https://op.gg/summoners/eune/{names}'
    return await ctx.send(url)

#Connection using a Discord token
client.run("Your Discord bot token")
