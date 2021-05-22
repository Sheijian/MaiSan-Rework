# This is the main file of the bot. set your token and modify or remove the status task.
# Help commands should match to your bots commands :)

import discord
from discord.ext import commands
import asyncio

#set variable and prefix
bot = commands.Bot(command_prefix='ms!', help_command=None)

#load the cogs
cogs = ['fun', 'mod', 'owner', 'anime', 'math', 'misc', 'giveaway', 'RussianRoulette', 'stats',
        'Economy', 'Tickets', 'Levelsystem', 'Warn']
for cog in cogs:
    bot.load_extension(f'cogs.{cog}')


#help commands
@bot.command()
async def help(ctx):
    em = discord.Embed(title='Help!', color=discord.Color.random())
    em.add_field(name='Math', value=f'ms!math-help to see my math commands. \n')
    em.add_field(name='Moderation', value='ms!mod-help to see my mod commands. \n')
    em.add_field(name='Giveaway', value='ms!g-help to see my giveaway commands. \n')
    em.add_field(name='Fun', value='ms!fun-help to see my fun commands. \n')
    em.add_field(name='Anime', value='ms!ani-help to see my anime commands. \n')
    em.add_field(name='Music', value='ms!music-help to see my music commands. \n')
    em.add_field(name='Economy', value='ms!economy-help to see my economy commands. \n')
    em.add_field(name='Tickets', value='ms!ticket-help to see my tickets commands. \n')
    em.add_field(name='Level', value='ms!level-help to see my level commands. \n')
    em.add_field(name=f'Information', value='ms!info-help to see my info commands. \n')
    em.add_field(name='Invite', value="Gives you the Link you can invite me with. \n")
    em.set_footer(text="Im searching for a second discord.py dev for the Bot rn. Dm me if you are interested"
                  , icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name="mod-help", aliases=["mod", "moderation"])
async def modhelp(ctx):
    em = discord.Embed(title="** <a:ModTime:806589420211273728> Moderation Help**", color=discord.Color.random())
    em.add_field(name='ban <member>', value="Ban the tagged User. \n")
    em.add_field(name='kick <member>', value="Kick the tagged User. \n")
    em.add_field(name='purge <amount>', value="Clear the wished amount messages \n")
    em.add_field(name='addrole <member> <role>', value="Add a role to a member \n")
    em.add_field(name='roles', value="Show you the role list in the server \n")
    em.add_field(name='lock', value="Locks the current channel (not for mods) \n")
    em.add_field(name='unlock', value="Unlocks the current channel) \n")
    em.add_field(name='createchannel <role whith acces> <name>', value='Creates the channel \n')
    em.add_field(name='deletechannel <name>', value='Deletes the channel \n')
    em.add_field(name='createcategory <role with acces> <name>', value='Creates the category \n')
    em.add_field(name='deletecategory <name>', value='Deletes the category \n')
    em.add_field(name='createrole <name>', value="Creates a role with the given informations \n")
    em.add_field(name='mcount', value="Show you how many messages was written in this channel ")
    em.set_footer(text="Thanks for using me! :)", icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name="fun-help", aliases=["fun"])
