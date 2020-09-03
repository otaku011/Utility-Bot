import discord, json, asyncio
from stream_redirect import Redirect
from discord.ext import tasks, commands
import youtube_dl
# import ProxyFinder as PF ## USAGE>> PF.get_proxy() will return a proxy
import threading, os
from youtube_search import YoutubeSearch

multi_queue = {}

async def get_real_url(url):
    ydl = youtube_dl.YoutubeDL()
    result = ydl.extract_info(url, download=False)
    urls = [f['url'] for f in result['formats']]
    url = urls[0]
    return url


async def connect(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        ctx.send("Not connected to Voice Channel!")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()

    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client

async def fplay(ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            await asyncio.sleep(5)
            await fplay(ctx)
        else:
            try:
                source = multi_queue[ctx.guild.id][0]
                voice_client.play(discord.FFmpegPCMAudio(await get_real_url(source), before_options=("-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")))
                del multi_queue[ctx.guild.id][0]
                await fplay(ctx)
            except IndexError:
                return


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('The Music cog was successfully loaded!')

    @commands.command(aliases=['disconnect'])
    async def voice_disconnect(self, ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()

    @commands.command(aliases=['vcplay'])
    async def voice_play(self, ctx, *, url="Empty"):

        try:
            await connect(ctx)
            if url == "Empty":
                try:
                    voice_client = ctx.voice_client
                    voice_client.resume()
                except:
                    ctx.send("No URL provided")
            elif 'watch?v=' in url and "&list" not in url:
                try:
                    multi_queue[ctx.guild.id].append(url)
                except KeyError:
                    multi_queue[ctx.guild.id] = [url]
                voice_client = ctx.voice_client
                await fplay(ctx)
            elif 'watch?v=' in url and "&list" in url:
                url = "https://www.youtube.com/playlist?" + url.split('&')[1]
                r = Redirect(stdout=True, stderr=True)
                with r:
                    os.system(f'youtube-dl -f best --ignore-errors --get-url "{url}"')
                video_links = r.stdout
                video_links = video_links.split('\n')
                for a in video_links:
                    try:
                        multi_queue[ctx.guild.id].append(a)
                    except KeyError:
                        multi_queue[ctx.guild.id] = [a]
                voice_client = ctx.voice_client
                await fplay(ctx)
            else:
                results = YoutubeSearch(url, max_results=1).to_dict()[0]
                url = 'https://www.youtube.com/' + results['link']
                try:
                    multi_queue[ctx.guild.id].append(url)
                except KeyError:
                    multi_queue[ctx.guild.id] = [url]
                voice_client = ctx.voice_client
                await fplay(ctx)
        except:
            if url == "Empty":
                try:
                    voice_client = ctx.voice_client
                    voice_client.resume()
                except:
                    ctx.send("No URL provided")
            if "/" in url:
                try:
                    multi_queue[ctx.guild.id].append(url)
                except KeyError:
                    multi_queue[ctx.guild.id] = [url]
                voice_client = ctx.voice_client
                await fplay(ctx)

    @commands.command(aliases=['vcpause'])
    async def voice_pause(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            return
        if voice_client.is_playing():
            voice_client.pause()
            return


    @commands.command(aliases=['vcskip'])
    async def voice_skip(self, ctx):
        voice_client = ctx.voice_client
        voice_client.stop()
        await fplay(ctx)




def setup(client):
    client.add_cog(Music(client))
