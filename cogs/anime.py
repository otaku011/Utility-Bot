import discord
from discord.ext import commands
import getanime as ga

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Anime cog was successfully loaded!')

    # Commands
    @commands.command()
    async def search(self, ctx, *, query):
        results = ga.search_anilist(query)
        url = results['link']
        embed = discord.Embed(color=0x00ff00)
        embed.title = results['title']
        embed.url = url
        embed.description = results['desc']
        embed.set_thumbnail(url=results['img'])
        embed.set_author(name='Anilist', url='http://anilist.co', icon_url='https://i.imgur.com/Ak72T73.png')
        embed.add_field(name='Total Eps:', value=results['totalEpisodes'])
        embed.add_field(name='Stats:', value=results['status'])
        genre = results['genres']
        genre_links = []
        for a in genre:
            url = f'[{a}]' + f'(https://anilist.co/search/anime/{a})'.replace(' ', '%20')
            genre_links.append(url)
        genre = ',  '.join(genre_links)
        embed.add_field(name='Genre:', value=genre)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Anime(client))
