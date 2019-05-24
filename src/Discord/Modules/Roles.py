import sys

from discord.ext import commands


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="role", pass_context=True)
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @roles.command(name="reaction", pass_context=True)
    async def reaction_promote(self, ctx, emoji_id, role_id):
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


def setup(bot):
    bot.add_cog(Roles(bot))