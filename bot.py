# Phantom Bot, Made by BastaMasta
# This bot was made under the order #FO5182C3357D8 at fiverr

# In case of any issues with the bot, make sure let me know on discord: BASTAMASTA#6003
# Check out my Fiverr page: https://www.fiverr.com/bastamasta

import asyncio
import discord
from discord import Intents
from discord.ext import commands
from collections.abc import Sequence

TOKEN = "Nope. Not Gonna Show ya"

BOT_PREFIX = "/"


# Defining functions for making my life easier later in the code

# A function for creating sequences
def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return(seq,)


def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)

    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check


PhantomBot = commands.Bot(command_prefix=BOT_PREFIX, intents=Intents.all())


@PhantomBot.event
async def on_ready():
    print("The Bot is now up and running!")


@PhantomBot.command()
async def login(ctx):
    author1 = ctx.message.author
    print("Login Command Initiated by {0}".format(author1.display_name))
    await author1.send("You have executed the /login command \nYou are now required to enter the Server name and send it to this little bot here **[that's me!]**")
    await author1.send("Please enter the server Name")
    try:
        response = await PhantomBot.wait_for('message', check=message_check(channel=author1.dm_channel), timeout=500)
        d = {}
        with open("servers_and_passwords.txt") as f:
            for line in f:
                (key, val) = line.split()
                d[key] = val
        statement = 1
        serverinp = response.content.replace(' ', '_').replace('.', '_').lower()
        for key in d:
            if key == serverinp:
                statement = 0
                await author1.send("Server name accepted. \nPlease enter the password")
                response1 = await PhantomBot.wait_for('message', check=message_check(channel=author1.dm_channel), timeout=500)
                passinp = response1.content.replace(' ', '_').replace('.', '_').lower()
                if passinp == d[key]:
                    guild1 = PhantomBot.get_guild(628111579585708042)
                    role = discord.utils.get(guild1.roles, name="Student")
                    await author1.send("Credentials Accepted.\nYou have now been granted the **Student** Role at Amazon Seller Pros!")
                    await author1.add_roles(role)
                    print("Positive credentials were received from {0}".format(author1.display_name))
                else:
                    await author1.send("EPIC FAIL")
                    print("Correct server, yet incorrect password was received from {0}".format(author1.display_name))
        if statement == 1:
            await author1.send("You seem to have entered the incorrect server.")
    except:
        await author1.send("The request was timed out (500 seconds)")
        print("timeout by {0}".format(author1.display_name))

@PhantomBot.command()
@commands.is_owner()
async def shutdown(ctx):
    print("Shutdown initiated by {0}".format(ctx.message.autor))
    await ctx.send("Shutting down the bot in 5 seconds")
    await asyncio.sleep(5)
    await ctx.bot.close()


PhantomBot.run(TOKEN)
