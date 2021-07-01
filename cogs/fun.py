import asyncio
import random
import aiohttp
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import clean_content
import datetime


bot = commands.Bot(command_prefix='ms!')
                        

class fun(commands.Cog):
    db = 'reaction.db'

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
    async def praise(self, ctx):
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self, ctx):
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')

    @commands.command()
    async def countdown(self, ctx):
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('<a:PepeYay:763632785860198420>')

    @commands.command()
    async def shoot(self, ctx, member: discord.Member):
        embed = discord.Embed(title=f"{member.mentioned} shot by {ctx.author} ",
                              color=discord.Color.red())
        embed.set_image(url="https://i.gifer.com/XdhK.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=["table", "flip"])
    async def throw(self, ctx):
        await ctx.send("```(╯°□°)╯︵ ┻━┻```")

    @commands.command(aliases=['rot'])
    async def red(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        img = user.avatar_url

        url = f'https://some-random-api.ml/canvas/red?avatar={img}'

        embed = discord.Embed(title='Snap!', color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_footer(text=f'Red filter | Requested by {ctx.author}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['rand'])
    async def random(self, ctx, *arg):

        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Head', 'Number']
                await ctx.send(f':arrows_counterclockwise: {random.choice(coin)}')
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                await ctx.send(f':congratulations: The winner is {random.choice(choices)}')
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await ctx.send(f':congratulations: The winner is {user}')
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            await ctx.send(
                f'**:arrows_counterclockwise:** random number ({start} - {end}): {random.randint(start, end)}')

    @commands.command()
    async def stone(self, ctx, member: str):
        await ctx.send(f'R.I.P. {member}\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

    @commands.command(aliases=['hypu', 'train'])
    async def hype(self, ctx):
        hypu = [
            'https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
            'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
            'https://gfycat.com/HairyFloweryBarebirdbat',
            'https://i.imgur.com/PFAQSLA.gif',
            'https://abload.de/img/ezgif-32008219442iq0i.gif',
            'https://i.imgur.com/vOVwq5o.jpg',
            'https://i.imgur.com/Ki12X4j.jpg',
            'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)


    @commands.command()
    async def joke(self, ctx):

        jokes = ['Was sagt das eine Streichholz zum anderen Streichholz?\n Komm, lass uns durchbrennen',
                'Wieviele Deutsche braucht man um eine Glühbirne zu wechseln?\n Einen, wir sind humorlos und effizient.',
                'Wo wohnt die Katze?\n Im Miezhaus.',
                'Wie begrüßen sich zwei plastische Chirurgen?\n "Was machst du denn heute für ein Gesicht?"',
                'Warum essen Veganer kein Huhn?\n Könnte Ei enthalten',
                '85% der Frauen finden ihren Arsch zu dick, 10% zu dünn, 5% finden ihn so ok, wie er ist und sind froh, dass sie ihn geheiratet haben...',
                'Meine Freundin meint, ich wär neugierig...\n...zumindest\' steht das in ihrem Tagebuch.',
                '"Schatz, Ich muss mein T-Shirt waschen! Welches Waschmaschinen Programm soll ich nehmen?" - "Was steht denn auf dem T-Shirt drauf?"\n "Slayer!"',
                'Gestern erzählte ich meinem Freund, dass ich schon immer dieses Ding aus Harry Potter reiten wollte.\n"einen Besen?" "nein, Hermine."',
                'Warum gehen Ameisen nicht in die Kirche?\nSie sind in Sekten.',
                'Was steht auf dem Grabstein eines Mathematikers?\n"Damit hat er nicht gerechnet."',
                'Wenn ein Yogalehrer seine Beine senkrecht nach oben streckt und dabei furzt, welche Yoga Figur stellt er da?\n Eine Duftkerze',
                'Warum ging der Luftballon kaputt?\n Aus Platzgründen.',
                'Ich wollte Spiderman anrufen, aber er hatte kein Netz.',
                'Was vermisst eine Schraube am meisten? Einen Vater',
                'Geht ein Panda über die Straße. Bam....Bus!']
        emojis = [':laughing:', ':smile:', ':joy:', ':sob:', ':rofl:']
        msg = f'{random.choice(emojis)} {random.choice(jokes)}'
        await ctx.send(msg)

    @commands.command()
    async def pat(self, ctx: commands.Context, user: discord.Member):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/pat') as r:
                res = await r.json()
                if user == ctx.author:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** gives themselves a pat on the back!",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** pats **{user.name}**",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)

    @commands.command()
    async def tickle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekos.life/api/v2/img/tickle") as r:
                data = await r.json()
                embed_tickle = Embed(
                    title='Tickle!',
                    description=f'*{ctx.author.display_name} tickles {member.display_name}~*',
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Color.red())
                embed_tickle.set_image(url=data['url'])
                embed_tickle.set_footer(text="{}".format(ctx.author.display_name),
                                        icon_url=ctx.author.avatar_url)
                embed_tickle.set_author(name=ctx.me.display_name,
                                        icon_url=ctx.me.avatar_url)
            await ctx.send(embed=embed_tickle)

    @commands.command()
    async def feed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekos.life/api/v2/img/feed") as r:
                data = await r.json()
                embed_feed = Embed(
                    title='Feed!',
                    description=f'*{ctx.author.display_name} feeds {member.display_name}~*',
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Color.red())
                embed_feed.set_image(url=data['url'])
                embed_feed.set_footer(text="{}".format(ctx.author.display_name),
                                      icon_url=ctx.author.avatar_url)
                embed_feed.set_author(name=ctx.me.display_name,
                                      icon_url=ctx.me.avatar_url)
            await ctx.send(embed=embed_feed)

    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekos.life/api/v2/img/poke") as r:
                data = await r.json()
                embed_poke = Embed(
                    title='Poke!',
                    description=f'*{ctx.author.display_name} pokes {member.display_name}~*',
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Color.red())
                embed_poke.set_image(url=data['url'])
                embed_poke.set_footer(text="{}".format(ctx.author.display_name),
                                      icon_url=ctx.author.avatar_url)
                embed_poke.set_author(name=ctx.me.display_name,
                                      icon_url=ctx.me.avatar_url)
            await ctx.send(embed=embed_poke)

    @commands.command()
    async def kill(self, context, member: discord.Member):

        author = context.message.author.mention
        mention = member.mention

        kill = "{0} killed {1} :/ "

        choices = ['https://cdn.discordapp.com/attachments/801475977158459432/801518210968846366/tenor_4.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801519256146804818/tenor_5.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801519490000879686/tumblr_mwobunzhg01rcj8eco1_500.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801519675317813329/m8ZtlNO.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801519872319422535/original.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801520070357680128/148903.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=kill.format(author, mention),
                              colour=discord.Color(random.randint(0x000000, 0xFFFFFF)))
        embed.set_image(url=image)
        embed.set_footer(text=f'Rest in Peace ')
        await context.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx: commands.Context, user: discord.Member):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/kiss') as r:
                res = await r.json()
                if user == ctx.author:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** kisses themselves ",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** kisses **{user.name}**",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)

    @commands.command()
    async def slap(self, context, member: discord.Member):

        author = context.message.author.mention
        mention = member.mention

        slap = "{0} slaps {1} :/"

        choices = ['https://cdn.discordapp.com/attachments/801475977158459432/801510342403686410/giphy_1.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801510284715360310/tenor_1.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801510804813643797/tenor_2.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801510840687132672/fm49srQ.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801511230727913562/yROjYng.gif',
                   'https://cdn.discordapp.com/attachments/801475977158459432/801511379881820200/tenor_3.gif']

        image = random.choice(choices)

        embed = discord.Embed(description=slap.format(author, mention),
                              colour=discord.Color(random.randint(0x000000, 0xFFFFFF)))
        embed.set_image(url=image)
        embed.set_footer(text=f'Ouhh :c that hurts!')
        await context.send(embed=embed)

    @commands.command()
    async def hug(self, ctx: commands.Context, user: discord.Member):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://shiro.gg/api/images/hug') as r:
                res = await r.json()
                if user == ctx.author:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** hugs themselves!",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** hugs **{user.name}**",
                        color=discord.Colour.random()
                    )
                    embed.set_image(url=res['url'])
                    await ctx.reply(embed=embed)


    @commands.command()
    async def magicball(self, ctx, *, question):
        responses = ['As I see it, yes.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don’t count on it.',
                     'It is certain.',
                     'It is decidedly so.',
                     'Most likely.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Outlook good.',
                     'Reply hazy, try again.',
                     'Signs point to yes.',
                     'Very doubtful.',
                     'Without a doubt.',
                     'Yes.',
                     'Yes – definitely.',
                     'You may rely on it.']

        choices = [
            "https://cdn.discordapp.com/attachments/801475977158459432/802485153841545246/9d2692b51ebf08955da879128c57ab69.gif",
            "https://cdn.discordapp.com/attachments/801475977158459432/802485412382638090/tenor.gif",
            "https://cdn.discordapp.com/attachments/801475977158459432/802485599125635092/tenor_7.gif",
            "https://cdn.discordapp.com/attachments/801475977158459432/802485712670556190/tenor_8.gif"]

        image = random.choice(choices)

        embed = discord.Embed(title=f'{random.choice(responses)}', colour=discord.Color.random())
        embed.set_image(url=image)
        embed.set_footer(text=f'This answers are random!')
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx):
        embed = discord.Embed(title='Here you go buddy.',
                              color=discord.Color.random())
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ship(self, ctx, name1 : clean_content, name2 : clean_content):
        shipnumber = random.randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(",
                                                            'Just "friends"',
                                                            '"Friends"',
                                                            "Little to no love ;(",
                                                            "There's barely any love ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone",
                                                     "Still in that friendzone ;(",
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!",
                                                     "But there's a small bit of love somewhere",
                                                     "I sense a small bit of love!",
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!",
                                                      "There is a bit of love there...",
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO",
                                                          "It appears one sided!",
                                                          "There's some potential!",
                                                          "I sense a bit of potential!",
                                                          "There's a bit of romance going on here!",
                                                          "I feel like there's some romance progressing!",
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!",
                                                      "There's some love in the air!",
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!",
                                                       "I can see the love is there! Somewhere...",
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!",
                                                              "I can definitely feel the love",
                                                              "I feel the love! There's a sign of a match!",
                                                              "There's a sign of a match!",
                                                              "I sense a match!",
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!",
                                                           "There's a match made in heaven!",
                                                           "It's definitely a match!",
                                                           "Love is truely in the air!",
                                                           "Love is most definitely in the air!"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                        ":sparkling_heart:",
                                                                                                        ":heart_decoration:",
                                                                                                        ":heart_exclamation:",
                                                                                                        ":heartbeat:",
                                                                                                        ":heartpulse:",
                                                                                                        ":hearts:",
                                                                                                        ":blue_heart:",
                                                                                                        ":green_heart:",
                                                                                                        ":purple_heart:",
                                                                                                        ":revolving_hearts:",
                                                                                                        ":yellow_heart:",
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun commands are ready!")


def setup(bot):
    bot.add_cog(fun(bot))