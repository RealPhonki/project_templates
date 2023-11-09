# so many fuking imports
import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle
import platform
import json
import sys
import os
import asyncio
from bot_logger import logger

# load json file
if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

# create instance of the bot
client = commands.Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=discord.Intents.all())
client.logger = logger()

# change the bot status every 5 seconds
@tasks.loop(seconds=5)
async def change_status() -> None:
    bot_status = cycle(["status 1", "status 2"])
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready() -> None:
    # make this code look super professional and sexy by printing random versions for no reason
    client.logger.info(f"Logged in as {client.user.name}")
    client.logger.info(f"discord.py API version: {discord.__version__}")
    client.logger.info(f"Python version: {platform.python_version()}")
    client.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    client.logger.info("-------------------")
    change_status.start()

async def load() -> None:
    # for every python file in the cogs folder
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = filename[:-3]
            try:
                # load the python extension and print a cool message
                await client.load_extension(f"cogs.{extension}")
                client.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                # print the exception if there is one
                exception = f"{type(e).__name__}: {e}"
                client.logger.error(f"Failed to load extension {extension}\n{exception}")

async def main():
    async with client:
        await load()
        await client.start(config['token'])

asyncio.run(main())