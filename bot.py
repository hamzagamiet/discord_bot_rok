import discord
import random
from discord_buttons_plugin import *
from discord.ext import commands
from dictionaries import commanders


TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.tmK7z05SOsTLSJ3hiY485EZs4Hs"

bot = commands.Bot(command_prefix = "!")
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
    print ("{0.user} is online".format(bot))

@bot.command()
async def Com(ctx):
    message_split = str(ctx.message.content).split("Com")[1].split()
    message = " ".join(message_split)
    
    print(f"Search: {message}")
    for name in commanders:
        print (f"Checking against: {name}")

        for search in commanders[name]['search']:
            if message.lower() == search.lower():
                print (f"Match found: {name}")

                # pairings = ""
                # for pair in commanders[name]['pairings']:
                #     pairings += pair + "\n"

                print_roles = "/ ".join(commanders[name]['roles']).title()
                roles_list = [role for role in commanders[name]['roles']]

                pairings = ""
                for pair in commanders[name]['roles'][roles_list[0]]['pairings']:
                    pairings += pair+"\n"


                info = discord.Embed(
                    title=f"{name} | {commanders[name]['title']}\n",
                    description= 
                    f"{commanders[name]['skills'][0]} | {commanders[name]['skills'][1]} | {commanders[name]['skills'][2]} \n\n"
                    f"**Rarity:** {commanders[name]['rarity']}\n**Troop Type:** {commanders[name]['type']}\n**Roles:** {print_roles}"
                    f"\n\n**Recommended Pairings:**\n{pairings}"
                    f"\n**Statistics:**\n"
                    f"Attack: +{commanders[name]['roles'][roles_list[0]]['attack']}\n"
                    f"Defence: +{commanders[name]['roles'][roles_list[0]]['defence']}\n"
                    f"Health: +{commanders[name]['roles'][roles_list[0]]['health']}\n"
                    f"March Speed: +{commanders[name]['roles'][roles_list[0]]['march speed']}\n"
                    f"\n**Talent Tree:**\n{commanders[name]['roles'][roles_list[0]]['build']}"
                    f"\nUse the buttons to navigate the information for {name}. All credits for this bot go to HAMZA#9000")
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