import discord
from discord.ext import commands


class Task(commands.Cog):

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


    @commands.command()
    async def createcategory(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"I created {category.name}!")


    @commands.command()
    async def createchannel(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=self.bot.get_channel(707945693582590005),
        )
        await ctx.send(f"I created {channel.name}!")


    @commands.command()
    async def deletecategory(self, ctx, category: discord.CategoryChannel, *, reason=None):
        await category.delete(reason=reason)
        await ctx.send(f"I deleted {category.name}")


    @commands.command()
    async def deletechannel(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"I deleted {channel.name}.")


def setup(bot):
    bot.add_cog(Task(bot))