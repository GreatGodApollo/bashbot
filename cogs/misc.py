import datetime
import time
import discord
from discord.ext import commands
import platform
import pkg_resources

from bot import start_time, version


class Misc:
    """Miscellaneous commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self):
        """Simple Ping with Response Time"""
        em = discord.Embed(description="Ping?", color=discord.Color.blue())
        t1 = time.perf_counter()
        msg = await self.bot.say(embed=em)
        emb = discord.Embed(title="Pong!", color=discord.Color.blue())
        t2 = time.perf_counter()
        data = (str(round((t2 - t1) * 1000)) + "ms")
        emb.add_field(name="Response Time", value=data)
        await self.bot.edit_message(msg, embed=emb)

    @commands.command(aliases=["stats"])
    async def info(self):
        """Get some info about the bot"""
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title="Bash — Bot", description="Information", color=0x4DA825)
        embed.add_field(name="Author", value="apollo#9292", inline=True)
        embed.add_field(name="Bot Version", value=version, inline=True)
        embed.add_field(name="Python Version", value=f"{platform.python_version()}", inline=True)
        embed.add_field(name="Discord.py Version", value=f"{pkg_resources.get_distribution('discord.py').version}", inline=True)
        embed.add_field(name="Hex Color", value="#4DA825", inline=True)
        embed.add_field(name="Uptime", value=text, inline=True)
        embed.add_field(name="Server Count", value=f"{len(self.bot.servers)} servers", inline=True)
        embed.add_field(name="User Count", value=f"{len(set(self.bot.get_all_members()))} users", inline=True)
        await self.bot.say(embed=embed)

    @commands.command()
    async def invite(self):
        await self.bot.say(f"Invite me using https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8")


def setup(bot):
    bot.add_cog(Misc(bot))
