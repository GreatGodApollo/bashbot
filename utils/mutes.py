from datetime import datetime, timedelta

import discord

from bot import session
from utils.db_declarative import ServerMutes


async def un_mute(bot, serverid, userid):

    try:
        row = session.query(ServerMutes).filter(ServerMutes.serverId == serverid).filter(ServerMutes.userId == userid).one()
    except:
        row = None

    if row is not None:
        server = discord.utils.get(bot.servers, id=serverid)
        role = discord.utils.get(server.roles, name='Muted')
        user = discord.utils.get(server.members, id=userid)
        await bot.remove_roles(user, role)
        session.delete(row)
        session.commit()
        await bot.send_message(user, f"You have been unmuted in {server.name}")
        return True
    else:
        return False


async def mute(bot, serverid, userid):
    try:
        prerow = session.query(ServerMutes).filter(ServerMutes.userId == userid).filter(ServerMutes.serverId == serverid).one()
    except:
        prerow = None
    if prerow is None:
        server = discord.utils.get(bot.servers, id=serverid)
        role = discord.utils.get(server.roles, name='Muted')
        user = discord.utils.get(server.members, id=userid)
        await bot.add_roles(user, role)
        new_mute = ServerMutes(serverId=serverid, userId=userid)
        session.add(new_mute)
        session.commit()
        await bot.send_message(user, f"You have been muted in {server.name}")
        return True
    else:
        return False

