import discord, json
from discord.ext import commands

def read_config():
    with open('./cogs/bannedwords.json', 'r') as f:
        return json.load(f)

def edit_config(data):
	with open('./cogs/bannedwords.json', 'w') as f:
		json.dump(data, f, indent=4)


async def check_forbidden(message):
    words = read_config()
    for word in words['banned']:
        if word in message.content:
            await message.author.send(f"Warning, you used the forbidden word: {word}")
            await message.delete()
        else:
            pass

class Automod(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Automod cog was successfully loaded!')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        await check_forbidden(message)


    # Commands
    @commands.command()
    async def banword(self, ctx, word):
        config = read_config()
        if str(ctx.message.author.id) in config['trusted']:

            words = read_config()
            words['banned'].append(str(word))
            edit_config(words)

            await ctx.send(f'Successfully added {word} to the banned words list!')
        else:
            pass

def setup(client):
    client.add_cog(Automod(client))
