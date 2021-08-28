import discord
import random
from discord_buttons_plugin import *
from discord.ext import commands
from dictionaries import commanders
from datetime import datetime
import requests
import asyncio

TOKEN = "ODYyNTMxMjE4NzA4NDk2NDM1.YOZsyw.eseGQs_A2CW9TN2Zew2mCyxjaGY"

bot = commands.Bot(command_prefix = "!")
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
    print ("{0.user} is online".format(bot))
    await bot.change_presence(activity=discord.Game(name="Rise Of Kingdoms"))



def commander_embed(name, index):
    print_roles = "/ ".join(commanders[name]['roles']).title()
    roles_list = [role for role in commanders[name]['roles']]
    if index == len(roles_list):
        index = 0
    elif index == -1:
        index = len(roles_list)-1

    print(f"Going to page {index+1}")
    current_build = roles_list[index]

    pairings = ""
    for pair in commanders[name]['roles'][current_build]['pairings']:
        pairings += pair+"\n"

    info = discord.Embed(
        title=f"{name} | {commanders[name]['title']} {index+1}/{len(roles_list)}\n",
        description= 
        f"{commanders[name]['skills'][0]} | {commanders[name]['skills'][1]} | {commanders[name]['skills'][2]} \n\n"
        f"**Rarity:** {commanders[name]['rarity']}\n**Troop Type:** {commanders[name]['type']}\n**Roles:** {print_roles}"
        f"\n\n**{current_build.title()} Build and Pairings:**",
        timestamp = datetime.utcnow()
    )
    embed = info
    embed.set_image(url=commanders[name]['roles'][current_build]['build'])
    embed.set_author(name="ROKBot", icon_url = "https://pbs.twimg.com/profile_images/1032911346554220544/sxBmKpGB_400x400.jpg")
    embed.set_footer(
        text = f"Use the buttons to navigate the information for {name}. Bot made by HAMZA#9000"
        )
    fields = [
        ("**Recommended Pairings**", pairings, True),
        ("**Statistics**", 
        f"Attack: +{commanders[name]['roles'][current_build]['attack']}\n"
        f"Defence: +{commanders[name]['roles'][current_build]['defence']}\n"
        f"Health: +{commanders[name]['roles'][current_build]['health']}\n"
        f"March Spd: +{commanders[name]['roles'][current_build]['march speed']}\n", True),
    ]
    #REASSIGNMENT OF "NAME"
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed



def get_buttons():
    #LIST COMPREHENSION for Buttons
    ActionRow_list = [                    
        Button(
            label = "<",
            style = ButtonType().Primary,
            custom_id = "left",
        ),
        Button(
            label = ">",
            style = ButtonType().Primary,
            custom_id = "right",
        ),
        Button(
            label = "Support",
            style = ButtonType().Link,
            url = "https://discord.gg/qgNpQXnA",
        )
    ]
    return ActionRow_list



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

                index = 0

                embed = commander_embed(name, index)

                ActionRow_list = get_buttons()

                await buttons.send(
                    embed = embed,
                    channel = ctx.channel.id,
                    components = [
                        ActionRow(ActionRow_list)
                    ]
                )


@buttons.click
async def left(ctx):
    name_split = str(ctx.message.embeds[0].title).split("|")[0].split()
    name = " ".join(name_split)
    page_str = str(ctx.message.embeds[0].title).split("/")[0].split()
    page = int(page_str[len(page_str)-1])#
    current_index = page-1
    index = current_index-1

    embed = commander_embed(name, index)
    ActionRow_list = get_buttons()
    await ctx.reply("Left Clicked")
    await ctx.message.edit(
        embed=embed,
        channel = ctx.channel.id,
        ActionRow_list = get_buttons(),
    )
    return



@buttons.click
async def right(ctx):
    name_split = str(ctx.message.embeds[0].title).split("|")[0].split()
    name = " ".join(name_split)
    page_str = str(ctx.message.embeds[0].title).split("/")[0].split()
    page = int(page_str[len(page_str)-1])
    current_index = page-1
    index = current_index+1

    embed = commander_embed(name, index)
    ActionRow_list = get_buttons()
    await ctx.reply("Right Clicked")
    await ctx.message.edit(
        embed=embed,
        channel = ctx.channel.id,
        ActionRow_list = get_buttons(),
    )
    return

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