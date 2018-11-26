import asyncio
import logging
import sys
import time
import traceback
import sched
from datetime import datetime

import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from utils.db_declarative import ServerConfig, Base, ServerMutes
from utils.mutes import *

logging.basicConfig(level=logging.ERROR)

# this specifies what extensions to load when the bot starts up
startup_extensions = Config.cogs

bot = commands.Bot(command_prefix=Config.prefixes, description=Config.description)
start_time = time.time()
version = "0.8"

dbengine = create_engine(Config.dburl,
                         pool_pre_ping=True)

Base.metadata.bind = dbengine
DBSession = sessionmaker(bind=dbengine)
session = DBSession()
start = 0
starttime = None

async def startmutechecks():
    while True:
        try:
            currentMutes = session.query(ServerMutes)
        except:
            currentMutes = None
            print("I couldn't connect to the DB!")
        if currentMutes is not None:
            for mutee in currentMutes:
                if datetime.utcnow() > mutee.timeToUnmute:
                    await un_mute(bot, mutee.serverId, mutee.userId)
                else:
                    pass

        await asyncio.sleep(15.00 - ((time.time() - start_time) % 15.00))



@bot.event
async def on_ready():
    global start
    global starttime
    print("------------")
    print("Bash bot v{}".format(version))
    print("------------")
    print("Logged in as")
    print(bot.user)
    print(bot.user.id)
    print("Invite me using https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8".format(bot.user.id))
    print('READY')
    await bot.change_presence(game=discord.Game(name="for {}help | v{}".format(Config.prefixes[0], version), type=3),
                              status="dnd")
    #if start is 0:
    #    start += 1
    #    starttime = time.time()
    #    await startmutechecks()


@bot.event
async def on_command_error(event, ctx):
    if isinstance(event, commands.CheckFailure):
        if "ownercheck" in str(ctx.command.checks):
            await bot.send_message(ctx.message.channel, "You are not root")
            return
        elif "guildonly" in str(ctx.command.checks):
            await bot.send_message(ctx.message.channel, ":x: Sorry, this command can only be used in servers :x:")
            return
        await bot.send_message(ctx.message.channel, ":no_entry: Access to this command is restricted.")
        return
    if isinstance(event, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
        return
    if isinstance(event, commands.CommandNotFound):
        pass
    if isinstance(event, commands.errors.BadArgument):
        await send_cmd_help(ctx)
        return
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(event), event, event.__traceback__, file=sys.stderr)


@bot.event
async def on_server_join(server):
    new_server = ServerConfig(serverId=server.id, adminRole="Administrator", modRole="Moderator")
    session.add(new_server)
    session.commit()

@bot.event
async def on_server_remove(server):
    session.query(ServerConfig).filter(ServerConfig.serverId == server.id).delete()
    session.commit()


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to install package {}\n{}'.format(extension, exc))

    bot.run(Config.token)
