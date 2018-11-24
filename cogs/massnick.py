import discord
from discord.ext import commands


class MassNick:
    """Mass Nicknaming Module"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(MassNick(bot))
