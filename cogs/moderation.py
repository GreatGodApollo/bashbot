import discord
from discord.ext import commands

from permissions import modcheck, guildonly
from utils.mutes import *


class Moderation:
    """Moderation Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.check(guildonly)
    @commands.check(modcheck)
    @commands.command(pass_context=True)
    async def unmute(self, ctx,  user: discord.User):
        """The simple yet majestic unmute command"""
        res = await un_mute(self.bot, ctx.message.server.id, user.id)
        if res is True:
            await self.bot.say("User {0} unmuted.".format(user.mention))
        else:
            await self.bot.say("User {0} isn't currently muted".format(user.mention))

    @commands.check(guildonly)
    @commands.check(modcheck)
    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.User):
        """The simple yet majestic mute command"""
        try:
            res = await mute(self.bot, ctx.message.server.id, user.id)
            if res is True:
                await self.bot.say(f"User {user.mention} muted for {minutes} minute(s).")
            else:
                await self.bot.say(f"User {user.mention} already has a mute!")
        except:
            await self.bot.say("I'm missing permissions!")


def setup(bot):
    bot.add_cog(Moderation(bot))

