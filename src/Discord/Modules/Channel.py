import asyncio

import typing
from discord.ext import commands


async def is_admin(ctx):
    if is_owner(ctx):
        return True
    if ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']:
        return ctx.author.id in ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']
    await ctx.send(content="You do not have access to this command.")
    return False

def is_owner(ctx):
    return ctx.message.author.id == int(ctx.bot.config['owner'])


class Channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='purge', aliases=['delete','remove'])
    async def purgeChannel(self, ctx, number):
        if ctx.author.guild_permissions.manage_channels:
            list = []
            count = 0
            async for msg in ctx.channel.history(limit=int(number)):
                if count < 100:
                    list.append(msg)
                    count +=1
                else:
                    await ctx.channel.delete_messages(list)
                    await asyncio.sleep(1)
                    count = 0
                    list = []
            await ctx.channel.delete_messages(list)
        else:
            await ctx.send(content='You do not have permissions for this command')

    @commands.group(name='channel', pass_context=True)
    async def channel(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @channel.command(name="mark", pass_context=True)
    async def mark(self, ctx, reaction_id):
        if ctx.author.guild_permissions.manage_channels:
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['watch']
            except:
                self.bot.config['guilds'][str(ctx.guild.id)]['watch'] = {}
                self.bot.save()
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['watch'][str(ctx.channel.id)]
            except:
                self.bot.config['guilds'][str(ctx.guild.id)]['watch'][str(ctx.channel.id)] = []
            self.bot.config['guilds'][str(ctx.guild.id)]['watch'][str(ctx.channel.id)].append(int(reaction_id))
            self.bot.save()
            await ctx.send(content='{} is now watching {} for reaction {}.'.format(self.bot.user.mention, ctx.channel.mention, self.bot.get_emoji(int(reaction_id))))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @channel.command(name="unmark", pass_context=True)
    async def unmark(self, ctx, reaction_id):
        if ctx.author.guild_permissions.manage_channels:
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['watch'][str(ctx.channel.id)].remove(int(reaction_id))
                self.bot.save()
            except:
                await ctx.send(content='{} was not watched.'.format(self.bot.get_emoji(int(reaction_id))))
        else:
            await ctx.send(content='You do not have permissions for this command')


def setup(bot):
    bot.add_cog(Channel(bot))