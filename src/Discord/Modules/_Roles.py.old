import sys

import typing
from discord.ext import commands

import Utils
from Utils import generic_embed

async def is_admin(ctx):
    if is_owner(ctx):
        return True
    if ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']:
        return ctx.author.id in ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']
    await ctx.send(content="You do not have access to this command.")
    return False

def is_owner(ctx):
    return ctx.message.author.id == int(ctx.bot.config['owner'])


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="role", pass_context=True)
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @roles.command(name="mute", pass_context=True)
    async def setMute(self, ctx, role_id):
        if Utils.checkPerms(ctx, ctx.author):
            self.bot.config["guilds"][str(ctx.guild.id)]["roles"]["mute"] = {}
            self.bot.config["guilds"][str(ctx.guild.id)]["roles"]["mute"]["role"] = int(role_id)
            self.bot.config["guilds"][str(ctx.guild.id)]["roles"]["mute"]["members"] = []
            self.bot.save()
            await ctx.send(content="<@&{}> set to mute role.".format(role_id))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @roles.command(name="reaction", pass_context=True)
    async def reaction_promote(self, ctx, emoji_id, role_id):
        if Utils.checkPerms(ctx, ctx.author):
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['reactions']
            except:
                self.bot.config['guilds'][str(ctx.guild.id)]['reactions'] = {}
                self.bot.save()
            try:
                if str(emoji_id) in self.bot.config['guilds'][str(ctx.guild.id)]['reactions']:
                    await ctx.send(content="Role already assigned to that reaction.")
                else:
                    self.bot.config['guilds'][str(ctx.guild.id)]['reactions'][str(emoji_id)] = int(role_id)
                    self.bot.save()
                    await ctx.send(content="{} assigned to {}.".format(ctx.guild.get_role(int(role_id)).mention, self.bot.get_emoji(int(emoji_id))))
            except:
                pass
        else:
            await ctx.send(content='You do not have permissions for this command')

    @roles.command(name="add", pass_context=True)
    async def add_role(self, ctx, level, role_id):
        if Utils.checkPerms(ctx, ctx.author):
            level = level.lower()
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['roles']
            except:
                self.bot.config['guilds'][str(ctx.guild.id)]['roles'] = {}
                self.bot.save()
            try:
                if int(role_id) not in self.bot.config['guilds'][str(ctx.guild.id)]['roles'][level]:
                    self.bot.config['guilds'][str(ctx.guild.id)]['roles'][level].append(int(role_id))
                    self.bot.save()
                    await ctx.send(content='Level {} created.\n{} is now listed as level {}.'.format(level, ctx.guild.get_role(int(role_id)), level))
                else:
                    await ctx.send(content='Role already assigned to that level.')
            except:
                self.bot.config['guilds'][str(ctx.guild.id)]['roles'][level] = [int(role_id)]
                self.bot.save()
                await ctx.send(content='{} is now listed as level {}.'.format(ctx.guild.get_role(int(role_id)), level))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @roles.command(name='remove', pass_context=True)
    async def remove_role(self, ctx, level, role_id):
        if Utils.checkPerms(ctx, ctx.author):
            level = level.lower()
            try:
                self.bot.config['guilds'][str(ctx.guild.id)]['roles'][level].remove(int[role_id])
                self.bot.save()
                await ctx.send(content='{} removed from level {}.'.format(ctx.guild.get_role(int(role_id)), level))
            except:
                await ctx.send('Level doesnt exist.')
        else:
            await ctx.send(content='You do not have permissions for this command')

    @roles.command(name='print', pass_context=True)
    async def roles_print(self, ctx, level: typing.Optional[str]=None):
        if Utils.checkPerms(ctx, ctx.author):
            Utils.checkPerms(ctx, ctx.author)
            if level is None:
                try:
                    content = ''
                    for level, roles in self.bot.config['guilds'][str(ctx.guild.id)]['roles'].items():
                        content = content + '**{}**\n'.format(level)
                        for role in roles:
                            content = content + '{}\n'.format(ctx.guild.get_role(int(role)).mention)
                    await ctx.send(content=None, embed=generic_embed(title='Internal Roles', description=content, author=self.bot.user))
                except:
                    await ctx.send(content='No roles found')
            else:
                try:
                    level = level.lower()
                    content = ''
                    for role in self.bot.config['guilds'][str(ctx.guild.id)]['roles'][level]:
                        content = content + '{}\n'.format(ctx.guild.get_role(int(role)).mention)
                    await ctx.send(content=None, embed=generic_embed(title='{}'.format(level), description=content, author=self.bot.user))
                except:
                    await ctx.send(content='{} not found.'.format(level))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.id) in self.bot.config['guilds'][str(message.guild.id)]['watch']:
            for id in self.bot.config['guilds'][str(message.guild.id)]['watch'][str(message.channel.id)]:
                await message.add_reaction(emoji=self.bot.get_emoji(id))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            pass
        else:
            channels_watched = self.bot.config['guilds'][str(payload.guild_id)]['watch']
            if str(payload.channel_id) in channels_watched:
                if payload.emoji.id in self.bot.config['guilds'][str(payload.guild_id)]['watch'][str(payload.channel_id)]:
                    guild = self.bot.get_guild(payload.guild_id)
                    role_id = self.bot.config['guilds'][str(payload.guild_id)]['reactions'][str(payload.emoji.id)]
                    await guild.get_member(payload.user_id).add_roles(guild.get_role(role_id), reason="Clicked on Highlight")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        before_ids = []
        after_ids = []
        try:
            mute_id = self.bot.config["guilds"][str(after.guild.id)]["roles"]["mute"]["role"]
            for roleB in before.roles:
                before_ids.append(roleB.id)
            for roleA in after.roles:
                after_ids.append(roleA.id)
            union = set(before_ids).union(after_ids)
            intersection = set(before_ids).intersection(after_ids)
            difference = set(union).difference(intersection)
            try:
                if mute_id in difference:
                    if mute_id in before_ids:
                        if before.id in self.bot.config["guilds"][str(after.guild.id)]["roles"]["mute"]["members"]:
                            self.bot.config["guilds"][str(after.guild.id)]["roles"]["mute"]["members"].remove(after.id)
                    if mute_id in after_ids:
                        if after.id not in self.bot.config["guilds"][str(after.guild.id)]["roles"]["mute"]["members"]:
                            self.bot.config["guilds"][str(after.guild.id)]["roles"]["mute"]["members"].append(after.id)
                    self.bot.save()
            except:
                pass
        except:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            if member.id in self.bot.config["guilds"][str(member.guild.id)]["roles"]["mute"]["members"]:
                await member.add_roles(member.guild.get_role(self.bot.config["guilds"][str(member.guild.id)]["roles"]["mute"]["role"]), reason="Mute evasion")
        except:
            pass



def setup(bot):
    bot.add_cog(Roles(bot))