
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import re


time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)


class mod(commands.Cog):

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



    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, *limit):
        try:
            limit = int(limit[0])
        except IndexError:
            limit = 1
        deleted = 0
        while limit >= 1:
            cap = min(limit, 100)
            deleted += len(await ctx.channel.purge(limit=cap, before=ctx.message))
            limit -= cap
        tmp = await ctx.send(f'**:put_litter_in_its_place:** {deleted} messages deleted.')
        await asyncio.sleep(15)
        await tmp.delete()
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.kick(reason=reason)
            await ctx.send('<a:papaKick:809073345245085746> Member kicked')
        else:
            await ctx.send('**:no_entry:** Please tag a user!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *reason):
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.ban(reason=reason)
            await ctx.send('<a:banned:809073168483745793> Member banned')
        else:
            await ctx.send('**:no_entry:** Please tag a user!')


    @commands.command()
    async def unban(self, ctx, *, member):
        if ctx.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'I unbanned {user.mention}.')
                    return
        else:
            await ctx.send('You dont have enough permissions to do that.')

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            await member.add_roles(role)
            if member is None:
                await ctx.send('Please tag the user you wish to add the role')
                if member is not None:
                   await ctx.send(f'{ctx.author} added the role to {member.mention}')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, *, name):
        role = await ctx.guild.create_role(name=name)
        em = discord.Embed(title=" Role Created", color=ctx.author.color)
        em.add_field(name="Role:", value=f"{role.mention}")
        em.add_field(name="Moderator:", value=f"{ctx.author.mention}")
        em.set_footer(text="Wow you did it. Congrats!!")
        await ctx.send(embed=em)

    @createrole.error
    async def createrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="<:CuteDuckPanda:752209116910321744> Role Creation Failed")
            em.add_field(name="Reason:", value="`Manage Roles perms missing!`")
            em.set_footer(text="Imagine thinking you have the perms!")
            await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod commands Loaded!")


    @commands.command()
    @has_permissions(manage_channels=True)
    async def lock(self, ctx, *, reason=None):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=True)
        em = discord.Embed(title=f"🔒 Channel has been locked!",
                           color=discord.Color.green())
        em.add_field(name="**Responsible Moderator:**", value=f"{ctx.author.name}")
        em.add_field(name="**Reason:**", value=f"`{reason}`")
        em.add_field(name="Description",
                     value=" This channel is locked now!",
                     inline=False)
        await ctx.channel.send(embed=em)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="<a:peperain:756237468860153864> Lock Failed!", color=ctx.author.color)
            embed.add_field(name="Reason:", value=f"Manage Channels Permissions Missing!")
            embed.set_footer(text="Imagine thinking you have enough perms!")
            await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(manage_channels=True)
    async def unlock(self, ctx, *, reason=None):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, read_messages=True)
        em = discord.Embed(title=f"🔓 Channel has been unlocked!",
                           color=discord.Color.green())
        em.add_field(name="**Responsible Moderator:**", value=f"{ctx.author.name}")
        em.add_field(name="**Reason:**", value=f"`{reason}`")
        em.add_field(name="Description",
                     value="This channel is unlocked now!",
                     inline=False)
        await ctx.channel.send(embed=em)

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="<a:peperain:756237468860153864> Unlock Failed!", color=ctx.author.color)
            embed.add_field(name="Reason:", value=f"Manage Channels Permissions Missing!")
            embed.set_footer(text="Imagine thinking you have enough perms!")
            await ctx.send(embed=embed)


    @commands.command()
    async def roles(self, ctx):
        msg = f'Server Roles **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
          if role.is_default():
            roleDict[role.position] = 'everyone'
          else:
            roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
         msg += role[1] + '\n'
        await ctx.send(msg)



    @commands.command()
    @has_permissions(manage_channels=True)
    async def mcount(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        messages = await channel.history(limit=None).flatten()
        count = len(messages)
        em = discord.Embed(title=f"Count of {channel.mention}", color=ctx.author.color,
                           description="There are {} messages in {}".format(count, channel.mention))
        await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod commands are ready!")


def setup(bot):
    bot.add_cog(mod(bot))










