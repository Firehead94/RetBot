import asyncio

import discord
from discord import Color
from discord.ext import commands
import json

class DiscordBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def testcommand(self,ctx):
        await ctx.send(content="test reply message")


def setup(bot):
    bot.add_cog(DiscordBot(bot))