from discord.ext import commands

from src.Discord import Utils
from src.Discord.Utils import generic_embed


async def is_admin(ctx):
    if is_owner(ctx):
        return True
    if ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']:
        return ctx.author.id in ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']
    await ctx.send(content="You do not have access to this command.")
    return False

def is_owner(ctx):
    return ctx.message.author.id == int(ctx.bot.config['owner'])

class Permissions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="permissions", pass_context=True, aliases=['permission'])
    async def permissions(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @permissions.command(name='set', pass_context=True, aliases=['add'])
    async def set(self, ctx, level, *cmd):
        if Utils.checkPerms(ctx, ctx.author):
            level = level.lower()
            command = ""
            for word in cmd:
                command = command + word.lower() + " "
            command = command[:-1]
            if command == "":
                await ctx.send(content="You must supply a command name.")
            elif level in self.bot.config['guilds'][str(ctx.guild.id)]['roles']:
                try:
                    if level in self.bot.config['guilds'][str(ctx.guild.id)]['permissions']:
                        if command not in self.bot.config['guilds'][str(ctx.guild.id)]['permissions'][level]:
                            self.bot.config['guilds'][str(ctx.guild.id)]['permissions'][level].append(command)
                            await ctx.send(content="**{}** added to level **{}**.".format(command, level))
                        else:
                            await ctx.send(content='**{}** already has permission to use **{}**.'.format(level, command))
                    else:
                        self.bot.config['guilds'][str(ctx.guild.id)]['permissions'][level] = [command]
                        await ctx.send(content="**{}** added to level **{}**.".format(command, level))
                    self.bot.save()
                except:
                    self.bot.config['guilds'][str(ctx.guild.id)]['permissions'] = {
                        level:[command]
                    }
                    await ctx.send(content="**{}** added to level **{}**.".format(command, level))
                self.bot.save()
            else:
                await ctx.send(content="**{}** is not a valid permission level.".format(level))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @permissions.command(name='remove', pass_context=True)
    async def remove(self, ctx, level, *cmd):
        if Utils.checkPerms(ctx, ctx.author):
            level = level.lower()
            command = ""
            for word in cmd:
                command = command + word.lower() + " "
            command = command[:-1]
            if command == "":
                await ctx.send(content="You must supply a command name.")
            elif level in self.bot.config['guilds'][str(ctx.guild.id)]['permissions']:
                try:
                    self.bot.config['guilds'][str(ctx.guild.id)]['permissions'][level].remove(command)
                    await ctx.send(content='**{}** removed from role **{}**.'.format(command, level))
                except:
                    await ctx.send(content='**{}** didn\'t have permissions for that command.'.format(level))
            else:
                await ctx.send(content="No permissions found for this level.")
            self.bot.save()
        else:
            await ctx.send(content='You do not have permissions for this command')

    @permissions.command(name='print', pass_context=True)
    async def print(self, ctx, level):
        if Utils.checkPerms(ctx, ctx.author):
            level = level.lower()
            if level in self.bot.config['guilds'][str(ctx.guild.id)]['permissions']:
                content = ''
                for permission in self.bot.config['guilds'][str(ctx.guild.id)]['permissions'][level]:
                    content = content + permission + "\n"
                await ctx.send(content=None, embed=generic_embed(title=level.upper(), description=content, author=self.bot.user))
            else:
                await ctx.send(content='**{}** is not registered in permissions.'.format(level))
        else:
            await ctx.send(content='You do not have permissions for this command')


def setup(bot):
    bot.add_cog(Permissions(bot))