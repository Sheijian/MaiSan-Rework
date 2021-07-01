
# import io
# import chat_exporter
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import json


class Tickets(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("Tickets are ready!")

    @commands.command(aliases=['createticket', 'ticketnew'])
    @cooldown(1, 10, BucketType.user)
    async def new(self, ctx, *, reason=None):
        em = discord.Embed(title="Confirm New Ticket", color=ctx.author.color)
        em.add_field(name="Reason:", value="We don`t want that people spam tickets!")
        em.add_field(name="Steps to do:", value="Type `yes` in the chat to confirm this ticket!")
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=em)

        def msg_check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.client.wait_for('message', timeout=15.0, check=msg_check)
        except:
            em = discord.Embed(title=" New Ticket Failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You took too long!")
            em.add_field(name="Cooldown", value="1 minute more!")
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        else:
            if msg.content != "yes":
                em = discord.Embed(title=" New Ticket Failed!", color=ctx.author.color)
                em.add_field(name="Reason:", value="You did not want to create one!")
                em.add_field(name="Cooldown", value="1 minute more!")
                em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em)

            else:
                channelname = "ticket-{}".format(ctx.author.name)
                for _channel in ctx.guild.channels:
                    if _channel.name == channelname:
                        return await ctx.channel.send(
                            f"You already have a ticket! Please contact staff in {_channel.mention}!")

                warning = \
                    f"""{ctx.author.mention} next time please add a reason so the staff team can solve your problem faster! Next time do: `ms!new <reason>`
                """
                tickets = await self.get_tickets()
                guild = ctx.guild
                author = ctx.author
                if str(ctx.guild.id) not in tickets:
                    em = discord.Embed(title=" New Failed", color=ctx.author.color)
                    em.add_field(name="Reason:", value="Tickets are not setup!")
                    em.add_field(name="Usage:",
                                 value="Usage for an admin:\n```diff\n+ ms!addticketrole <@role> [reason]\n"
                                       " ms!new [reason]\n```")
                    await ctx.send(embed=em)
                    return
                ticketrole = tickets[str(ctx.guild.id)]["ticketrole"]
                role_id = int(ticketrole)
                helper_role = ctx.guild.get_role(role_id)
                channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.name}')
                em = discord.Embed(title=f" New ticket", color=ctx.author.color)
                em.add_field(name="Ticket Channel:", value=f"{channel.mention}")
                em.add_field(name="Description:", value="Staff will be with your shortly")
                em.add_field(name="Member:", value=f"{ctx.author.mention}")
                em.add_field(name="Reason:", value=f"`{reason}`")
                await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
                await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
                await channel.set_permissions(helper_role, read_messages=True, send_messages=True)
                await channel.send(embed=em)
                if reason == None:
                    await channel.send(warning)
                await ctx.send(f"Created the ticket! Check {channel.mention}")

                try:
                    channelId = int(tickets[str(ctx.guild.id)]["ticketchannel"])
                    for channel_ in ctx.guild.channels:
                        if channel_.id == channelId:
                            em = discord.Embed(title="Ticket Opened!",
                                               color=ctx.author.color)
                            em.add_field(name="Member:", value=f"{ctx.author.mention}")
                            em.add_field(name="Reason:", value=f"`{reason}`")
                            em.add_field(name="Channel / Access Point", value=f'{channel.mention}')
                            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            await channel_.send(embed=em)
                            break
                except:
                    pass

    @new.error
    async def new_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=" New Error", color=ctx.author.color)
            em.add_field(name="Reason:", value="If your trying to spam the server just stfu please!")
            em.add_field(name="Try again in:", value="`{:.2f}s`".format(error.retry_after))
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=['setticketrole', 'ticketrole'])
    @commands.has_permissions(manage_guild=True)
    async def addticketrole(self, ctx, role: discord.Role = None, *, reason=None):
        if role == None:
            await ctx.send("You need to provide a valid role!")
            return

        tickets = await self.get_tickets()
        em = discord.Embed(title=" Added ticketrole", color=ctx.author.color)
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        guild = ctx.guild
        author = ctx.author
        if str(ctx.guild.id) not in tickets:
            em.add_field(name="Switch:", value=f"`None` => {role.mention}")
            tickets[str(guild.id)] = {}
            tickets[str(guild.id)]["ticketrole"] = int(role.id)
        else:
            role_id = tickets[str(guild.id)]["ticketrole"]
            tickets[str(guild.id)]["ticketrole"] = int(role.id)
            em.add_field(name="Role:", value=f"{role.mention}")
        em.add_field(name="Features:", value="Users can now type ` ms!new <reason>`")
        em.add_field(name="Reason:", value=f"`{reason}`")
        await ctx.send(embed=em)

        try:
            channelId = int(tickets[str(ctx.guild.id)]["ticketchannel"])
            for channel_ in ctx.guild.channels:
                if channel_.id == channelId:
                    em = discord.Embed(title=" Ticket Role Set!", color=ctx.author.color)
                    em.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                    em.add_field(name="Reason:", value=f"`{reason}`")
                    em.add_field(name="Ticket Role", value=f'{role.mention}')
                    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await channel_.send(embed=em)
                    break
        except:
            pass

        with open("tickets.json", "w") as f:
            json.dump(tickets, f)

