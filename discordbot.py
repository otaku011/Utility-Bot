import discord, time, json, requests
from discord.ext import tasks, commands
import ast, os, asyncio
import sys
from bs4 import BeautifulSoup

command_prefix = 'u!'
BOT_TOKEN = 'token goes here'
def run(client):
	client.run(BOT_TOKEN)
client = commands.Bot(command_prefix = command_prefix)
client.remove_command('help')

extensions = []
for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and 'getanime' not in filename:
		client.load_extension(f'cogs.{filename[:-3]}')
		extensions.append(filename[:-3])
commandss = []
for extension in extensions:
	try:
		with open(os.path.join('./cogs', extension + '.json'), 'r') as f:
			helpm = json.loads(f.read())['help']
			for key, value in helpm.items():
				entry = [key, value]
				commandss.append(entry)
	except Exception as e:
		print("Error: " + str(e))
@client.command()
async def help(ctx):
	embed = discord.Embed(color=0x00ff00)
	embed.set_author(name='Help')
	for a in commandss:
		embed.add_field(inline=False, name=a[0], value=a[1])
	embed.add_field(inline=False, name='ping', value='Returns the ping of the bot.')
	embed.add_field(inline=False, name='help', value='Lists all the available commands the bot offers.')
	await ctx.send(embed=embed)



def read_config():
	with open('config.json', 'r') as f:
		return json.load(f)

def edit_config(data):
	with open('config.json', 'w') as f:
		json.dump(data, f, indent=4)

##events

#on_connect()
@client.event
async def on_connect():
	print('Bot is connecting...')

#on_ready()
@client.event
async def on_ready():
	print('Discord bot is ready.')

#on_message()
@client.event
async def on_message(message):
	#Checks if message sent by himself
	if message.author == client.user:
		return
	#Checks if mentioned
	if client.user in message.mentions:
		await message.channel.send("Utility bot reports to duty, Sir!. My prefix is "+ command_prefix)

	await client.process_commands(message)


##commands

#Trusted
@client.command()
async def trusted(ctx, user: discord.User):
	trusted_mems = read_config()
	if str(ctx.message.author.id) in trusted_mems['trusted']:
		with open('config.json', 'r') as f:
			trusted = json.load(f)
			trusted['trusted'].append(str(user.id))
			print(trusted)
			with open('config.json', 'w') as f:
				json.dump(trusted, f, indent=4)
			await ctx.send(f'Successfully added {user.mention} to the trusted members list!')
	else:
		pass




#DM command
@client.command()
async def dm(ctx, user: discord.User, *, message):
	await user.send(message)


#Ping utility
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#Creates an embed and returns it.
def mk_embed(title, link, desciption):
	embed = discord.Embed(color=0x00ff00)
	embed.title = title
	embed.url = link
	embed.description = desciption
	return embed

run(client)
