import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random


class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaways are now ready!")

    def convert(self, time):
        pos = ["s", "m", "h", "d"]

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def gstart(self, ctx):
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

        questions = ["Which channel should it be hosted in?",
                     "What should be the duration of the giveaway? (s|m|h|d)",
                     "What is the prize of the giveaway?"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didnt answer in time, please be faster next time!')
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return

        channel = self.bot.get_channel(c_id)

        time = self.convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d)!")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return

        prize = answers[2]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")
        embed = discord.Embed(title="Giveaway!", description=f"{prize}", color=ctx.author.color)
        embed.add_field(name="Hosted by:", value=ctx.author.mention)
        embed.set_footer(text=f"Ends {answers[1]} from now!")
        my_msg = await channel.send(embed=embed)
        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)
        if len(users) == 0:
            em = discord.Embed(title='<:fail:761292267360485378> Giveaway Failed', color=ctx.author.color)
            em.add_field(name="Reason:", value="No one joined D:")
            em.add_field(name="Next steps:", value="Dont make a giveaway which you don't enter!")
            await channel.send(embed=em)
            return

        newembed = discord.Embed(title="Giveaway!", description=f"{prize}", color=ctx.author.color)
        newembed.add_field(name="Hosted by:", value=ctx.author.mention)
        newembed.add_field(name="Winner", value=f"{winner.mention}")
        newembed.set_footer(text=f"Ends {answers[1]} from now!")
        await my_msg.edit(embed=newembed)
        await channel.send(f"Congratulations! {winner.mention} won {prize}!")

    @gstart.error
    async def gstart_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="<:fail:761292267360485378> Giveaway failed!", color=ctx.author.color)
            embed.add_field(name="Reason:", value="`Administrator Permission is missing!`")
            embed.add_field(name="Ideal Solution:", value="Get the perms, lmao!")
            await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def reroll(self, ctx, channel: discord.TextChannel, id_: int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id was entered incorrectly.\nNext time mention a channel first and then the id!")
            return

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)
        await channel.send(f"Congratulations! The new winner is {winner.mention}!")

    @reroll.error
    async def reroll_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="<:fail:761292267360485378> Reroll failed!", color=ctx.author.color)
            embed.add_field(name="Reason:", value="`Manage Server is missing!`")
            embed.add_field(name="Ideal Solution:", value="Get the perms, lmao!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Giveaways(bot))
