import typing
from discord import Color, Embed, User
from discord.ext import commands

COLORS = {
    'RED': Color(0xff0000),
    'ORANGE': Color(0xFF9B00),
    'BLUE': Color(0x0000ff),
    'GREEN': Color(0x00ff00),
    'YELLOW': Color(0xFFFF00),
    'PURPLE': Color(0xaFF00FF),
    'AQUA': Color(0x00FFFF)
}

def is_owner(ctx):
    return ctx.message.author.id == int(ctx.bot.config['owner'])

def generic_embed(*, title: typing.Optional[str]=None, description: typing.Optional[str]=None,
                  color: typing.Optional[Color]=Color(0xffffff), author: typing.Optional[User]=None, footer: typing.Optional[str]=None, fields: typing.Optional[dict]=None):
    embed = Embed(title=title, description=description, color=color)
    if author is not None:
        embed.set_author(name='{}#{}'.format(author.name, author.discriminator), icon_url=author.avatar_url)
    if footer is not None:
        embed.set_footer(text=footer)
    if fields is not None:
        for name,value in fields.items():
            embed.add_field(name=name, value=value, inline=False)
    return embed

'''
def get_perm_command(ctx, command):
    permissions = ctx.bot.config['guilds'][str(ctx.guild.id)]['permissions']
    for role, allowed in permissions.items():
        if str(command) in allowed:
            return role.lower()
    return None

def get_perm_member(ctx, member):
    roles = ctx.bot.config['guilds'][str(ctx.guild.id)]['roles']
    for role, ids in roles.items():
        for id in ids:
            for mem_role in member.roles:
                if id == mem_role.id:
                    return role.lower()
    return None

def checkPerms(ctx, member):
    if is_owner(ctx):
        return True
    commandperm = get_perm_command(ctx, ctx.command)
    memperm = get_perm_member(ctx, member)
    if commandperm is not None and memperm is not None:
        if commandperm == memperm:
            return True
        else:
            return False
    else:
        return False
'''