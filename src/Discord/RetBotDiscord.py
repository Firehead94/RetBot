import asyncio
import datetime
import json
import re
import sys
from os.path import isfile, join
import discord
import os

import typing
from discord import Color, Embed, Message, TextChannel, User, Member, DMChannel, Forbidden
from discord.ext import commands

from src.Discord import Utils


class RetBotDiscord(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.config = {}
        super().__init__(*args, **kwargs)

    def save(self):
        json.dump(self.config, open('discord.json', 'w'), indent=4)
        print('Configuration file saved.')

    def loadModules(self):
        cogFolder = 'Modules'
        for extension in [f.replace('.py', '') for f in os.listdir(cogFolder) if isfile(join(cogFolder, f))]:
            try:
                retBot.load_extension(name=cogFolder+'.'+extension)
                print('Extension {} Loaded Successfully!'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

    async def send_cmd_help(self, ctx):
        await ctx.send(content="No subcommand found. Please visit <https://github.com/Firehead94/RetBot> for usage information.")

def initialize():
    os.chdir(os.path.dirname(sys.argv[0] + 'Discord'))
    if isfile('discord.json'):
        config = json.load(open('discord.json'))
    else:
        print('No configuration file found.\n'
              'Generating new configuration file.\n')
        config = {}
        json.dump(config, open('discord.json', 'w'))
    try:
        config['token']
    except:
        print('No Token found for Discord. This is \nneeded in order to connect to Discord.\n'
              'Please enter your discord Token: ')
        config['token'] = input()
    try:
        config['prefix']
    except:
        config['prefix'] = '!'
    try:
        config['owner']
    except:
        print('\nThere is no owner for this\n'
              'bot. Please enter in a Discord \n'
              'ID number: ')
        config['owner'] = input()
    try:
        config['guilds']
    except:
        config['guilds'] = {}
    retBot = RetBotDiscord(command_prefix=config['prefix'], description='RetBot built by Firehead94', max_messages=10000)
    retBot.author = retBot.user
    retBot.config = config
    retBot.save()

    async def is_admin(ctx):
        if is_owner(ctx.message):
            return True
        if retBot.config['guilds'][str(ctx.guild.id)]['admins']:
            return ctx.author.id in retBot.config['guilds'][str(ctx.guild.id)]['admins']
        await ctx.send(content="You do not have access to this command.")
        return False

    def is_owner(message):
        return message.author.id == int(retBot.config['owner'])

    def blacklist_filter(word, guild_id: typing.Optional[str]=None):
        try:
            guild_id = str(guild_id)
            blacklist = retBot.config['guilds'][guild_id]['blacklist']['words']
            if blacklist and word is not None:
                regex = '^(?!.*(?:\\b'
                for word in blacklist:
                    regex = regex+word+'\\b|'
                regex = (regex[:regex.rindex('|')] if ('|' in regex) else regex)
                regex = regex + '))'
                match = re.match(regex, word, re.I)
                print(match + '|{}|{}'.format(regex, word))
                if match:
                    return True
                return False
            return True
        except:
            return True

    @retBot.command()
    async def reload(ctx):
        if Utils.checkPerms(ctx, ctx.author):
            try:
                retBot.config = json.load(open('discord.json'))
                await ctx.send(content='Reload successful')
            except:
                await ctx.send(content="Failed to reload config")
        else:
            await ctx.send(content='You do not have permissions for this command')

    @retBot.event
    async def on_guild_join(guild):
        try:
            retBot.config['guilds'][str(guild.id)]
        except KeyError:
            retBot.config['guilds'][str(guild.id)] = {
                'blacklist':{
                    'channels':[],
                    'users':[],
                    'words':[]
                },
                'admins':[],
                'logchannel': None,
                'watch':{},
                'reactions':{}
            }
            retBot.save()

    @retBot.event
    async def on_command_error(ctx, error):
        #await ctx.send(content="{}".format(error))
        print('Command Error: '+str(error))

    @retBot.event
    async def on_ready():
        print("\n----------------------------------------")
        print('Welcome to RetBot for Discord')
        print("----------------------------------------")
        print("Logged in as: "+retBot.user.name)
        print("User ID: "+str(retBot.user.id))
        print('Prefix: '+retBot.config['prefix'])
        print('In Guilds: ')
        for guild in retBot.guilds:
            try:
                retBot.config['guilds'][str(guild.id)]
            except KeyError:
                retBot.config['guilds'][str(guild.id)] = {
                                                            'blacklist':{
                                                                'channels':[],
                                                                'users':[],
                                                                'words':[]
                                                            },
                                                            'admins':[],
                                                            'logchannel': None
                                                        }
                retBot.save()
            print('- '+guild.name)
        print('Documentation: https://github.com/Firehead94/RetBot')
        activity = discord.Game(name="GitHub", url="https://github.com/Firehead94/RetBot")
        await retBot.change_presence(status=discord.Status.online, activity=activity)

    return retBot


async def main(bot):
    bot.loadModules()
    await bot.login(bot.config['token'])
    await bot.connect()

if __name__ == '__main__':
    retBot = initialize()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(retBot))
    except discord.LoginFailure:
        print('RetBot Failed to Login: Invalid Credentials.\n'
              'This may be a temporary issue, consult Discords\n'
              'Login Server Status before attemping again.\n'
              'If servers are working properly, you may need\n'
              'a new token. Please replace the token in the\n'
              'discord.json file with a new token.\n')
    except KeyboardInterrupt:
        loop.run_until_complete(retBot.logout())
    except Exception as e:
        print("Fatal exception, attempting graceful logout.\n{}".format(e))
        loop.run_until_complete(retBot.logout())
    finally:
        loop.close()
        exit(1)