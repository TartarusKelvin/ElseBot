from discord.ext import commands, tasks
from else_bot.util.persist import PersistedDict
from discord.utils import get


class Elsify(commands.Cog):
    def __init__(self, client, else_channel):
        self.client = client
        self.elses = PersistedDict("data/elses.json", keyType=int)
        self.else_channel = else_channel
        self.verify_elses.start()

    @commands.command()
    async def who(self, ctx):
        """Returns Who "elsed" a given user"""
        user = ctx.message.mentions[0]
        for parent, elses in self.elses.items():
            if user.id in elses:
                parent_user = self.__get_user_by_id(parent)
                await ctx.send(f"User {user.name} was elsified by {parent_user.name}")
                return
        await ctx.send("It looks like that user hasnt been elsed :skull: ...")

    @commands.command()
    async def elsestat(self, ctx):
        """Returns some stats about an else"""
        user = ctx.message.mentions[0]
        elses = self.elses.get(user.id, [])
        else_users = [self.__get_user_by_id(x) for x in elses]
        elselist = ", ".join([e.name for e in else_users])
        await ctx.send(f"User {user.name} has elsed {elselist}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.else_channel:
            return
        for mention in message.mentions:
            desc = await self.add_user(message.author, mention)
            await message.channel.send(desc)

    async def add_user(self, parent, child):
        parent_id = parent.id
        child_id = child.id
        parent_elses = self.elses.get(parent_id, [])
        if len(parent_elses) >= 2:
            return "You already have 2 elses, may I suggest :dagger:?"
        for p, es in self.elses.items():
            if child_id in es:
                return "User has already been elsified"
        self.elses[parent_id] = parent_elses + [child_id]
        # assign the correct roles
        for role in parent.roles:
            if role.name.startswith("Tier "):
                new_tier = 1 + int(role.name.split(" ")[-1])
                if new_tier == 5:
                    new_tier = 6
                for role in parent.guild.roles:
                    if role.name == f"Tier {new_tier}":
                        c = chr((len(role.members)) + ord("a"))
                        await child.add_roles(role, reason="Elsification")
                        await child.edit(nick=f"Else (tier {new_tier}{c})")
        return "New Else Has Been Added"

    @tasks.loop(hours=24)
    async def verify_elses(self):
        """Check elses and update if necessary"""
        print("Verifying")
        missing_elses = []
        invalid_members = []
        to_delete = []
        member_ids = [x.id for x in self.client.get_all_members()]
        for parent, elses in self.elses.items():
            new_elses = [x for x in elses if x in member_ids]
            if len(new_elses) < len(elses):
                self.elses["parent"] = new_elses
                invalid_members.append(parent)
            if parent not in member_ids:
                to_delete.append(parent)
        for id in to_delete:
            del self.elses[to_delete]
        for member in member_ids:
            for parent, elses in self.elses.items():
                if member in elses:
                    break
            else:
                missing_elses.append(member)
        if len(missing_elses) > 0:
            message = "I have been doing some spring cleaning and I cant help but notice some of you have not been elsed :angry:\n"
            usrs = ", ".join([self.__get_user_by_id(x).name for x in missing_elses])
            message += f"{usrs} you have 24 hours"
            await self.client.get_channel(self.else_channel).send(message)
        if len(invalid_members) > 0:
            await self.client.get_channel(self.else_channel).send(
                f"I have refunded {len(invalid_members)}"
            )

    def __get_user_by_id(self, userid):
        return get(self.client.get_all_members(), id=userid)
