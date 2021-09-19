import discord
import random
from discord_buttons_plugin import *
from discord.ext import commands
from commander_bot.models import Commander
from datetime import datetime
import requests
import asyncio
import json

TOKEN = ""

bot = commands.Bot(command_prefix="!")
buttons = ButtonsClient(bot)


@bot.event
async def on_ready():
    print("{0.user} is online".format(bot))
    await bot.change_presence(activity=discord.Game(name="Rise Of Kingdoms"))


def commander_embed(commander_info, name, index):
    roles_list = [role for role in commander_info["builds"]]
    print_roles = "/ ".join(roles_list).title()
    if index == len(roles_list):
        index = 0
    elif index == -1:
        index = len(roles_list) - 1

    print(f"Going to page {index+1}")
    current_build = roles_list[index]

    primary_pairings = ""
    for pair in commander_info["builds"][current_build]["primary_pairings"]:
        primary_pairings += pair + "\n"

    secondary_pairings = ""
    for pair in commander_info["builds"][current_build]["primary_pairings"]:
        secondary_pairings += pair + "\n"

    info = discord.Embed(
        title=f"{name} | {commander_info['commander']['title']} {index+1}/{len(roles_list)}\n",
        description=f"{commander_info['commander']['speciality_one']} | {commander_info['commander']['speciality_two']} | {commander_info['commander']['speciality_three']} \n\n"
        f"**Rarity:** {commander_info['commander']['rarity']}\n**Troop Type:** {commander_info['commander']['troop_type']}\n**Roles:** {print_roles}"
        f"\n\n**{current_build.title()} Build and Pairings:**",
        timestamp=datetime.utcnow(),
    )
    embed = info
    embed.set_image(url=commander_info["builds"][current_build]["talent_tree"])
    embed.set_author(
        name="ROKBot",
        icon_url="https://pbs.twimg.com/profile_images/1032911346554220544/sxBmKpGB_400x400.jpg",
    )
    embed.set_footer(
        text=f"Use the buttons to navigate the information for {name}. Bot made by HAMZA#9000"
    )
    fields = [
        ("**Primary Pairings**", primary_pairings, True),
        ("**Secondary Pairings**", secondary_pairings, True),
        (
            "**Statistics**",
            f"Attack: +{commander_info['builds'][current_build]['attack']}\n"
            f"Defence: +{commander_info['builds'][current_build]['defence']}\n"
            f"Health: +{commander_info['builds'][current_build]['health']}\n"
            f"March Spd: +{commander_info['builds'][current_build]['march speed']}\n",
            True,
        ),
    ]
    # REASSIGNMENT OF "NAME"
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


def get_buttons():
    # LIST COMPREHENSION for Buttons
    ActionRow_list = [
        Button(
            label="<",
            style=ButtonType().Primary,
            custom_id="left",
        ),
        Button(
            label=">",
            style=ButtonType().Primary,
            custom_id="right",
        ),
        Button(
            label="Support",
            style=ButtonType().Link,
            url="https://discord.gg/qgNpQXnA",
        ),
    ]
    return ActionRow_list


@bot.command()
async def Com(ctx):
    message_split = str(ctx.message.content).split("Com")[1].split()
    message = " ".join(message_split)

    response = requests.get(
        "https://rise-of-kingdoms-bot.herokuapp.com/api/commander/<str:pk>"
    )
    commander_info = response.json()
    try:
        index = 0
        embed = commander_embed(
            commander_info, commander_info["commander"]["name"], index
        )

        ActionRow_list = get_buttons()

        await buttons.send(
            embed=embed, channel=ctx.channel.id, components=[ActionRow(ActionRow_list)]
        )
    except:
        await ctx.reply(commander_info["error"])


@buttons.click
async def left(ctx):
    name_split = str(ctx.message.embeds[0].title).split("|")[0].split()
    name = " ".join(name_split)
    page_str = str(ctx.message.embeds[0].title).split("/")[0].split()
    page = int(page_str[len(page_str) - 1])  #
    current_index = page - 1
    index = current_index - 1

    embed = commander_embed(name, index)
    ActionRow_list = get_buttons()
    await ctx.reply(" ")
    await ctx.message.edit(
        embed=embed,
    )


@buttons.click
async def right(ctx):
    name_split = str(ctx.message.embeds[0].title).split("|")[0].split()
    name = " ".join(name_split)
    page_str = str(ctx.message.embeds[0].title).split("/")[0].split()
    page = int(page_str[len(page_str) - 1])
    current_index = page - 1
    index = current_index + 1

    embed = commander_embed(name, index)
    ActionRow_list = get_buttons()
    await ctx.reply("")
    await ctx.message.edit(
        embed=embed,
    )


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    # if message author is the bot itself, don't reply
    if message.author == bot.user:
        return

    # replies to general chat
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
