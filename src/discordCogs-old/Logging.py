import json

import typing
from discord import Embed, Color, User, DMChannel
from discord.ext import commands
import src.RetBot as RetBot
from src.discordCogs.Utils import COLORS


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def log(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @log.command(pass_context=True, name="toggle")
    async def setEnabled(self, ctx):
        currentFlag = RetBot.config['settings']['discord'][ctx.guild.id]['flags']['logging']
        if not currentFlag:
            currentFlag = False
        RetBot.config['settings']['discord'][ctx.guild.id]['flags']['logging'] = (not currentFlag)
        RetBot.save()

    @log.command(pass_context=True, name='setchannel')
    async def setChannel(self, ctx):
        RetBot.config['settings']['discord'][ctx.guild.id]['channels']['logchannel'] = ctx.channel.id
        RetBot.save()

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if self.isEnabled(payload.guild_id) and not self.blacklist_check(payload.channel_id, payload.guild_id):
            logChannel = self.bot.get_channel(RetBot.config['settings']['discord'][payload.guild_id]['channels']['logchannel'])
            if type(self.bot.get_channel(payload.channel_id)) is not DMChannel and payload.channel_id not in logChannel:
                message = payload.cached_message
                if message is not None:
                    embed = self.generic(description='**Messag Deleted in {}**'.format(message.channel.mention + '\n{}'.format(message.content),
                                         color=COLORS['RED']),
                                         author=message.author,
                                         footer='ID: {} | Msg ID: {} • {}'.format(message.author.id, message.id, message.edited_at))
                else:
                    embed = self.generic(description='**Message Deleted in <#{}>**\n{}'.format(payload.channel_id,payload.message_id),
                                         color=COLORS['RED'],
                                         author=self.bot.user)
                self.log_embed(content=None, embed=embed, guild_id=payload.guild_id)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        if self.isEnabled(payload.guild_id) and not self.blacklist_check(payload.channel_id, payload.guild_id):
            logChannel = self.bot.get_channel(RetBot.config['settings']['discord'][payload.guild_id]['channels']['logchannel'])
            if type(self.bot.get_channel(payload.channel_id)) is not DMChannel and payload.channel_id not in logChannel:
                messages = payload.cached_messages
                if messages is not None:
                    for message in messages:
                        content = content + '**{}#{}**\n{}\n'.format(message.author.name, message.author.discriminator, message.content)
                    embed = self.generic(description='**{} Messages Deleted in <#{}>\n'.format(str(len(messages)), payload.channel_id)+content,
                                         color=COLORS['RED'],
                                         author=self.bot.user)
                else:
                    for id in payload.message_ids:
                        idList = idList + str(id) + '\n'
                    embed = self.generic(description='**Message Deleted in <#{}>**\n{}'.format(payload.channel_id,idList),
                                         color=COLORS['RED'],
                                         author=self.bot.user)
                self.log_embed(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.isEnabled(before.guild.id) and not self.blacklist_check(before.channel.id, before.guild.id):
            logChannel = self.bot.get_channel(RetBot.config['settings']['discord'][before.guild.id]['channels']['logchannel'])
            if type(before.channel) is not DMChannel and before.channel.id not in logChannel:
                if before.content == after.content:
                    pass
                else:
                    embed = Embed(description='**Message Edited in {}**'.format(before.channel.mention),
                                  color=COLORS['AQUA'],
                                  author=before.author,
                                  footer='User ID: {} | {}'.format(before.author.id,after.edited_at),
                                  fields={
                                      'Before': before.content,
                                      'After': after.content
                                  })
                    await logChannel.send(content=None, embed=embed)


    def generic(self, *, title: typing.Optional[str], description: typing.Optional[str],
                color: typing.Optional[Color], author: typing.Optional[User], footer: typing.Optional[str], fields: typing.Optional[dict]):
        embed = Embed(title=title, description=description, color=color)
        embed.set_author(name='{}#{}'.format(author.name, author.discriminator), icon_url=author.avatar_url)
        embed.set_footer(text=footer)
        if fields:
            for field in fields:
                embed.add_field(name=field[0], value=field[1], inline=False)
        return embed

    def blacklist_check(self, channel_id, guild_id):
        blacklist = RetBot.config['settings']['discord'][guild_id]['channels']['blacklist']
        if channel_id in blacklist:
            return True
        return False

    @staticmethod
    def isEnabled(guild_id):
        return RetBot.config['settings']['discord'][guild_id]['flags']['logging']

    def log_embed(self, *, content, embed, guild_id):
        logChannel = self.bot.get_channel(RetBot.config['settings']['discord'][guild_id]['channels']['logchannel'])
        await logChannel.send(content=content, embed=embed)



def setup(bot):
    bot.add_cog(Logging(bot))