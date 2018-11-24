import discord
from discord.ext import commands

from permissions import modcheck


class Moderation:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.check(modcheck)
    @commands.command(pass_context=True)
    async def unmute(self, ctx, user: discord.User):
        """The simple yet majestic unmute command"""
        role = discord.utils.get(ctx.message.server.roles, name='Muted')
        await self.bot.remove_roles(user, role)
        await self.bot.say("User {0} unmuted.".format(user.mention))

    @commands.check(modcheck)
    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.User):
        """The simple yet majestic mute command"""
        role = discord.utils.get(ctx.message.server.roles, name='Muted')
        await self.bot.add_roles(user, role)
        await self.bot.say("User {0} muted.".format(user.mention))


def setup(bot):
    bot.add_cog(Moderation(bot))