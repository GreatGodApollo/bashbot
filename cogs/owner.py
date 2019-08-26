import string
import discord
import asyncio
from bot import session
from permissions import ownercheck
from discord.ext import commands

from utils.db_declarative import ServerConfig


class Owner:
    """Owner commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["o"])
    async def owner(self, ctx):
        """The base owner command"""
        if ownercheck(ctx) and ctx.invoked_subcommand is None:
            await self.bot.say("You are root")
        elif not ownercheck(ctx) and ctx.invoked_subcommand is None:
            await self.bot.say("You are not root")

    @commands.check(ownercheck)
    @owner.command(pass_context=True, hidden=True)
    async def testing(self, ctx):
        await self.bot.say("Just a generic testing command")

    @commands.check(ownercheck)
    @owner.command(pass_context=True, aliases=["eval"])
    async def debug(self, ctx, *, code):
        """Evaluate code"""

        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.server
        global_vars['session'] = session

        try:
            result = eval(code, global_vars, locals())
            if asyncio.iscoroutine(result):
                result = await result
            result = str(result)  # the eval output was modified by me but originally submitted by DJ electro
            if len(result) > 2000:
                err2 = Exception("TooManyChars")
                raise err2
            embed = discord.Embed(title="✅ Evaluated successfully.", color=0x80ff80)
            embed.add_field(name="Input :inbox_tray:", value="```" + code + "```")
            embed.add_field(name="Output :outbox_tray:", value="```" + result + "```")
            await self.bot.say(embed=embed)
        except Exception as error:
            if str(type(error).__name__ + str(error)) == "HTTPException: BAD REQUEST (status code: 400)":
                return
            else:
                embed = discord.Embed(title="❌ Evaluation failed.", color=0xff0000)
                embed.add_field(name="Input :inbox_tray:", value="```" + code + "```", inline=True)
                embed.add_field(name="Error <:error2:442590069082161163>",
                                value='```{}: {}```'.format(type(error).__name__, str(error)))
                await self.bot.say(embed=embed)
                return

    @commands.check(ownercheck)
    @owner.command(pass_context=True)
    async def importconfig(self, ctx, modrole: str, adminrole: str):
        """Import servers to the DB"""
        msg = await self.bot.say("Importing servers to the DB")
        for r in self.bot.servers:
            new_server = ServerConfig(serverId=r.id, adminRole=adminrole, modRole=modrole)
            session.add(new_server)
            session.commit()
        await self.bot.edit_message(msg, "Finished importing servers to the DB")

    @commands.check(ownercheck)
    @owner.command(pass_context=True, aliases=["incmn"])
    async def incrementalmassnick(self, ctx, start_at: int, *, name):
        """Incremental MassNick"""
        await self.bot.say(f"Incrementally renaming users to {name}{start_at}")

        x = start_at
        for user in ctx.message.server.members:
            try:
                await self.bot.change_nickname(user, f"{name}{x}")
                x += 1
            except:
                continue
        await self.bot.say("Finished Incremental MassNick")

    @commands.check(ownercheck)
    @owner.command(pass_context=True, aliases=["mn"])
    async def massnick(self, ctx, *, name=""):
        """MassNick"""
        if name is "":
            msgToSend = "Un-nicknaming users"
        else:
            msgToSend = f"Renaming users to {name}"
        msg = await self.bot.say(msgToSend)
        for user in ctx.message.server.members:
            try:
                await self.bot.change_nickname(user, f"{name}")
            except:
                continue
        await self.bot.edit_message(msg, "Finished MassNick")

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)


def setup(bot):
    bot.add_cog(Owner(bot))
