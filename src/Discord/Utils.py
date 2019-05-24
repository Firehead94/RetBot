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
