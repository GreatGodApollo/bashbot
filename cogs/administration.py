import discord
from discord.ext import commands

from permissions import admincheck


class Administration:
    """Admnistration module"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def admin(self, ctx):
        """This is a command to check if you have admin privileges"""

        bot = self.bot
        if admincheck(ctx) and ctx.invoked_subcommand is None:
            pages = bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await bot.send_message(ctx.message.channel, page)
        elif not admincheck(ctx):
            await bot.say("You are not an admin")

    @commands.check(admincheck)
    @admin.command(pass_context=True)
    async def setupmute(self, ctx):
        if discord.utils.get(ctx.message.server.roles, name="Muted") is None:
            try:
                msg = await self.bot.say("Please allow some time for this command to work")
                perms = discord.Permissions(send_messages=False, read_messages=True)
                role = await self.bot.create_role(ctx.message.server, name="Muted", permissions=perms)
                override = discord.PermissionOverwrite()
                override.send_messages = False
                for r in ctx.message.server.channels:
                    await self.bot.edit_channel_permissions(r, role, override)
                await self.bot.edit_message(msg, "I finished setting up the Muted role and channel overrides!")
            except:
                await self.bot.say("I'm missing permissions!")
        else:
            await self.bot.say("A Muted role already exists, please run `admin setupmutechannels` in order to just setup the channel overrides")

    @commands.check(admincheck)
    @admin.command(pass_context=True)
    async def setupmutechannels(self, ctx):
        if discord.utils.get(ctx.message.server.roles, name="Muted") is None:
            await self.bot.say("It looks like you don't even have a Muted role, run `admin setupmute` in order to get the full setup going")
        else:
            message = await self.bot.say("Setting up channel overrides.")
            role = discord.utils.get(ctx.message.server.roles, name="Muted")
            override = discord.PermissionOverwrite()
            override.send_messages = False
            for r in ctx.message.server.channels:
                await self.bot.edit_channel_permissions(r, role, override)
            await self.bot.edit_message(message, "I finished setting up the channel overrides!")


def setup(bot):
    bot.add_cog(Administration(bot))
