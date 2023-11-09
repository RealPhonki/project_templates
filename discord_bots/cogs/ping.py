import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def ping(self, ctx):
        # get bot latency from discord api
        bot_latency = round(self.client.latency * 1000)

        # create embed instance
        embed_message = discord.Embed(title = f"pong : {bot_latency} ms")
        embed_message.set_author( # set author of embed to the user who requested the command
            name = f'Requested by {ctx.author.name}',
            icon_url = ctx.author.avatar
        )

        await ctx.send(embed = embed_message)

# add cog extension to "client" (the bot)
# NOTE: THIS CODE RUNS FROM THE DIRECTORY THAT "main.py" IS IN
async def setup(client):
    await client.add_cog(Ping(client))