import discord
from discord.ext import commands

import asyncio
import random


class RussianRoulette(commands.Cog, name="Games"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def russianroulette(self, ctx, *adversaries: discord.Member):
        await ctx.send("https://tenor.com/view/gun-pistol-revolver-gif-9832859")
        await ctx.send(
            "Russian Roulette game!! "
            "Take the gun, spin the barrel, shoot and hope to survive!"
        )

        players = list(adversaries)
        if len(players) == 0:
            players.append(self.bot.user)

        players.insert(0, ctx.author)
        NUMBER_OF_PLAYERS = len(players)
        turn = 0

        def checkresponse(m):
            return m.channel == ctx.channel and m.author == players[turn]

        # MAIN LOOP
        while True:
            await ctx.send(f"{players[turn].mention}, type s (shoot) or q (quit)")
            if players[turn] != self.bot.user:
                try:
                    m = await self.bot.wait_for(
                        "message", timeout=30.0, check=checkresponse
                    )
                except asyncio.TimeoutError:
                    await ctx.send(
                        "Stopping russian roulette, timeout expired\n"
                        + f"{players[turn].mention} loses!"
                    )
                    return

                if m.content.lower() in ("stop", "exit", "quit", "q"):
                    await ctx.send("Stopping russian roulette")
                    return

                if m.content.lower() not in ("pow", "s", "shoot"):
                    continue

            await ctx.send("https://tenor.com/view/cameron-monaghan-gif-5508114")
            await asyncio.sleep(1)

            if random.randint(0, 5):
                await ctx.send(
                    f"{players[turn].mention}, click... you are lucky, my friend..."
                )
                turn = (turn + 1) % NUMBER_OF_PLAYERS
            else:
                await ctx.send(
                    f"***POW!!!!*** {players[turn].mention} got shot and died."
                )
                return

    @commands.Cog.listener()
    async def on_ready(self):
        print("RussianRoulette is ready!")


def setup(bot: commands.Bot):
    bot.add_cog(RussianRoulette(bot))