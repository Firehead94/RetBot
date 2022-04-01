import sys
import typing
from discord.ext import commands
import discord

class ReactionRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="react", pass_context=True)
    async def reactroles(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @reactroles.command(name="setup", pass_context=True)
    async def setup(self, ctx):
        if ctx.author.guild_permissions.administrator:
            channel_id = str(ctx.channel.id)
            emoji_id = 0
            trash_msg = [ctx.message]
            if channel_id in self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"]:
                trash_msg.append(await ctx.send("This channel already has an associated tracking, would you like to remove it?"))
                reply = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                trash_msg.append(reply)
                if reply.content.lower() in ["y", "yes", "Y", "Yes", "YES"]:
                    trash_msg.append(await ctx.send("Deleting tracking"))
                    del self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"][channel_id]
                    self.bot.save()
                else:
                    trash_msg.append(await ctx.send("Exiting Setup"))
            if channel_id not in self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"]:
                sent = await ctx.send("React to this message with the emote you'd like to use for this channel.")
                trash_msg.append(sent)
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=lambda reaction, user: user == ctx.author)
                trash_msg.append(await ctx.send("*Please mention the role you'd like to give for  {.emoji}. Note, you may need to temporarily make the roles mentionable in their settings.*".format(reaction)))
                role = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
                trash_msg.append(role)
                if role is not None:
                    self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"][channel_id] = {"role_id":str(role.role_mentions[0].id),"emoji_id":str(reaction.emoji.id)}
                    self.bot.save()
                    trash_msg.append(await ctx.send("Now tracking messages in this channel"))

            trash_msg.append(await ctx.send("Would you like me to clean up the mess? (y/n)"))
            reply = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            trash_msg.append(reply)
            if reply.content.lower() in ["y", "yes", "Y", "Yes", "YES"]:
                await ctx.channel.delete_messages(trash_msg)
            else:
                pass

    @reactroles.command(name="remove", pass_context=True)
    async def remove(self, ctx):
        if ctx.author.guild_permissions.administrator:
            channel_id = str(ctx.channel.id)
            trash_msg = [ctx.message]
            if channel_id in self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"]:
                await ctx.send("Are you sure you want to untrack this channel? (y/n)")
                reply = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                trash_msg.append(reply)
                if reply.content.lower() in ["y", "yes", "Y", "Yes", "YES"]:
                    trash_msg.append(await ctx.send("Deleting tracking"))
                    del self.bot.config["guilds"][str(ctx.guild.id)]["reactroles"][channel_id]
                    self.bot.save()
            await ctx.channel.delete_messages(trash_msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel_id = str(message.channel.id)
        if channel_id in self.bot.config["guilds"][str(message.guild.id)]["reactroles"]:
            await message.add_reaction(emoji = self.bot.get_emoji(int(self.bot.config["guilds"][str(message.guild.id)]["reactroles"][channel_id]["emoji_id"])))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            pass
        else:
            channel_id = str(payload.channel_id)
            if channel_id in self.bot.config["guilds"][str(payload.guild_id)]["reactroles"]:
                if self.bot.config["guilds"][str(payload.guild_id)]['reactroles'][channel_id]["emoji_id"] == str(payload.emoji.id):
                    guild = self.bot.get_guild(payload.guild_id)
                    role_id = self.bot.config["guilds"][str(payload.guild_id)]['reactroles'][channel_id]["role_id"]
                    member = await guild.fetch_member(payload.user_id)
                    if isinstance(member, discord.Member):
                        await member.add_roles(guild.get_role(int(role_id)), reason="Reaction for role auto assign")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            pass
        else:
            channel_id = str(payload.channel_id)
            if channel_id in self.bot.config["guilds"][str(payload.guild_id)]["reactroles"]:
                if self.bot.config["guilds"][str(payload.guild_id)]['reactroles'][channel_id]["emoji_id"] == str(payload.emoji.id):
                    guild = self.bot.get_guild(payload.guild_id)
                    role_id = self.bot.config["guilds"][str(payload.guild_id)]['reactroles'][channel_id]["role_id"]
                    member = await guild.fetch_member(payload.user_id)
                    if isinstance(member, discord.Member):
                        await member.remove_roles(guild.get_role(int(role_id)), reason="Reaction for role auto assign")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))