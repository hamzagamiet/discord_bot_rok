import discord
import random
from discord_buttons_plugin import *
from discord.ext import commands
from dictionaries import commanders
from datetime import datetime
import requests


TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.eseGQs_A2CW9TN2Zew2mCyxjaGY"

bot = commands.Bot(command_prefix = "!")
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
    print ("{0.user} is online".format(bot))
    await bot.change_presence(activity=discord.Game(name="Rise Of Kingdoms"))

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

                print_roles = "/ ".join(commanders[name]['roles']).title()
                roles_list = [role for role in commanders[name]['roles']]

                current_build = roles_list[0]

                pairings = ""
                for pair in commanders[name]['roles'][current_build]['pairings']:
                    pairings += pair+"\n"

                info = discord.Embed(
                    title=f"{name} | {commanders[name]['title']}\n",
                    description= 
                    f"{commanders[name]['skills'][0]} | {commanders[name]['skills'][1]} | {commanders[name]['skills'][2]} \n\n"
                    f"**Rarity:** {commanders[name]['rarity']}\n**Troop Type:** {commanders[name]['type']}\n**Roles:** {print_roles}"
                    f"\n\n**{current_build.title()} Build and Pairings:**",
                    timestamp = datetime.utcnow()
                )
                embed = info
                embed.set_image(url=commanders[name]['roles'][current_build]['build'])
                fields = [
                    ("**Recommended Pairings**", pairings, True),
                    ("**Statistics**", 
                    f"Attack: +{commanders[name]['roles'][current_build]['attack']}\n"
                    f"Defence: +{commanders[name]['roles'][current_build]['defence']}\n"
                    f"Health: +{commanders[name]['roles'][current_build]['health']}\n"
                    f"March Speed: +{commanders[name]['roles'][current_build]['march speed']}\n", True),
                ]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                embed.set_author(name="ROKBot", icon_url = "https://pbs.twimg.com/profile_images/1032911346554220544/sxBmKpGB_400x400.jpg")        
                embed.set_footer(text = f"Use the buttons to navigate the information for {name}.\nBot development server: https://discord.gg/qgNpQXnA\nBot made by HAMZA#9000")

                #LIST COMPREHENSION for Buttons
                ActionRow_list = [                    
                    Button(
                        label = role.title(),
                        style = ButtonType().Primary,
                        custom_id = role,
                    )
                    for role in roles_list
                ]

                await buttons.send(
                    embed = embed,
                    channel = ctx.channel.id,
                    components = [
                        ActionRow(ActionRow_list)
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