#    @commands.command()
#    async def save(self, ctx):
#        transcript = await chat_exporter.export(ctx.channel)
#
#        if transcript is None:
#            return
#        transcript_file = discord.File(io.BytesIO(transcript.encode()),
#                                       filename=f"transcript-{ctx.channel.name}.html")
#        await ctx.send(file=transcript_file)

    @addticketrole.error
    async def addticketrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title=" Ticket Error", color=ctx.author.color)
            em.add_field(name="Reason:", value="You don't have the perms")
            em.add_field(name="Perms:", value="`Manage Server permission missing!`")
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=" Ticket Error", color=ctx.author.color)
            em.add_field(name="Reason:", value=f"{ctx.author.mention}, you need to provide a valid role!")
            em.add_field(name="Usage:",
                         value='```diff\n+ ms!addticketrole <@role> [reason]```')
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=['addticketlogs', 'atl', 'stl'])
    @commands.has_permissions(manage_guild=True)
    async def setticketlog(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        if channel is None:
            await ctx.send("You need to provide a valid channel!")

        em = discord.Embed(title="Ticket Logs Set", color=ctx.author.color)
        em.add_field(name="Moderator:", value=f"{ctx.author.mention}")
        em.add_field(name="Channel:", value=f"{channel.mention}")
        em.add_field(name="Reason:", value=f"`{reason}`", inline=False)
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.set_footer(text="Invite me with ms!invite ;)")
        await ctx.send(embed=em)

        tickets = await self.get_tickets()
        guild = ctx.guild

        if str(ctx.guild.id) not in tickets:
            tickets[str(guild.id)] = {}
            tickets[str(guild.id)]["ticketchannel"] = int(channel.id)
        else:
            tickets[str(guild.id)]["ticketchannel"] = int(channel.id)

        with open("tickets.json", "w") as f:
            json.dump(tickets, f)

    @setticketlog.error
    async def setticketlogs_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title=' Setticketlogs Failed', color=ctx.author.color)
            em.add_field(name="Reason:", value="`Manage Server permission is missing!`")
            em.set_thumbnail(url=ctx.author.avatar_url)
            em.set_footer(text="You wish to have enough permissions lmao!")
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=' Setticketlogs Failed', color=ctx.author.color)
            em.add_field(name="Reason:", value="Mention a channel properly, like {}".format(ctx.channel.mention))
            em.add_field(name="Usage:",
                         value="```diff\n+ ms!setticketlogs <#channel> better ticket logs\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            em.set_footer(text="Smh, imagine being that bad!")
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command(aliases=['deleteticket', "ticketdelete"])
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx, channel: discord.TextChannel):
        if channel.name.startswith('ticket-'):
            await channel.delete()
            await ctx.send("Successfully deleted the channel!")

    @commands.command(aliases=['closeticket', 'ticketclose'])
    async def close(self, ctx):
        em = discord.Embed(title=f"🔒 Channel has been closed!",
                           color=discord.Color.green())
        em.add_field(name="**Responsible Moderator:**", value=f"{ctx.author.name}")
        em.add_field(name="Description",
                     value=" Successfully closed the ticket!",
                     inline=False)
        await ctx.channel.send(embed=em)


    @delete.error
    async def close_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title=' Close Failed', color=ctx.author.color)
            em.add_field(name="Reason:", value="`Manage Channels permission is missing!`")
            em.set_thumbnail(url=ctx.author.avatar_url)
            em.set_footer(text="Imagine thinking that you have enough perms lmao...")
            await ctx.send(embed=em)

    async def get_tickets(self):
        with open("tickets.json", "r") as f:
            data = json.load(f)
        return data


    async def get_logs(self, guild):
        guild_id = guild.id
        tickets = await self.get_tickets()

        if str(guild_id) not in tickets:
            return False
        return int(tickets[str(guild.id)]["ticketchannel"])


    async def get_role(self, guild):
        guild_id = guild.id
        tickets = await self.get_tickets()

        if str(guild_id) not in tickets:
            return False
        return int(tickets[str(guild_id)]["ticketrole"])


    async def open_guild(self, guild, ticketrole: discord.Role, ticketchannel: discord.TextChannel):
        tickets = await self.get_tickets()
        if not str(guild.id) in tickets:
            tickets[str(guild.id)] = {}
            tickets[str(guild.id)]["ticketchannel"] = int(ticketchannel.id)
            tickets[str(guild.id)]["ticketrole"] = int(ticketrole.id)
        else:
            tickets[str(guild.id)]["ticketchannel"] = int(ticketchannel.id)
            tickets[str(guild.id)]["ticketrole"] = int(ticketrole.id)

        with open("tickets.json", "w") as f:
            json.dump(tickets, f)

        return [self.get_logs(guild), self.get_role(guild)]


def setup(client):
    client.add_cog(Tickets(client))