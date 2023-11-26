from discord.ext import commands
import else_bot.util.clients.scryfall as scryfall
import re


class ScrySearch(commands.Cog):
    def __init__(self):
        self._sc = scryfall.ScryfallClient()

    @commands.Cog.listener()
    async def on_message(self, message):
        a = re.findall("m\[\[(.*?)\]\]", message.content, re.DOTALL)
        for card in a:
            try:
                img = self._sc.lookup_card_image(card_name=card, exact=False)
                await message.channel.send(img)
            except scryfall.NoMatch:
                await message.channel.send(f"Could not find card {card}")
            except scryfall.TooManyMatches:
                await message.channel.send(f"Card name '{card}' has to many matches")
