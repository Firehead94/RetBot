import re
import typing
from discord import Embed, Forbidden, Member, DMChannel
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

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def blacklist_filter(self, word, guild_id: typing.Optional[str]=None):
        return True
        #try:
        #    guild_id = str(guild_id)
        #    blacklist = self.bot.config['guilds'][guild_id]['blacklist']['words']
        #    if blacklist and word is not None:
        #        regex = '^(?!.*(?:\\b'
        #        for word in blacklist:
        #            regex = regex+word+'\\b|'
        #        regex = (regex[:regex.rindex('|')] if ('|' in regex) else regex)
        #        regex = regex + '))'
        #        match = re.match(regex, word, re.I)
        #        print(match + '|{}|{}'.format(regex, word))
        #        if match:
        #            return True
        #        return False
        #    return True
        #except:
        #    return True

    async def sendbanmessage(self, guild, user, reason, staffmember):
        embed=Embed(title='Reason: `{}`'.format(reason), description='You can appeal this ban by filling out the [ban appeal form](https://goo.gl/forms/tzFK05hyQVN3GEbt2)', color=0xff0000)
        embed.set_author(name='You have been banned from {}'.format(guild.name), icon_url='{}'.format(guild.icon_url))
        embed.set_footer(text='Banned by: {}'.format(staffmember.top_role.name))
        try:
            finalmessage = await user.send(content=None, embed=embed)
            return finalmessage
        except Forbidden:
            await staffmember.send('User `{}` was banned, however the ban message could not be sent.'.format(user))
            return None

    @commands.command()
    async def ban(self, ctx, target: Member, delete_days: typing.Optional[int] = 0, *, reason: typing.Optional[str] = None):
        canban = True
        for role in ctx.author.roles:
            for roleTar in target.roles:
                if role.id == roleTar.id:
                    canban = False

        if ctx.author.guild_permissions.ban_members and canban:
            """Bans a member and sends them a dm with the reason."""
            if delete_days > 7:
                await ctx.send('Messages can only be purged up to 7 days.')
                return
            finalmessage = await self.sendbanmessage(ctx.guild, target, reason, ctx.author)
            try:
                await ctx.guild.ban(target, reason='{}: {}'.format(ctx.author, reason), delete_message_days=delete_days)
            except Forbidden:
                embed = Embed(title='Unable to ban `{}`.'.format(target), description='The bot is missing permissions.', color=0xF89817)
                if finalmessage is not None:
                    await finalmessage.delete()
                await ctx.send(content=None, embed=embed)
        else:
            await ctx.send(content='You do not have permissions for this command or target has higher permissions that you.')

    @ban.error
    async def ban_error(self, ctx, error): # Command error handling
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have permission to access this command.')

    @commands.command()
    async def blacklist(self, ctx, action, word: typing.Optional[str]=None):
        if ctx.author.guild_permissions.ban_members:
            if action == 'add':
                if word not in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['words']:
                    self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['words'].append(word)
                else:
                    ctx.send(content="{} is already on the blacklist.".format(word))
            if action in ['remove', 'delete']:
                if word in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['words']:
                    self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['words'].remove(word)
                else:
                    ctx.send(content="{} is not on the blacklist.".format(word))
            if action == 'print':
                content = ''
                for word in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['words']:
                    content = content + word + '\n'
                await ctx.send(content=None, embed=generic_embed(title="Blacklist", description=content, author=self.bot.user))
            self.bot.save()
        else:
            await ctx.send(content='You do not have permissions for this command')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.blacklist_filter(member.name, member.guild.id):
            pass
        else:
            await member.send(content="'{}' violates **{}'s** blacklist. Your new nickname was reset to your previous name.".format(member.name, member.guild.name))
            await member.kick(reason="Name violated the blacklist")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.bot.skip_nxtUpdate = False
        if after.nick != before.nick:
            if not self.blacklist_filter(after.nick, after.guild.id) and not self.bot.skip_nxtUpdate:
                await after.send(content="'{}' violates **{}'s** blacklist. Your new nickname was reset to your previous name.".format(after.nick, after.guild.name))
                try:
                    await after.edit(reason='Name violates the blacklist', nick=before.nick)
                    self.bot.skip_nxtUpdate = True
                except Forbidden:
                    print("Unable to reset username due to permission conflicts.")
            elif self.bot.skip_nxtUpdate:
                self.bot.skip_nxtUpdate = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is DMChannel:
            pass
        elif message.author.id == self.bot.user.id:
            pass
        elif self.blacklist_filter(message.content, message.guild.id) or is_owner(message):
            pass
        else:
            await message.delete(delay=1)

def setup(bot):
    bot.add_cog(General(bot))