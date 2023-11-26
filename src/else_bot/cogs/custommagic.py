from discord.ext import commands, tasks
from else_bot.util.persist import PersistedDict
from discord.utils import get
from else_bot.util.clients.reddit import RedditClient
from else_bot.util.clients.imgur import ImgurClient
from else_bot.util.markdown import get_links
import discord


class CustomMagic(commands.Cog):
    def __init__(self, client, bot_config):
        self.client = client
        self.last_post = PersistedDict("data/posts.json", keyType=str)
        self.custommagic_channel = bot_config.custom_magic_channel
        self._rc = RedditClient(**bot_config.reddit_config.to_dict())
        self._imgc = ImgurClient(**bot_config.imgur_config.to_dict())
        self.get_weeks_worst.start()

    @tasks.loop(hours=1)
    async def get_weeks_worst(self):
        """Check if there has been a new post and if so post to channel"""
        recent_post = self._rc.get_user_recent_post(
            "CorbinGDawg69", on_subreddit="magicthecirclejerking"
        )
        if recent_post is None or self.last_post.get(recent_post.permalink, False):
            return
        self.last_post[recent_post.permalink] = True
        links = get_links(recent_post.selftext)
        albumn_link = links[0][1].split("/")[-1]
        card_images = self._imgc.get_album_images(albumn_link)
        cards = links[1:-2]
        await self.client.get_channel(self.custommagic_channel).send(
            "Time for some bad magic cards"
        )
        for card in cards:
            message = f"**{card[0]}**\n [original post](<{card[1]}>)"
            images = []
            for i in range(self._rc.get_post_image_count(card[1])):
                images.append(self._imgc.get_image_as_buffer(card_images.pop(0)))
            print(message)
            await self.client.get_channel(self.custommagic_channel).send(
                content=message,
                files=[
                    discord.File(i, filename="card.jpg", spoiler=True) for i in images
                ],
            )
        await self.client.get_channel(self.custommagic_channel).send("Best, Elsebot")
