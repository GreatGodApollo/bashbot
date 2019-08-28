import discord
from discord.ext import commands
import random


class Random:
    """Random Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, sides: int = 6):
        """Roll a die"""
        await self.bot.say(f"You rolled a {sides} sided die.\n> {random.randint(1, sides)}")

    @commands.command(pass_context=True)
    async def choose(self, ctx, *choices):
        """Get a random choice"""
        choice = choices[random.randint(0, len(choices) - 1)]
        await self.bot.say(f"I choose\n> {choice}")


def setup(bot):
    bot.add_cog(Random(bot))
