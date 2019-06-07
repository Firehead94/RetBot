import datetime

from discord import DMChannel
from discord.ext import commands
from discord.ext.commands import Command, Group

from src.Discord import RetBotDiscord, Utils
from src.Discord.Utils import generic_embed, COLORS


def enabled(ctx):
    print(ctx.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] is not None)
    return ctx.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] is not None

async def is_admin(ctx):
    if is_owner(ctx):
        return True
    if ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']:
        return ctx.author.id in ctx.bot.config['guilds'][str(ctx.guild.id)]['admins']
    await ctx.send(content="You do not have access to this command.")
    return False

def is_owner(ctx):
    return ctx.message.author.id == int(ctx.bot.config['owner'])

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self,ctx):
        try:
            if ctx.invoked_subcommand.name in ['clear', 'stop', 'disable', 'none', 'remove', 'delete']:
                return True
        except:
            pass
        if type(ctx.channel) is DMChannel:
            return False
        if not self.valid_channel(ctx.channel.id, guild_id=ctx.guild.id):
            if type(ctx.command) is Command or type(ctx.command) is Group:
                await ctx.send(content="Command '{}' not allowed in this channel".format(ctx.command.name))
                await ctx.message.delete(delay=1)
            return False
        return True

    def valid_channel(self, channel_id, *, guild_id):
        blacklist = self.bot.config['guilds'][str(guild_id)]['blacklist']['channels']
        if blacklist:
            if channel_id in blacklist:
                return False
        return True

    '''
    BEGING COMMANDS
    '''
    @commands.group(pass_context=True, invoke_without_command=True)
    async def log(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @log.group(pass_context=True, name='blacklist', aliases=['hide','ignore'], invoke_without_command=True)
    async def blacklist(self, ctx):
        if Utils.checkPerms(ctx, ctx.author):
            if ctx.invoked_subcommand is None:
                self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].append(ctx.channel.id)
                self.bot.save()
                await ctx.send(content='{} added to the blacklist'.format(ctx.channel.mention))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @log.group(pass_context=True, name='setchannel', aliases=['set','channelset'], invoke_without_command=True)
    async def setchannel(self, ctx):
        if Utils.checkPerms(ctx, ctx.author):
            if ctx.invoked_subcommand is None:
                if self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels']:
                    self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].remove(self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'])
                self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] = ctx.channel.id
                if ctx.channel.id not in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels']:
                    self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].append(ctx.channel.id)
                self.bot.save()
                await ctx.send(content='Log channel set to {}'.format(ctx.channel.mention))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @blacklist.command(pass_context=True, name='add')
    async def blacklist_add(self, ctx):
        if Utils.checkPerms(ctx, ctx.author):
            self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].append(ctx.channel.id)
            self.bot.save()
            await ctx.send(content='{} added to the blacklist'.format(ctx.channel.mention))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @blacklist.command(pass_context=True, name='remove', aliases=['delete'])
    async def blacklist_remove(self, ctx):
        if Utils.checkPerms(ctx, ctx.author):
            self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].remove(ctx.channel.id)
            self.bot.save()
            await ctx.send(content='{} removed from the blacklist'.format(ctx.channel.mention))
        else:
            await ctx.send(content='You do not have permissions for this command')

    @setchannel.command(pass_context=True, name='clear', aliases=['stop', 'disable', 'none'])
    async def clearlogchannel(self, ctx):
        if Utils.checkPerms(ctx, ctx.author):
            if self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] in self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels']:
                self.bot.config['guilds'][str(ctx.guild.id)]['blacklist']['channels'].remove(self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'])
            self.bot.config['guilds'][str(ctx.guild.id)]['logchannel'] = None
            self.bot.save()
            await ctx.send(content='Log channel cleared')
        else:
            await ctx.send(content='You do not have permissions for this command')

    '''
    BEGIN LISTENERS
    '''
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(member.guild.id)]['logchannel'])
        if channel is not None:
            embed = generic_embed(description='{} **{}#{}**'.format(member.mention, member.display_name, member.discriminator),
                                  color=COLORS['GREEN'], footer='Joined At: {} | ID: {}'.format(member.joined_at, member.id))
            embed.set_author(name='Member Joined', icon_url=member.avatar_url)
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(member.guild.id)]['logchannel'])
        if channel is not None:
            embed = generic_embed(description='{} **{}#{}**'.format(member.mention, member.display_name, member.discriminator),
                                  color=COLORS['ORANGE'], footer='Left At: {} | ID: {}'.format(member.joined_at, member.id))
            embed.set_author(name='Member Left', icon_url=member.avatar_url)
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(before.guild.id)]['logchannel'])
        if channel is not None and before.nick != after.nick:
            embed = generic_embed(description='{} **{}#{}**'.format(after.mention, after.name, after.discriminator),
                                  color=COLORS['YELLOW'], footer='User ID: {}'.format(before.id),
                                  fields={
                                      'Before': before.nick,
                                      'After': after.nick
                                  })
            embed.set_author(name='Member Name Changed'.format(before.name,before.discriminator), icon_url=after.avatar_url)
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            for guild in self.bot.guilds:
                if guild.get_member(after.id) is not None:
                    channel = self.bot.get_channel(self.bot.config['guilds'][str(guild.id)]['logchannel'])
                    embed = generic_embed(description='{} **{}#{}**'.format(after.mention, after.name, after.discriminator),
                                          color=COLORS['YELLOW'], footer='User ID: {}'.format(before.id),
                                          fields={
                                              'Before': before.name,
                                              'After': after.name
                                          })
                    embed.set_author(name='Member Name Changed'.format(before.name,before.discriminator), icon_url=after.avatar_url)
                    await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(guild.id)]['logchannel'])
        if channel is not None:
            reason = str((await guild.fetch_ban(member)).reason).split(':')
            try:
                embed = generic_embed(title='User `{}` banned.'.format(member.mention),
                                      description='**Name:** {}\n**Reason:** `{}`'.format(reason[0],reason[1]),
                                      color=COLORS['ORANGE'],
                                      footer='User ID: {} | {}'.format(member.id, str(datetime.datetime.now())))
            except:
                embed = generic_embed(title='User `{}` banned.'.format(member.mention),
                                      description='**Name:** {}'.format(member.name),
                                      color=COLORS['ORANGE'],
                                      footer='User ID: {} | {}'.format(member.id, str(datetime.datetime.now())))
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(guild.id)]['logchannel'])
        if channel is not None:
            embed = generic_embed(title='User `{}` unbanned.'.format(member.mention),
                                  color=COLORS['GREEN'],
                                  footer='User ID: {} | {}'.format(member.id, str(datetime.datetime.now())))
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            channel = self.bot.get_channel(self.bot.config['guilds'][str(after.guild.id)]['logchannel'])
            if channel is not None and before.content != after.content and self.valid_channel(before.channel.id, guild_id=before.guild.id):
                embed = generic_embed(description='**Message Edited in {}**'.format(before.channel.mention),
                                      color=COLORS['AQUA'], footer='User ID: {}'.format(before.id),
                                      fields={
                                          'Before': before.content,
                                          'After': after.content
                                      }, author=before.author)
                await channel.send(content=None, embed=embed)
        except:
            print("Message Edit Error: {} is no longer in this discord.".format(before.name))

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(payload.guild_id)]['logchannel'])
        if channel is not None and self.valid_channel(payload.channel_id, guild_id=payload.guild_id):
            messages = payload.cached_messages
            if messages is not None:
                content = ''
                for message in messages:
                    content = content + '**{}#{}**\n{}\n'.format(message.author.name, message.author.discriminator, message.content)
                content = (content[-1500:] + "\n...") if len(content) > 1500 else content
                embed = generic_embed(description='**{} Messages Deleted in <#{}>**\n'.format(str(len(messages)), payload.channel_id)+content,
                                      color=COLORS['RED'], author=self.bot.author)
            else:
                idList = ''
                for id in payload.message_ids:
                    idList = idList + str(id) + '\n'
                embed = generic_embed(description='**Message Deleted in <#{}>**\n{}'.format(payload.channel_id,idList),
                                      color=COLORS['RED'], author=self.bot.author)
            await channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel = self.bot.get_channel(self.bot.config['guilds'][str(payload.guild_id)]['logchannel'])
        if channel is not None and self.valid_channel(payload.channel_id, guild_id=payload.guild_id):
            message = payload.cached_message
            if message is not None:
                embed = generic_embed(description='**Message Deleted in {}**'.format(message.channel.mention) + '\n{}'.format(message.content),
                                      color=COLORS['RED'], author=message.author,
                                      footer='ID: {} | Msg ID: {} • {}'.format(message.author.id, message.id, message.edited_at))
            else:
                embed = generic_embed(description='**Message Deleted in <#{}>**\n{}'.format(payload.channel_id,payload.message_id),
                                      color=COLORS['RED'], author=self.bot.author)
            await channel.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Logging(bot))
