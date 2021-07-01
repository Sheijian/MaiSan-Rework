import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.filtered_words = ['idiot', 'Idiots', "DIE", "ass", "butt", "Fool", "bitch"]
        self.INVITE_LINK = \
            "https://discord.com/oauth2/authorize?client_id=802249048382898186&permissions=1345711190&scope=bot"


    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc commands are ready!")

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite Link:", color = ctx.author.color)
        embed.add_field(name="Here:", value=f"[Click me]({self.INVITE_LINK})")
        await ctx.send(embed=embed)

    @commands.command(aliases=["sc"])
    async def servercount(self, ctx):
        sc = 0
        for i in self.client.guilds:
            sc += 1
        embed = discord.Embed(title="Server Count", color = ctx.author.color)
        embed.add_field(name="Server Count:", value = f"`{sc}`")
        embed.add_field(name="User Count:", value = f'`{len(self.client.users)}`')
        await ctx.send(embed=embed)



    @commands.command()
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        if suggestion is None:
            await ctx.send("Please enter the suggestion.")
        await ctx.send("Your suggestion has been sent to the devs!")
        embed = discord.Embed(title = "New Suggestions", color = discord.Color.random())
        embed.add_field(name="Author:", value=f"`{ctx.author.name}`")
        embed.add_field(name="Server:", value=f"`{ctx.guild.name}`")
        embed.add_field(name="Suggestion: ", value=f"`{suggestion}`")
        embed.set_footer(text="Thanks for the feedback <a:1461_Heart:793565711494152202>")
        guild = self.client.get_guild(805770467562094632)
        for channel in guild.channels:
            if channel.id == 805807510132490311:
                await channel.send(embed = embed)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title = "Slow it down C'mon", color = ctx.author.color)
            embed.add_field(name = 'Reason:', value = "If you have many suggestions than dm sheijian#0004!")
            await ctx.send(embed = embed)

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title="Support Me! 🎉", color=ctx.author.color,
        description ="""
        :link: Review me on top.gg [here](https://top.gg/bot/802249048382898186)\n
        :link: Please vote on top.gg [here](https://top.gg/bot/802249048382898186/vote)
        """
        )
        embed.add_field(name = "Invite Link!", value = f":link: [Invite Link]({self.INVITE_LINK})")
        embed.add_field(name = "Support Server!", value = f":link: [Support Server](https://discord.gg/48TYrhJ3V2)")
        embed.add_field(name = "Why Support me?", inline = False, value = f"Its your decision if you wanna support me or not.\n"
        "But if you like how I roll and think that I help your servers, just by doing these small tasks you can take me to other people who \n"
        f"are in need like you.\n\nPlus I have many commands and am just in {len(self.client.guilds)} servers.")
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Misc(client))