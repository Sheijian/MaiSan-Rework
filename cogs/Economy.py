import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import aiosqlite
import random


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('BankCommands are ready!')
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS users (userid INTEGER, bank INTEGER, wallet INTEGER);")
                await connection.commit()

    @commands.command(aliases=['bal'])
    @cooldown(1, 5, BucketType.channel)
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM users WHERE userid = ?", (member.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)", (member.id, 0, 0))
                    await cursor.execute("SELECT * FROM users WHERE userid = ?", (member.id,))
                    rows = await cursor.fetchone()
                await connection.commit()
                em = discord.Embed(title=f" {member.name}'s Balance",
                                   color=ctx.author.color)
                em.add_field(name=":dollar: Wallet Balance:", value=f"{rows[2]} :coin:")
                em.add_field(name=":bank: Bank Balance:", value=f"{rows[1]} :coin:")
                em.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=em)

    @commands.command(aliases=['dep'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount=None):
        if amount == None:
            em = discord.Embed(title=" Deposit failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You didn't provide an amount. Or go to school!")
            em.add_field(name="Next Steps:", value="Next time try to type an amount too!")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            return

        if amount != "all" or amount != "max":
            amount = int(amount)

        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?", (ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",
                                         (ctx.author.id, 0, 0, ''))
                else:
                    if amount != 'all' or amount != "max":
                        if amount > rows[1]:
                            em = discord.Embed(title=" Deposit failed!",
                                               color=ctx.author.color)
                            em.add_field(name="Reason:", value="You don't even have that much money!")
                            em.add_field(name="Next Steps:", value="Get richer next time!")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                            return
                        elif amount <= 0:
                            em = discord.Embed(title=" Deposit failed!",
                                               color=ctx.author.color)
                            em.add_field(name="Reason:", value="Amount was too low!")
                            em.add_field(name="Next Steps:", value="Type a positive integer next time!")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                            return
                        else:
                            await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                                 (rows[1] - amount, rows[0] + amount, ctx.author.id,))
                            em = discord.Embed(title=" Deposit successful!",
                                               color=ctx.author.color)
                            em.add_field(name=":bank: Amount Deposited:", value=f"{amount} :coin:")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                    else:
                        await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                             (0, rows[0] + rows[1], ctx.author.id,))
                        em = discord.Embed(title=" Deposit successful!",
                                           color=ctx.author.color)
                        em.add_field(name=":bank: Amount Deposited:", value=f"{rows[1]} :coin:")
                        em.set_thumbnail(url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                    await connection.commit()

    @commands.command(aliases=['with'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        if amount == None:
            em = discord.Embed(title=" Withdraw failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You didn't provide an amount. Or go to school!")
            em.add_field(name="Next Steps:", value="Next time try to type an amount too!")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            return

        if not amount == 'all':
            amount = int(amount)
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?", (ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",
                                         (ctx.author.id, 0, 0,))
                else:
                    if not amount == 'all':
                        if amount > rows[0]:
                            em = discord.Embed(title=" Withdraw failed!",
                                               color=ctx.author.color)
                            em.add_field(name="Reason:", value="You don't even have that much money!")
                            em.add_field(name="Next Steps:", value="Get richer next time!")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                            return
                        elif amount <= 0:
                            em = discord.Embed(title=" Withdraw failed!",
                                               color=ctx.author.color)
                            em.add_field(name="Reason:", value="Amount was too low!")
                            em.add_field(name="Next Steps:", value="Type a positive integer next time!")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                            return
                        else:
                            await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                                 (rows[1] + amount, rows[0] - amount, ctx.author.id,))
                            em = discord.Embed(title=" Withdraw successful!",
                                               color=ctx.author.color)
                            em.add_field(name=":dollar: Amount Withdrawn:", value=f"{amount} :coin:")
                            em.set_thumbnail(url=ctx.author.avatar_url)
                            await ctx.send(embed=em)
                    else:
                        await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                             (rows[1] + rows[0], 0, ctx.author.id,))
                        em = discord.Embed(title=" Withdraw successful!",
                                           color=ctx.author.color)
                        em.add_field(name=":dollar: Amount Withdrawn:", value=f"{rows[0]} :coin:")
                        em.set_thumbnail(url=ctx.author.avatar_url)
                        await ctx.send(embed=em)
                await connection.commit()

    @commands.command(aliases=['send', "share"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def give(self, ctx, member: discord.Member = None, amount=None):
        if amount == None:
            em = discord.Embed(title=" Give failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You didn't provide an amount. Or go to school!")
            em.add_field(name="Next Steps:", value="Next time try to type an amount too!")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            return
        if member is None:
            em = discord.Embed(title=" Give failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You didn't provide a valid member. Get better at discord!")
            em.add_field(name="Next Steps:", value="Next time try to type a valid member too!")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            return

        amount = int(amount)

        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?", (ctx.author.id))
                bal = await cursor.fetchone()

                if not bal:
                    return await ctx.send("bruh, you've never even played-")

                if bal[1] < amount:
                    return await ctx.send("You don't even have that much money!")

                if amount == 0 or amount < 0:
                    await ctx.send("Amount must be positive!")
                    return

                em = discord.Embed(title=" Give successful!", color=ctx.author.color)
                em.add_field(name=":dollar: Amount Given:", value=f"{amount} :coin:")
                em.add_field(name="Member:", value=f"{member.mention}")
                em.add_field(name=":tada: Money:", value="Give your money! :tada:")
                await ctx.send(embed=em)

                await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                     (bal[1] - amount, bal[0], ctx.author.id))
                await connection.commit()

        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?", (member.id))
                rows = await cursor.fetchone()

                await cursor.execute("UPDATE users SET wallet = ?, bank = ?, WHERE userid = ?",
                                     (rows[1] + amount, rows[0], member.id))
                await connection.commit()

    # error handling
    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f" Slow it down C'mon", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"Stop giving money it makes you poor!")
            em.add_field(name="Try again in:", value="{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=f" Give Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"Arguments were of the wrong data type!")
            em.add_field(name="Args", value="```\nimp give <@user> <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(title=f" Give Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"You didn't provide the right arguments!")
            em.add_field(name="Args", value="```\nimp give <@user> <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f" Slow it down C'mon", color=ctx.author.color)
            em.add_field(name=f"Reason:", value="You can always withdraw later idiot!")
            em.add_field(name="Try again in:", value="{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=f" Withdraw Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"Arguments were of the wrong data type!")
            em.add_field(name="Args", value="```\nimp with <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(title=f" Withdraw Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"You didn't provide the right arguments!")
            em.add_field(name="Args", value="```\nimp with <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f" Slow it down C'mon", color=ctx.author.color)
            em.add_field(name=f"Reason:",
                         value="Check it later, money doesn't matter. Adding me to your server does \:D")
            em.add_field(name="Try again in:", value="{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)

        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=f" Balance Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"Arguments were of the wrong data type!")
            em.add_field(name="Args", value="```\nimp balance [@user]\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f" Slow it down C'mon", color=ctx.author.color)
            em.add_field(name=f"Reason:", value="You can always deposit later idiot!")
            em.add_field(name="Try again in:", value="{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(title=f" Deposit Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"Arguments were of the wrong data type!")
            em.add_field(name="Args", value="```\nimp deposit <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(title=f" Deposit Error", color=ctx.author.color)
            em.add_field(name=f"Reason:", value=f"You didn't provide the right arguments!")
            em.add_field(name="Args", value="```\nimp dep <amount>\n```")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    async def bet(self, ctx, amount=None):
        if amount is None:
            em = discord.Embed(title=" Bet failed!", color=ctx.author.color)
            em.add_field(name="Reason:", value="You didn't provide an amount. Or go to school!")
            em.add_field(name="Next Steps:", value="Next time try to type an amount too!")
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            return

        if amount != 'all':
            amount = int(amount)

        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?", (ctx.author.id))
                rows = await cursor.fetchone()

                if not rows:
                    await ctx.send("bruh you haven't even played-")
                    return

                if rows[1] < amount:
                    em = discord.Embed(title=" Bet failed!", color=ctx.author.color)
                    em.add_field(name="Reason:", value="You don't even have that much money!")
                    em.add_field(name="Next Steps:", value="Get richer next time!")
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await ctx.send(embed=em)
                    return

                if amount == 0 or amount < 0:
                    em = discord.Embed(title=" Bet failed!", color=ctx.author.color)
                    em.add_field(name="Reason:", value="Amount was too low!")
                    em.add_field(name="Next Steps:", value="Type a positive integer next time!")
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await ctx.send(embed=em)
                    return

                res = random.choice(["Won", "Lost"])
                if res == "Won":
                    em = discord.Embed(title=" Bet Won!", color=ctx.author.color)
                    em.add_field(name="Money Earned:", value=f"{amount}")
                elif res == "Lost":
                    em = discord.Embed(title=" Bet Lost!", color=ctx.author.color)
                    em.add_field(name="Money Lost:", value=f"{amount}")
                em.add_field(name="Result:", value=f"{res}")

                if res == "Won":
                    await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                         (rows[1] + amount, rows[0], ctx.author.id))
                elif res == "Lost":
                    await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",
                                         (rows[1] - amount, rows[0], ctx.author.id))


    async def leaderboard(self, entries):
        embed = discord.Embed(title='🏆 Top 10 users 🏆',
                              description='Sorted by the total of wallet and bank balance combined')
        place = 0

        for row in entries:
            place += 1
            user = row[0]
            embed.add_field(name=f'{user}',
                            value=f"**Bank:** {row[1]}\n**Wallet:** {row[2]}\n**Total:** {row[1] + row[2]}",
                            inline=False)
        return embed


    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def beg(self, ctx):
        earnings = random.randint(
        1, 100
        )
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?",(ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",(ctx.author.id,0,0))
                    await connection.commit()
                await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",(rows[1] + earnings, rows[0], ctx.author.id))
                rows = await cursor.fetchone()
                await connection.commit()
                em = discord.Embed(title = f" {ctx.author.name} begs hard!", color = ctx.author.color)
                em.add_field(name = ":coin: Earnings", value = f"{earnings} :coin:", inline = False)
                em.set_thumbnail(url = ctx.author.avatar_url)
                em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def devwith(self, ctx, amount = None):
        if amount is None:
            await ctx.send("Type an amount!")
            return
        if not amount == 'all':
            amount = int(amount)
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?",(ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",(ctx.author.id,0,0,))
                else:
                    if not amount == 'all':
                        await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?", (rows[1] + amount, rows[0], ctx.author.id))
            await connection.commit()
        await ctx.send(f"Gave you {amount} :dollar:")

    @commands.command()
    @cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        earnings = 2000
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?",(ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",(ctx.author.id,0,0))
                await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",(rows[1] + earnings, rows[0], ctx.author.id))
                rows = await cursor.fetchone()
                await connection.commit()
                em = discord.Embed(title = f" {ctx.author.name} begs hard!", color = ctx.author.color)
                em.add_field(name = ":dollar: Earnings", value = f"{earnings} :coin:", inline = False)
                em.add_field(name = ":tada: Free prize:", value = "Once a day you can claim a free price!")
                em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                em.set_thumbnail(url = ctx.author.avatar_url)
                await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def serve(self, ctx):
        earnings = random.randint(
        1, 500
        )
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?",(ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",(ctx.author.id,0,0))
                await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",(rows[1] + earnings, rows[0], ctx.author.id))
                rows = await cursor.fetchone()
                await connection.commit()
                em = discord.Embed(title = f" {ctx.author.name} serves their server!", color = ctx.author.color)
                em.add_field(name = ":coin: Earnings", value = f"{earnings} :coin:", inline = False)
                em.add_field(name = "Server:", value = f"{ctx.guild.name}")
                em.set_thumbnail(url = ctx.author.avatar_url)
                em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed=em)


    @commands.command()
    @cooldown(1, 604800, BucketType.user)
    async def weekly(self, ctx):
        earnings = 15000
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT bank, wallet FROM users WHERE userid = ?",(ctx.author.id,))
                rows = await cursor.fetchone()
                if not rows:
                    await cursor.execute("INSERT INTO users (userid, bank, wallet) VALUES (?,?,?)",(ctx.author.id,0,0))
                await cursor.execute("UPDATE users SET wallet = ?, bank = ? WHERE userid = ?",(rows[1] + earnings, rows[0], ctx.author.id))
                rows = await cursor.fetchone()
                await connection.commit()
                em = discord.Embed(title = f" {ctx.author.name} begs hard!", color = ctx.author.color)
                em.add_field(name = ":dollar: Earnings", value = f"{earnings} :coin:", inline = False)
                em.add_field(name = ":tada: Free prize:", value = "Once a day you can claim a free price!")
                em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
                em.set_thumbnail(url = ctx.author.avatar_url)
                await ctx.send(embed=em)

    @commands.command()
    @cooldown(1, 20, BucketType.user)
    async def shop(self, ctx):
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM shop WHERE available = ?", (True,))
                items = await cursor.fetchall()

                em = discord.Embed(title="Shop", color=ctx.author.color)
                for item in items:
                    em.add_field(name=f"{item[1]}", value=f"Cost: {item[2]}\nID: {item[3]}")
                await ctx.channel.send(embed=em)
                await connection.commit()


    @commands.command()
    @commands.is_owner()
    async def itemadd(self, ctx, name, price: int):
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    await ctx.send("Type the availibility for this item! (True or False)")
                    msg = await self.client.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('You didn\'t answer in time, please be quicker next time!')
                    return
                else:
                    if msg.content.lower() == "true":
                        await cursor.execute("INSERT INTO shop (name, price, available) VALUES (?, ?, ?)",
                                             (name, price, True,))
                    elif msg.content.lower() == "false":
                        await cursor.execute("INSERT INTO shop (name, price, available) VALUES (?, ?, ?)",
                                             (name, price, False,))
                    await cursor.execute('SELECT id FROM shop')
                    rows = await cursor.fetchall()
                    number = rows[-1][0]
                    await cursor.execute(f'ALTER TABLE users ADD COLUMN item{number} INTEGER;')
                    await connection.commit()

        await ctx.send(f"{ctx.author.mention}, item was created!\nName: {name} | Price {price} | ID = {number}")

    @commands.command()
    @commands.is_owner()
    async def itemremove(self, ctx, item_id):
        item_id = int(item_id)
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM shop WHERE id = ? AND available = ?", (item_id, True,))
                rows = await cursor.fetchone()
                if rows:
                    await ctx.send(f"Successfully removed item `{item_id}` from the shop")
                else:
                    await ctx.send("That item doesnt exist")
                    return
                await cursor.execute("UPDATE shop SET available = ? WHERE id = ?", (False, item_id,))
                await connection.commit()

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, item_id):
        item_id = int(item_id)
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM shop WHERE id = ? AND available = ?", (item_id, False,))
                rows = await cursor.fetchone()
                if rows:
                    await ctx.send(f"Successfully enabled item `{item_id}` in the shop")
                else:
                    await ctx.send("That item doesnt exist or is enabled")
                await cursor.execute("UPDATE shop SET available = ? WHERE id = ?", (True, item_id,))
                await connection.commit()

    @commands.command()
    @commands.is_owner()
    async def edit(self, ctx, item_id, price):
        item_id = int(item_id)
        price = int(price)
        async with aiosqlite.connect("economy.db") as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE shop SET price = ? WHERE id = ?", (price, item_id,))
                await connection.commit()
        await ctx.send(f"Successfully changed price of item `{item_id}` to `{price}`")

    @serve.error
    async def serve_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = f" Slow it down C'mon", color = ctx.author.color)
            em.add_field(name = f"Reason:", value = f"Stop serving the server your in!")
            em.add_field(name = "Try again in:", value = "{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = f" Slow it down C'mon", color = ctx.author.color)
            em.add_field(name = f"Reason:", value = f"Get back to studying!")
            seconds = round(error.retry_after)
            minutes = round(seconds / 60)
            hours = round(minutes / 60)
            em.add_field(name = "Try again in:", value = f"{hours} hours, {minutes} minutes and {seconds} seconds!")
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @weekly.error
    async def weekly_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = f" Slow it down C'mon", color = ctx.author.color)
            em.add_field(name = f"Reason:", value=f"Get back to studying! Weekly prizes are called weekly for a reason!")
            em.add_field(name = "Try again in:", value = "{:.2f}s".format(error.retry_after))
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @devwith.error
    async def devwith_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = f" Slow it down C'mon", color = ctx.author.color)
            em.add_field(name = f"Reason:", value = f"Your already too rich, Lord {ctx.author.mention}!")
            em.add_field(name = "Try again in:", value = "{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = em)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title = f" Slow it down C'mon", color = ctx.author.color)
            em.add_field(name = f"Reason:", value = f"Begging makes you look poor which you are {ctx.author.mention}!")
            em.add_field(name = "Try again in:", value = "{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url = ctx.author.avatar_url)
            em.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed = em)

    @shop.error
    async def shop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f" Slow it down C'mon", color=ctx.author.color)
            em.add_field(name=f"Reason:", value="You can always see the shop idiot!")
            em.add_field(name="Try again in:", value="{:.2f} seconds".format(error.retry_after))
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Economy(client))
