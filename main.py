import discord
from discord.ext import commands
from else_bot.util.config import Config
from else_bot.util.clients.imgur import ImgurClient
from else_bot.util.clients.reddit import RedditClient
from else_bot.cogs.elseify import Elsify
from else_bot.cogs.scry import ScrySearch
from else_bot.cogs.custommagic import CustomMagic

conf = Config.get_config()
imgur_client = ImgurClient(**conf.imgur_config.to_dict())
reddit_client = RedditClient(**conf.reddit_config.to_dict())


class ElseBot(commands.Bot):
    async def on_ready(self):
        game = discord.Game("Destroying the evidence")
        await self.change_presence(status=discord.Status.idle, activity=game)
        await self.add_cog(Elsify(self, conf.else_channels[0]))
        await self.add_cog(ScrySearch())
        await self.add_cog(CustomMagic(self, conf))


intents = discord.Intents.all()
print(intents)
intents.members = True
intents.messages = True

bot = ElseBot(intents=intents, command_prefix="$")
bot.run(conf.discord_token)
