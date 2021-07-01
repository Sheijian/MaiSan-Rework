
import random
import aiohttp
import discord
from discord.ext import commands


class anime(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @commands.command()
    async def anime(self, ctx):

     responses = ["Akudama Drive",
                 "Deca-Dence",
                 "Dorohedoro",
                 "In/Spectre",
                 "Kaguya-sama: Love is War",
                 "Kakushigoto",
                 "Moriarty the Patriot",
                 "My Next Life as a Villainess: All Routes Lead to Doom!",
                 "Rascal does not dream of a Bunny Girl Senpai + Rascal does not dream of a dreaming girl"]


     choices = [
                "https://cdn.discordapp.com/attachments/801475977158459432/802500323053797376/4e807d2d9bd21cb1a2a0e2255bc474e4.gif",
                "https://cdn.discordapp.com/attachments/793848298359488522/802605052719398972/216f939f15ed9d5af5622777c4cb88b2.gif",
                "https://cdn.discordapp.com/attachments/801475977158459432/802606134749954058/0fe4042eb03b1360c533f05de51377a9.gif",
                "https://cdn.discordapp.com/attachments/801475977158459432/802606445799538698/Anime-watching-tv-gif.gif",
                "https://cdn.discordapp.com/attachments/801475977158459432/802607085702348910/1.gif"]

     image = random.choice(choices)

     embed = discord.Embed(title=f'{random.choice(responses)}', colour=discord.Color.random())
     embed.set_image(url=image)
     embed.set_footer(text=f'I hope i could help you with this :)', )
     await ctx.send(embed=embed)

    @commands.command()
    async def animepfp(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/avatars') as r:
                res = await r.json()
                embed = discord.Embed(
                    description=f"**Here's your anime profilpicture!**",
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)

    @commands.command()
    async def wallpaper(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/wallpapers') as r:
                res = await r.json()
                embed = discord.Embed(
                    description=f"**Here's your wallpaper!**",
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)


    @commands.command()
    async def animepfp2(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/avatars') as r:
                res = await r.json()
                embed = discord.Embed(
                    description=f"**Here's your anime avatar!**",
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)

    @commands.command()
    async def wallpaper2(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/wallpapers') as r:
                res = await r.json()
                embed = discord.Embed(
                    description=f"**Here's your wallpaper!**",
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/nsfw/hentai') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def thigh(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/nsfw/thighs') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.random()
                )
                embed.set_image(url=res['url'])
                await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ohayo!")


def setup(bot):
    bot.add_cog(anime(bot))