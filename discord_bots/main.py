# external imports
from discord.ext import commands, tasks
from discord import Intents, Embed, Game, __version__
from asyncio import run

# builtin imports
from platform import python_version, system, release
from itertools import cycle
import json
import os

# local imports
from bot_logger import logger

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        """
        Creates some custom attributes before calling the super initializer.
        """
        self.config = self.load_config()
        self.logger = logger()
        self.add_commands()

        super().__init__(self.config["prefix"], intents=Intents.all())
    
    def load_config(self) -> dict:
        """
        Loads config.json as a json file and returns the contents as a dictionary.
        """
        try:
            with open("config.json") as file:
                return json.load(file)
            
        except Exception as error:
            raise FileNotFoundError(f"{type(error).name}: {error}")

    async def on_ready(self) -> None:
        """
        Debug information to confirm that the bot has connected.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {__version__}")
        self.logger.info(f"Python version: {python_version()}")
        self.logger.info(f"Running on: {system()} {release()} ({os.name})")
        self.logger.info("-------------------")

        self.change_status.start()

    async def load(self) -> None:
        """
        Loops through every python file in the cogs folder and loads it as a cog extension.
        """
        for filename in os.listdir("./cogs"):
            if not filename.endswith(".py"):
                continue

            extension = filename[:-3] # remove the '.py' from the name
            try:
                await self.load_extension(f"cogs.{extension}")
                self.logger.info(f"Loaded extension '{extension}'")

            except Exception as error:
                exception = f"{type(error).__name__}: {error}"
                self.logger.error(f"Failed to load extension {extension}\n{exception}")

    @tasks.loop(seconds=60)
    async def change_status(self) -> None:
        """
        Changes the bot status every 60 seconds.
        """
        bot_status = cycle(self.config["statuses"])
        await self.change_presence(activity=Game(next(bot_status)))

    def add_commands(self) -> None:
        """
        Adds commands that are required for bot development.
        """
        try:
            @self.command(name="sync") 
            async def sync(ctx: commands.Context):
                print("test")
                try:
                    synced = await self.tree.sync()

                    # create embed instance
                    embed_message = Embed(title = f"Synced {len(synced)} command(s)")
                    embed_message.set_author( # set author of embed to the user who requested the command
                        name = f'Requested by {ctx.author.name}',
                        icon_url = ctx.author.avatar
                    )

                    await ctx.send(embed=embed_message)

                except Exception as e:
                    await ctx.send(f"{type(e).__name__}: {e}")
            
            self.logger.info(f"Loaded command 'sync'")

        except Exception as error:
            exception = f"{type(error).__name__}: {error}"
            self.logger.error(f"Failed to load command 'sync'\n{exception}")

    async def main(self) -> None:
        """
        Loads the bot and logs into the discord server.
        """
        await self.load()
        await self.start(self.config["token"])

if __name__ == '__main__':
    discord_bot = DiscordBot()
    run(discord_bot.main())
