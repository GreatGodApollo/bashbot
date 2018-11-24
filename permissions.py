import discord

from bot import session
from config import Config
from utils.db_declarative import ServerConfig


def ownercheck(ctx):
    return ctx.message.author.id in Config.owners

def serverownercheck(ctx):
    return ctx.message.author == ctx.message.server.owner

def admincheck(ctx):

    roles = ctx.message.server.roles
    try:
        serverconf = session.query(ServerConfig).filter(ServerConfig.serverId == ctx.message.server.id).one()
        rolename = serverconf.adminRole
        if rolename:
            role = discord.utils.get(roles, name=rolename)
            return role in ctx.message.author.roles or serverownercheck(ctx) or ownercheck(ctx)
    except Exception as e:
        print(e)
        return ownercheck(ctx)

def modcheck(ctx):

    roles = ctx.message.server.roles
    try:
        serverconf = session.query(ServerConfig).filter(ServerConfig.serverId == ctx.message.server.id).one()
        rolename = serverconf.modRole
        if rolename:
            role = discord.utils.get(roles, name=rolename)
            return role in ctx.message.author.roles or admincheck(ctx)
    except Exception as e:
        print(e)
        return ownercheck(ctx)