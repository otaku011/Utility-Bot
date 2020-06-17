import discord, time, json, requests
import getanime as ga
from discord.ext import commands
import ast
import pastebin
from bs4 import BeautifulSoup
def run(client):
	client.run(YOUR_TOKEN_GOES_HERE)


def get_prefix(client, message):
	with open('config.json', 'r') as f:
		prefixes = json.load(f)
	return prefixes['prefix'][str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')


@client.event
async def on_ready():
	print('discord bot is ready.')
providers = ['gogoanime']
provider = 'gogoanime'

client.remove_command('help')
@client.command(pass_context=True)
async def help(ctx):
	user = client.get_user(ctx.message.author.id)
	embed = discord.Embed(color=0x00ff00)
	embed.set_author(name='Help')
	embed.add_field(inline=False, name='search', value='Searches for anime and returns the 1st result found.')
	embed.add_field(inline=False, name='ping', value='Returns the ping of the bot.')
	embed.add_field(inline=False, name='prefix', value='Change the prefix of the current server.')
	embed.add_field(inline=False, name='help', value='Lists all the available commands the bot offers.')
	await user.send(embed=embed)
	await ctx.send(f'Sent a DM to {user.mention} with all the available commands!')


@client.event
async def on_guild_join(guild):
	with open('config.json', 'r') as f:
		prefixes = json.load(f)

	prefixes['prefix'][str(guild.id)] = 'a!'

	with open('config.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	prefixes['prefix'].pop(str(guild.id))

	with open('config.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

def mk_embed(title, link, desciption):
	embed = discord.Embed(color=0x00ff00)
	embed.title = title
	embed.url = link
	embed.description = desciption
	return embed



def get_members():
	with open('config.json', 'r') as f:
		trusted = json.load(f)['trusted']
		return trusted

@client.command(aliases=['prefix'])
async def setprefix(ctx, prefix):
	trusted_mems = get_members()
	if str(ctx.message.author.id) in trusted_mems:
		with open('config.json', 'r') as f:
			prefixes = json.load(f)

		prefixes['prefix'][str(ctx.guild.id)] = prefix

		with open('config.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		await ctx.send(f'Successfully changed the prefix to: "{prefix}"!')
	else:
		await ctx.send('You are not allowed to use this command.')


"""discord id for the bot owner, change this!!!"""
owner = 674710789138939916

@client.command(aliases=['exit'])
async def shutdown(ctx):
	if str(ctx.message.author.id) == str(owner):
		await ctx.send('The bot is exiting.')
		await client.change_presence(status=discord.Status.offline)
		time.sleep(2)
		exit()
	else:
		await ctx.send('You are not allowed to use this command.')

@client.command()
async def trusted(ctx, user: discord.User):
	trusted_mems = get_members()
	if str(ctx.message.author.id) in trusted_mems:
		with open('config.json', 'r') as f:
			trusted = json.load(f)['trusted']

		trusted.append(str(user.id))
		print(trusted)
		with open('config.json', 'w') as f:
			json.dump(trusted, f, indent=4)
		await ctx.send(f'Successfully added {user.mention} to the trusted members list!')
	else:
		await ctx.send('You are not allowed to use this command.')

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def roast(ctx, user: discord.User):
	message = f'{ctx.message.author.mention} roasted {user.mention} in the barbecue!'
	await ctx.send(message)

if provider == 'gogoanime':
	@client.command()
	async def search(ctx, *, query):
		await ctx.send(f'Searching for: *{query}*')
		try:
			results = ga.gogo_api(f'Search/', query)['search'][0]
			url = 'https://www2.gogoanime.video/category/' + results['episodes'][0]['id'].replace('-episode-1', '')
			embed = discord.Embed(color=0x00ff00)
			embed.title = results['title']
			embed.url = url
			embed.description = results['synopsis']
			embed.set_thumbnail(url=results['img'])
			embed.set_author(name='Gogoanime', url='http://gogoanime.video', icon_url='https://cache.cdnfile.info/files/gogo/img/favicon.png')
			embed.add_field(name='Total Eps:', value=results['totalEpisodes'])
			embed.add_field(name='Stats:', value=results['status'])
			genre = results['genres']
			genre_links = []
			for a in genre:
				url = f'[{a}](https://www2.gogoanime.video/genre/{a})'
				genre_links.append(url)
			genre = ',  '.join(genre_links)
			embed.add_field(name='Genre:', value=genre)
			await ctx.send(embed=embed)
		except:
			try:
				results = ga.gogo_api_ani_list(f'Search/', query)['search'][0]
				url = 'https://www2.gogoanime.video/category/' + results['episodes'][0]['id'].replace('-episode-1', '')
				embed = discord.Embed(color=0x00ff00)
				embed.title = results['title']
				embed.url = url
				embed.description = results['synopsis']
				embed.set_thumbnail(url=results['img'])
				embed.set_author(name='Gogoanime', url='http://gogoanime.video', icon_url='https://cache.cdnfile.info/files/gogo/img/favicon.png')
				embed.add_field(name='Total Eps:', value=results['totalEpisodes'])
				embed.add_field(name='Stats:', value=results['status'])
				genre = results['genres']
				genre_links = []
				for a in genre:
					url = f'[{a}](https://www2.gogoanime.video/genre/{a})'
					genre_links.append(url)
				genre = ',  '.join(genre_links)
				embed.add_field(name='Genre:', value=genre)
				await ctx.send(embed=embed)
			except:
				await ctx.send("Couldn't perform the anime search. \nMake sure your spelling is correct and that you use the romaji anime name.")
else:
	@client.command()
	async def search(ctx, *, query):
		await ctx.send(f'Searching for: *{query}*')
		await ctx.send(f"```Couldn't perform the anime search.\nThe selescted provider may not be available.\nPlease choose a provider from this list:\n{providers}```")

run(client)
