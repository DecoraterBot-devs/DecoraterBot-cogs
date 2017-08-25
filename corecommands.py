# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
import traceback
import time

import discord
from discord.ext import commands
from DecoraterBotUtils.BotErrors import CogUnloadError
from DecoraterBotUtils.utils import *


class CoreCommands:
    """
    Core Commands class for DecoraterBot.
    """
    def __init__(self):
        self.corecommands_text = PluginTextReader(
            file='corecommands.json')

    @commands.command(name='uptime', pass_context=True, no_pm=False)
    async def uptime_command(self, ctx):
        """
        Command.
        """
        if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in ctx.bot.banlist['Users']:
            return
        else:
            stop = time.time()
            seconds = stop - ctx.bot.uptime_count_begin
            days = int(((seconds / 60) / 60) / 24)
            hours = str(int((seconds / 60) / 60 - (days * 24)))
            minutes = str(int((seconds / 60) % 60))
            seconds = str(int(seconds % 60))
            days = str(days)
            time_001 = str(self.corecommands_text['Uptime_command_data'][0]
                           ).format(days, hours, minutes, seconds)
            time_parse = time_001
            try:
                await ctx.bot.send_message(ctx.message.channel,
                                            content=time_parse)
            except discord.Forbidden:
                return

    @commands.command(name='load', pass_context=True, no_pm=True)
    async def load_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == ctx.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'load '):].strip()
            ctx.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                ctx.bot._somebool = True
                try:
                    ret = ctx.bot.load_plugin(desmod_new)
                except ImportError:
                    ret = str(traceback.format_exc())
            if ctx.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.corecommands_text['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Loading Plugin')
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
                else:
                    try:
                        msgdata = str(
                            self.corecommands_text['reload_command_data'][0])
                        message_data = msgdata + ' Loaded ' + desmod_new + '.'
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
            else:
                try:
                    await ctx.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.corecommands_text[
                                                        'reload_command_data'][
                                                        2]))
                except discord.Forbidden:
                    await ctx.bot.BotPMError.resolve_send_message_error(
                        ctx)
        else:
            try:
                await ctx.bot.send_message(
                    ctx.message.channel,
                    content=str(
                        self.corecommands_text[
                            'reload_command_data'
                        ][3]).replace('reload', 'load'))
            except discord.Forbidden:
                await ctx.bot.BotPMError.resolve_send_message_error(
                    ctx)

    @commands.command(name='unload', pass_context=True, no_pm=True)
    async def unload_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == ctx.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'unload '):].strip()
            ctx.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                ctx.bot._somebool = True
                try:
                    ret = ctx.bot.unload_plugin(desmod_new)
                except CogUnloadError:
                    ret = str(traceback.format_exc())
            if ctx.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.corecommands_text['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Unloading Plugin')
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
                else:
                    try:
                        msgdata = str(
                            self.corecommands_text['reload_command_data'][0])
                        message_data = msgdata + ' Unloaded ' + desmod_new +\
                            '.'
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
            else:
                try:
                    await ctx.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.corecommands_text[
                                                        'reload_command_data'][
                                                        2]))
                except discord.Forbidden:
                    await ctx.bot.BotPMError.resolve_send_message_error(
                        ctx)
        else:
            try:
                await ctx.bot.send_message(
                    ctx.message.channel,
                    content=str(
                        self.corecommands_text[
                            'reload_command_data'
                        ][3]).replace('reload', 'unload'))
            except discord.Forbidden:
                await ctx.bot.BotPMError.resolve_send_message_error(
                    ctx)

    @commands.command(name='reload', pass_context=True, no_pm=True)
    async def reload_plugin_command(self, ctx):
        """
        Command.
        """
        if ctx.message.author.id == ctx.bot.BotConfig.discord_user_id:
            desmod_new = ctx.message.content.lower()[len(
                ctx.prefix + 'reload '):].strip()
            ctx.bot._somebool = False
            ret = ""
            if desmod_new is not None:
                ctx.bot._somebool = True
                try:
                    ret = ctx.bot.reload_plugin(desmod_new)
                except ImportError:
                    ret = str(traceback.format_exc())
            if ctx.bot._somebool is True:
                if ret is not None:
                    try:
                        reload_data = str(
                            self.corecommands_text['reload_command_data'][1]
                        ).format(ret).replace('Reloading', 'Reloading Plugin')
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=reload_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
                else:
                    try:
                        msgdata = str(
                            self.corecommands_text['reload_command_data'][0])
                        message_data = msgdata + ' Reloaded ' + desmod_new +\
                            '.'
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx)
            else:
                try:
                    await ctx.bot.send_message(
                        ctx.message.channel, content=str(
                            self.corecommands_text[
                                'reload_command_data'
                            ][2]))
                except discord.Forbidden:
                    await ctx.bot.BotPMError.resolve_send_message_error(
                        ctx)
        else:
            try:
                await ctx.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.corecommands_text[
                                                    'reload_command_data'][3]))
            except discord.Forbidden:
                await ctx.bot.BotPMError.resolve_send_message_error(
                    ctx)

    @commands.command(name='install', pass_context=True, no_pm=True)
    async def install_command(self, ctx):
       # TODO: finish command.
       pass

    @commands.command(name='uninstall', pass_context=True, no_pm=True)
    async def uninstall_command(self, ctx):
       # TODO: finish command.
       pass


def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    bot.add_cog(CoreCommands())
