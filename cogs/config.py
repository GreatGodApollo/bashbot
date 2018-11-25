from discord.ext import commands

from bot import session
from permissions import admincheck, guildonly
from utils.db_declarative import ServerConfig


class Config:
    """Configuration Cog"""

    def __init__(self, bot):
        self.bot = bot

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @commands.check(guildonly)
    @commands.check(admincheck)
    @commands.group(pass_context=True)
    async def config(self, ctx):
        """The base config command"""
        if ctx.invoked_subcommand is None:
            await self.send_cmd_help(ctx)
        else:
            pass

    @commands.check(guildonly)
    @commands.check(admincheck)
    @config.command(pass_context=True)
    async def set(self, ctx, option: str, *, value: str):
        """Sets a Configuration Value"""
        serverconf = session.query(ServerConfig).filter(ServerConfig.serverId == ctx.message.server.id).one()
        opt = option.lower()
        if opt == "adminrole":
            serverconf.adminRole = value
        elif opt == "modrole":
            serverconf.modRole = value
        else:
            await self.bot.say("Invalid option `{}`".format(option))
            return
        session.commit()
        await self.bot.say("Configuration Updated")

    @commands.check(guildonly)
    @commands.check(admincheck)
    @config.command(pass_context=True)
    async def get(self, ctx, option: str):
        """Gets a configuration value"""
        serverconf = session.query(ServerConfig).filter(ServerConfig.serverId == ctx.message.server.id).one()
        opt = option.lower()
        if opt == "adminrole":
            await self.bot.say("The current value for `adminRole` is {}.".format(serverconf.adminRole))
        elif opt == "modrole":
            await self.bot.say("The current value for `modRole` is {}.".format(serverconf.modRole))
        else:
            await self.bot.say("Invalid option `{}`".format(option))

    @commands.check(guildonly)
    @commands.check(admincheck)
    @config.command(pass_context=True)
    async def list(self, ctx):
        """List all configuration values"""
        serverconf = session.query(ServerConfig).filter(ServerConfig.serverId == ctx.message.server.id).one()
        servername = ctx.message.server.name
        serverid = ctx.message.server.id
        adminrole = serverconf.adminRole
        modrole = serverconf.modRole
        await self.bot.say("```\n"
                           "Listing all configuration values for '{0}' ({1})\n\n"
                           "modRole: {2}\n"
                           "adminRole: {3}\n"
                           "```".format(servername, serverid, modrole, adminrole))


def setup(bot):
    bot.add_cog(Config(bot))
