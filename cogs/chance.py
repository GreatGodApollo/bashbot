import discord
from discord.ext import commands

from permissions import admincheck


class Chance:
    """Chance Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.check(admincheck)
    @commands.command()
    async def chance(self):
        """Have a chance to get a punishment"""

        await self.bot.say("Not yet implemented")


def setup(bot):
    bot.add_cog(Chance(bot))

