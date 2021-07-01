
import discord
from discord.ext import commands


class owner(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.command(hidden=True, aliases=['guilds'])
    async def servers(self, ctx):
        msg = '```js\n'
        msg += ' {!s:>5s} | {} | {}\n'.format('Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:>5s}| {} | {}\n'.format(guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, string):
        occupation = discord.Game(name=string)
        await self.bot.change_presence(activity=occupation)
        await ctx.message.add_reaction("✅")


    @commands.Cog.listener()
    async def on_ready(self):
        print("King commands are ready!")


def setup(bot):
    bot.add_cog(owner(bot))