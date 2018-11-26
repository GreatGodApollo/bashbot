import asyncio

import discord
from discord.ext import commands

from permissions import modcheck, guildonly
from utils.mutes import *


class Hidden:
    """Gets a reaction, and performs an action"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def hidden(self, ctx):
        """The base Hidden command"""
        bot = self.bot
        if ctx.invoked_subcommand is None:
            pages = bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await bot.send_message(ctx.message.channel, page)

    @hidden.command(pass_context=True)
    async def message(self, ctx, *, msgToReplace):
        """Creates a hidden message"""
        await self.bot.delete_message(ctx.message)
        msg = await self.bot.send_message(ctx.message.channel,
                                          "This message is hidden, react for it to be revealed\nHidden by: " +
                                          ctx.message.author.name + "#" + ctx.message.author.discriminator)
        await self.bot.add_reaction(msg, "❌")

        def check(reaction, user):
            return user != self.bot.user

        res = await self.bot.wait_for_reaction(message=msg, check=check, timeout=120)
        if res is not None:
            await self.bot.edit_message(msg, msgToReplace + "\nHidden by: " + ctx.message.author.name +
                                        ctx.message.author.discriminator + "\nRevealed by: "
                                        + res.user.name + "#" + res.user.discriminator)
        else:
            await self.bot.edit_message(msg, "This hidden message expired")
        await self.bot.clear_reactions(msg)

    @commands.check(guildonly)
    @commands.check(modcheck)
    @hidden.command(pass_context=True, hidden=True)
    async def mute(self, ctx, emote, *, msg):
        """Creates a message that mutes people on reaction"""
        await self.bot.delete_message(ctx.message)
        mesg = await self.bot.send_message(ctx.message.channel, msg)
        try:
            await self.bot.add_reaction(mesg, emote)
        except:
            try:
                await self.bot.add_reaction(mesg, '😄')
            except:
                await self.bot.edit_message(mesg, "I don't have the proper permissions to add reactions")
                return

        def check(reaction, user):
            return user != self.bot.user
        res = await self.bot.wait_for_reaction(message=mesg, check=check, timeout=120)
        if res is not None:
            role = discord.utils.get(ctx.message.server.roles, name='Muted')
            if role is not None:
                res = await mute(self.bot, ctx.message.server.roles, res.user.id)
                if res:
                    await self.bot.edit_message(mesg, "User {0} muted.".format(res.user.mention))
                else:
                    self.bot.say("I'm missing permissions!")
            else:
                permsoverwrite = discord.PermissionOverwrite()
                permsoverwrite.send_messages = False
                perms = discord.Permissions(send_messages=False, read_messages=True)
                role = await self.bot.create_role(ctx.message.server, name="Muted", permissions=perms)
                for channel in ctx.message.server.channels:
                    await self.bot.edit_channel_permissions(channel, role, permsoverwrite)
                res = await mute(self.bot, ctx.message.server.roles, res.user.id)
                if res:
                    await self.bot.edit_message(mesg, "User {0} muted.".format(res.user.mention))
                else:
                    self.bot.say("I'm missing permissions!")
        await asyncio.sleep(1)
        await self.bot.delete_message(mesg)


def setup(bot):
    bot.add_cog(Hidden(bot))
