import discord
import random


TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.tmK7z05SOsTLSJ3hiY485EZs4Hs"


client = discord.Client()

@client.event
async def on_ready():
    print ("We have logged in as {0.user}".format(client))

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