async def funhelp(ctx):
    em = discord.Embed(title="**Fun Help**", color=discord.Color.random())
    em.add_field(name='Praise', value='Praise! \n')
    em.add_field(name='css', value='just try it. \n')
    em.add_field(name='countdown', value='Starts a five second countdown. \n')
    em.add_field(name='neko', value='Shows you a cat picture \n')
    em.add_field(name='random', value='number, between member, coin flip \n')
    em.add_field(name='stone <member>', value='Trow a little stone at the tagged member. \n')
    em.add_field(name='hype', value='feel the hype. \n')
    em.add_field(name='joke', value='in germany we say: Die sind flach. \n')
    em.add_field(name='pat <member>', value='pat the tagged member. \n')
    em.add_field(name='kill <member>', value='kill the tagged member. \n')
    em.add_field(name='slap <member>', value='slap the tagged member. \n')
    em.add_field(name='hug <member>', value='hug the tagged member. \n')
    em.add_field(name='poke <member>', value='poke the tagged member. \n')
    em.add_field(name='feeding <member>', value='feed the tagged member. \n')
    em.add_field(name='tickle <member>', value='tickle the tagged member. \n')
    em.add_field(name='Magicball <question>', value='Ask the magicball your question. \n')
    em.add_field(name='Avatar', value='shows you your avatar. \n')
    em.add_field(name='Timer <time in seconds>', value='When the timer expires the bot will tag you.')
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name='math-help', aliases=["math"])
async def math_help(ctx):
    em = discord.Embed(title='**Math Help**', color=discord.Color.random())
    em.add_field(name='square <number1> <number2>', value="square number 1 with number 2 \n")
    em.add_field(name='divide <number1> <number2>', value="divide number 1 with number 2 \n")
    em.add_field(name='multiply <number1> <number2>', value="multiply number 1 with number 2 \n")
    em.add_field(name='subtract <number1> <number2>', value="subtract number 1 with number 2 \n")
    em.add_field(name='add <number1> <number2>', value="add number 1 with number 2 \n")
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name='info-help', aliases=["info"])
async def info_help(ctx):
    em = discord.Embed(title='**Information Help**', color=discord.Color.random())
    em.add_field(name='suggest <suggestion>', value="Sends your suggestion to the devs. \n")
    em.add_field(name='channelinfo', value="Shows you the facts about the current channel. \n")
    em.add_field(name='userinfo <member>', value="Gives you informations about a member. \n")
    em.add_field(name='userinfo', value="Shows you my on how many server i am. \n")
    em.add_field(name='support', value="Show you a list with a few ways you can support us. \n")
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name='ani-help', aliases=["anime-help"])
async def ani_help(ctx):
    em = discord.Embed(title='**Anime Help**', color=discord.Color.random())
    em.add_field(name='anime', value="Gives you a random anime advice. \n")
    em.add_field(name='animepfp', value='gives you an anime profile picture.\n')
    em.add_field(name='animepfp2', value='pfp from another source.\n')
    em.add_field(name='wallpaper', value='gives you a wallpaper.\n')
    em.add_field(name='wallpaper2', value='wallpaper from another source.\n')
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name='g-help', aliases=["giveaway", "giveaway-help"])
async def g_help(ctx):
    em = discord.Embed(title='**Giveaway Help**', color=discord.Color.random())
    em.add_field(name='gstart', value="Starts a giveaway \n")
    em.add_field(name='greroll', value="Rerolls the giveaway \n")
    em.set_footer(text='ms!invite if you want to support me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name="Ticket-help", aliases=["ticket", 'Tickets'])
async def ticket_help(ctx):
    em = discord.Embed(title='**Ticket Help**', color=discord.Color.random())
    em.add_field(name='ticketrole <@role> <reason>', value='Set the team-role that should have access to the tickets.')
    em.add_field(name='new <reason>', value='to open a new ticket')
    em.add_field(name='setticketlog <#channel>', value='set the ticket-log channel')
    em.add_field(name='close <#channel', value='close the ticket')
    await ctx.send(embed=em)


@bot.command(name='rr-help')
async def rr_help(ctx):
    em = discord.Embed(title='**Reaction Role Help**', color=discord.Color.random())
    em.add_field(name='reactionrole(rr)', value=" add a reaction role to the tagged message. \n")
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name='economy-help', aliases=['economy'])
async def economyhelp(ctx):
    em = discord.Embed(title='**Economy Help', color=discord.Color.random())
    em.add_field(name='balance', value='to see your cash')
    em.add_field(name='deposit <amount>', value='to dep some money')
    em.add_field(name='withdraw <amount>', value='to with some money')
    em.add_field(name='give <amount> <member>', value='give a member some of your money')
    em.add_field(name='beg', value='to beg a bit money')
    em.add_field(name='serve', value='serve and gain ;)')
    em.add_field(name='daily', value='collect every 24h money')
    em.add_field(name='weekly', value='collect every 7d money')
    em.add_field(name='shop', value='coming soon with nice items... :)')
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)



@bot.command(name="music-help", aliases=["music"])
async def music_help(ctx):
    em = discord.Embed(title='**Music Help**', color=discord.Color.random())
    em.add_field(name='join', value='Make the Bot join your channel. \n')
    em.add_field(name='leave', value='Make the Bot leave your channel. \n')
    em.add_field(name='play <yotubelink>', value='plays the song \n')
    em.add_field(name='pause', value='stops playing the current song \n')
    em.add_field(name='resume', value='resumes the current song \n')
    em.add_field(name='stop', value='stops playing the current song')
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)


@bot.command(name="level-help")
async def levelhelp(ctx):
    em = discord.Embed(title='**Level Help**', color=discord.Color.random())
    em.add_field(name='rank', value='shows you your rank')
    em.set_footer(text='ms!invite if you want to invite me :)', icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)

#bot's status
@bot.event
async def status_task():

        while True:
            await bot.change_presence(activity=discord.Game('1'),
                                        status=discord.Status.online)
            await asyncio.sleep(15)
            await bot.change_presence(activity=discord.Game('2'), status=discord.Status.online)
            await asyncio.sleep(15)
            await bot.change_presence(activity=discord.Game('3'), status=discord.Status.online)
            await asyncio.sleep(15)
            await bot.change_presence(activity=discord.Game('4'),
                                        status=discord.Status.online)
            await asyncio.sleep(15)
            bot.loop.create_task(status_task())

#print event and run the status task
@bot.event
async def on_ready():
    print("im online")
    bot.loop.create_task(status_task())


#run the bot
bot.run("your token here")
