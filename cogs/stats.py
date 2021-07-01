import time
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='ms!')


class stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    def userOnline(self, memberList):
        online = []
        for i in memberList:
            if i.status == discord.Status.online and i.bot == False:
                online.append(i)
        return online


    @commands.Cog.listener()
    async def on_ready(self):
        print("Stats are ready!")


    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")


    @commands.command(aliases=["ci"])
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        nsfw = self.bot.get_channel(channel.id).is_nsfw()
        news = self.bot.get_channel(channel.id).is_news()
        embed = discord.Embed(title='Channel Infromation: ' + str(channel),
                              colour=discord.Colour.from_rgb(54, 151, 255))
        embed.add_field(name='Channel Name: ', value=str(channel.name))
        embed.add_field(name="Channel's NSFW Status: ", value=str(nsfw))
        embed.add_field(name="Channel's id: ", value=str(channel.id))
        embed.add_field(name='Channel Created At: ',
                        value=str(channel.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
        embed.add_field(name='Channel Type: ', value=str(channel.type))
        embed.add_field(name="Channel's Announcement Status: ", value=str(news))
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        if member:
            embed = discord.Embed(title=f'Userinfo for {format(member.name)}',
                                  description=f'This is the userinfo for {format(member.mention)}',
                                  color=0x22a7f0)
            embed.add_field(name='joined Server', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                            inline=True)
            embed.add_field(name='joined discord', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                            inline=True)
            rollen = ''
            for role in member.roles:
                if not role.is_default():
                    rollen += f'{format(role.mention)}'
            if rollen:
                embed.add_field(name='Roles', value=rollen, inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'Userinfo from {format(member.name)}.')
            mess = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='❌ Unexpected Error ❌',
                                  description='Please try again!',
                                  color=0xFF0000)
            embed.set_footer(text='')
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/776832404135477268/801784214651535360/Logo.png')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(stats(bot))