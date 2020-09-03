import discord, requests, random
from discord.ext import commands
import json

def getRoast():
	with open('./roasts.json', 'r') as f:
		data = json.loads(f.read())
	return data

def WriteRoast(data):
	with open('./roasts.json', 'w') as f:
		json.dump(data, f, indent=4)

class Admin(commands.Cog):

	def __init__(self, client):
		self.client = client
	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('The Administration cog was successfully loaded!')

	# Commands
	@commands.command(aliases=['exit'])
	async def restart(self, ctx):
		if ctx.author.id in [674710789138939916, 497786894789378059]:
			await self.client.logout()
			await self.client.close()
		else:
			ctx.send('You are not allowed to use this command.')


	@commands.command()
	async def roast(self, ctx, user: discord.User):
		roasts = getRoast()['roast_list']
		message = random.choice(roasts).format(user.mention)
		await ctx.send(message)

	@commands.command(aliases=['roast-add'])
	async def add_roast(self, ctx, *, roast):
		if ctx.author.id in [674710789138939916, 497786894789378059]:
			roasts = getRoast()
			roasts['roast_list'].append(roast)
			WriteRoast(roasts)
			await ctx.send(f"**{roast}** was successfuly added.")
		else:
			await ctx.send("Couldn't register the roast, you are not in the **Trusted** list.")


def setup(client):
	client.add_cog(Admin(client))
