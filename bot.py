TOKEN = ""

import discord
import json
import re
import requests

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for g in self.guilds:
            print(f"GUILD: {g.name}")
            print(f"{g.roles}")
            print(f"{g.channels}")
        game = discord.Game("Destroying the evidence")
        await self.change_presence(status=discord.Status.idle, activity=game)
			

    async def on_message(self, message):
        print(message.content)
        if message.author == client.user:
            return
        if message.content== "ping":
            await message.channel.send("Pnog")
        if (message.channel.id == 1048979078675447868) or message.channel.id == 1058738039775580250:
            print(f"{message.author} Has added the following:")
            for mention in message.mentions:
                res,desc = await self.add_user (message.author,mention)
                print(res,desc)
                await message.channel.send(desc)
                print(mention)

        if message.content.startswith("~who ") and len(message.mentions)>0:
            f=open('data/elses.json')
            data=json.loads(f.read())
            f.close()
            mention = message.mentions[0]
            mention_id = mention.id
            for pid in data:
                if mention_id in data[pid]["elses"]:
                    for mem in message.guild.members:
                        #print(mem.id,pid,str(mem.id)==str(pid))
                        if str(mem.id)==str(pid):
                            await message.channel.send(f"User {mention.name} was elsified by {mem.name}")
                            return

        if message.content.startswith("~whoelse ") and len(message.mentions)>0:
            f=open('data/elses.json')
            data=json.loads(f.read())
            f.close()
            mention = message.mentions[0]
            mention_id = mention.id
            msg=f"{mention.name} has elsified: "
            for e in data[str(mention_id)]["elses"]:
                for mem in message.guild.members:
                    #print(mem.id,pid,str(mem.id)==str(pid))
                    if str(mem.id)==str(e):
                        msg+=(f" {mem.name}, ")
            msg[-2:]
            await message.channel.send(msg)
            return
        if message.content.startswith("~tier ") and len(message.mentions)>0:
            rs = message.mentions[0].roles
            for r in rs:
                if r.name.startswith("Tier "):
                    await message.channel.send(r.name)
                    return
        if message.content.startswith("~ntier ") and len(message.mentions)>0:
            rs = message.mentions[0].roles
            for r in rs:
                if r.name.startswith("Tier "):
                    new_tier = "Tier "+str(1+int(r.name.split(" ")[-1]))
                    for nr in message.channel.guild.roles:
                        if nr.name == new_tier:
                            await message.channel.send(f"new_tier {nr.id}")
                    return
        if message.content.startswith("~nname ") and len(message.mentions)>0:
            rs = message.mentions[0].roles
            for r in rs:
                if r.name.startswith("Tier "):
                    new_tier = 1+int(r.name.split(" ")[-1])
                    ## We dont accept 5
                    if new_tier == 5:
                        new_tier=6
                    for nr in message.channel.guild.roles:
                        if nr.name == f"Tier {new_tier}":
                            c=chr((len(nr.members))+ord('a'))
                            await message.channel.send(f"Else (tier {new_tier}{c})")
        a=re.findall("\[\[(.*?)\]\]",message.content,re.DOTALL)
        for card in a:
            url="https://api.scryfall.com/cards/named"
            params={'exact':card}
            d=requests.get(url = url, params = params).json()
            if d["object"]=="error":
                return
            await message.channel.send(d["image_uris"]["border_crop"])


    async def add_user(self,fr,uname):
        f=open('data/elses.json','r')
        data=json.loads(f.read())
        f.close()
        if str(fr.id) in data:
            print(len(data[str(fr.id)]["elses"]))
            if len (data[str(fr.id)]["elses"]) >= 2:
                ## Person has to many elses
                return (1, "User Has Already Elsified Two Elses, Kill One Of Your Elses Please")
        else:
            data[str(fr.id)]={"elses":[]}
        if str(uname.id) in data:
            ## Already Claimed
            return (1, "User Has Existing Elsification, Perhaps Start A Else War?")
        data[str(fr.id)]["elses"].append(uname.id)
        data[str(uname.id)]={"elses":[]}
        with open("data/elses.json", "w") as outfile:
            outfile.write(json.dumps(data, indent=4)) 
        rs = fr.roles
        for r in rs:
            if r.name.startswith("Tier "):
                new_tier = 1+int(r.name.split(" ")[-1])
                ## We dont accept 5
                if new_tier == 5:
                    new_tier=6
                for nr in fr.guild.roles:
                    if nr.name == f"Tier {new_tier}":
                        c=chr((len(nr.members))+ord('a'))
                        await uname.add_roles(nr,reason="Elsification")
                        await uname.edit(nick=f"Else (tier {new_tier}{c})")
           
        return (0, "New Else Has Been Added")

intents = discord.Intents.all()
print(intents)
intents.members=True
intents.messages = True

client = MyClient(intents=intents)
client.run(TOKEN)

