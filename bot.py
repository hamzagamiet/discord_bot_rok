import discord
import random
from discord_buttons_plugin import *
from discord.ext import commands


TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.tmK7z05SOsTLSJ3hiY485EZs4Hs"

bot = commands.Bot(command_prefix = "!")
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
    print ("{0.user} is online".format(bot))

@bot.command()
async def comm(ctx):
    info = discord.Embed(title=f"Talent Tree", description="Click the arrows to see different talent tree builds")
    await buttons.send(
        embed = info,
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "<",
                    style = ButtonType().Primary,
                    custom_id = "left"
                ),
                Button(
                    label = ">",
                    style = ButtonType().Primary,
                    custom_id = "right"
                )
            ])
        ]
    )


@bot.event
async def on_message(message):
    print ("message")
    await bot.process_commands(message)
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    #if message author is the bot itself, don't reply
    if message.author == bot.user:
        return

    #replies to general chat
    if message.channel.name == "general":
        if user_message.lower() == "hello":
            print("say hello")
            await message.channel.send(f"hello {username}!")
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f"see you later {username}!")
            return
        elif user_message.lower() == "!random":
            response = f"your random number is {random.randrange(1000000)}!"
            await message.channel.send(response)
            return


bot.run(TOKEN)