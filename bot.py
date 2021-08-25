import discord
import random
from discord_components import *
from discord.ext import commands


TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.tmK7z05SOsTLSJ3hiY485EZs4Hs"

bot = commands.Bot(command_prefix= ="!")

client = discord.Client()

@client.event
async def on_ready():
    DiscordComponents(bot)
    print ("{0.user} is online".format(client))

@bot.command()
async def commanders(ctx):
    info = discord.Embed(title=f"Talent Tree", description="Click the arrows to see different talent tree builds")
    await ctx.send(
        embed = info
        components = [
            Button(style=1, label="<"),
            Button(style = 1, label=">")
            ]
    )
    try:
        res = await bot.wait_for("button click", check = check)
        left_or_right = res.component.label

        if left_or_right == "<":
            await message.channel.send(f"Left")
        if left_or_right == "<":
            await message.channel.send(f"Right")

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    #if message author is the bot itself, don't reply
    if message.author == client.user:
        return

    #replies to general chat
    if message.channel.name == "general":
        if user_message.lower() == "hello":
            await message.channel.send(f"hello {username}!")
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f"see you later {username}!")
            return
        elif user_message.lower() == "!random":
            response = f"your random number is {random.randrange(1000000)}!"
            await message.channel.send(response)
            return


client.run(TOKEN)