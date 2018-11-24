import discord
from discord.ext import commands
from permissions import ownercheck


class Apt:
    """'Package Manager'"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["yum"])
    async def apt(self, ctx):
        """Your average package manager.\nThis apt has Super Cow Powers"""
        if ownercheck(ctx) and ctx.invoked_subcommand is None:
            await self.bot.say("```\nUsage: apt/yum command package\n```")
        elif not ownercheck(ctx) and ctx.invoked_subcommand is None:
            await self.bot.say("You are not root")

    @commands.check(ownercheck)
    @apt.command()
    async def install(self, extension_name: str):
        """Installs a package."""
        msg = await self.bot.say("The package {} is being installed.".format(extension_name))
        try:
            self.bot.load_extension("cogs.{}".format(extension_name))
        except Exception as e:
            await self.bot.edit_message(msg, "We ran into an issue installing {}.".format(extension_name))
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.edit_message(msg, "The package {} was successfully installed.".format(extension_name))

    @commands.check(ownercheck)
    @apt.command()
    async def remove(self, extension_name: str):
        """Removes a package."""
        msg = await self.bot.say("The package {} is being removed.".format(extension_name))
        try:
            self.bot.unload_extension("cogs.{}".format(extension_name))
        except:
            await self.bot.say("We ran into an issue removing {}.".format(extension_name))
        await self.bot.edit_message(msg, "The package {} was successfully removed.".format(extension_name))

    @apt.command()
    async def upgrade(self, extension_name: str):
        """Upgrades a package."""
        msg = await self.bot.say("The package {} is being upgraded.".format(extension_name))
        try:
            self.bot.unload_extension("cogs.{}".format(extension_name))
        except (AttributeError, ImportError) as error:
            await self.bot.say("```py\n{}: {}\n```".format(type(error).__name__, str(error)))
            return
        try:
            self.bot.load_extension("cogs.{}".format(extension_name))
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.edit_message(msg, new_content="The package {} was successfully upgraded.".format(extension_name))


def setup(bot):
    bot.add_cog(Apt(bot))