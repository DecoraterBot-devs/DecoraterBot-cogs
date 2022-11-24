# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
import json
import os
import sys
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils.BotErrors import CogUnloadError
from DecoraterBotUtils import utils, readers


class CoreCommands(commands.Cog):
    """
    Core Commands class for DecoraterBot.
    """
    def __init__(self, bot):
        self.bot = bot
        self.corecommands_text = readers.PluginTextReader(
            file='corecommands.json').get_config

    @app_commands.command(name='load', description='Loads a specific cog into the bot (Bot owner only).')
    @app_commands.describe(module='The cog to load.')
    @utils.Checks.is_bot_owner()
    async def load_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            try:
                ret = await self.bot.load_plugin(module)
            except ImportError:
                ret = str(traceback.format_exc())
        if self.bot._somebool is True:
            if ret is not None:
                try:
                    reload_data = str(
                        self.corecommands_text['reload_command_data'][1]
                    ).format(ret).replace('Reloading', 'Loading Plugin')
                    await interaction.response.send_message(reload_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
            else:
                try:
                    msgdata = str(
                        self.corecommands_text['reload_command_data'][0])
                    message_data = f'{msgdata} Loaded {module}.'
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
        else:
            try:
                await interaction.response.send_message(str(
                    self.corecommands_text['reload_command_data'][2]))
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    interaction)

    @app_commands.command(name='unload', description='Unloads a specific cog from the bot (Bot owner only).')
    @app_commands.describe(module='The cog to unload.')
    @utils.Checks.is_bot_owner()
    async def unload_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            try:
                ret = await self.bot.unload_plugin(module)
            except CogUnloadError:
                ret = str(traceback.format_exc())
        if self.bot._somebool is True:
            if ret is not None:
                try:
                    reload_data = str(
                        self.corecommands_text['reload_command_data'][1]
                    ).format(ret).replace('Reloading', 'Unloading Plugin')
                    await interaction.response.send_message(reload_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
            else:
                try:
                    msgdata = str(
                        self.corecommands_text['reload_command_data'][0])
                    message_data = f'{msgdata} Unloaded {module}.'
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
        else:
            try:
                await interaction.response.send_message(str(
                    self.corecommands_text['reload_command_data'][2]))
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    interaction)

    @app_commands.command(name='reload', description='Reloads a specific cog on the bot (Bot owner only).')
    @app_commands.describe(module='The cog to reload.')
    @utils.Checks.is_bot_owner()
    async def reload_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            try:
                ret = await self.bot.reload_plugin(module)
            except ImportError:
                ret = str(traceback.format_exc())
        if self.bot._somebool is True:
            if ret is not None:
                try:
                    reload_data = str(
                        self.corecommands_text['reload_command_data'][1]
                    ).format(ret).replace('Reloading', 'Reloading Plugin')
                    await interaction.response.send_message(reload_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
            else:
                try:
                    msgdata = str(
                        self.corecommands_text['reload_command_data'][0])
                    message_data = f'{msgdata} Reloaded {module}.'
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        interaction)
        else:
            try:
                await interaction.response.send_message(str(
                    self.corecommands_text['reload_command_data'][2]))
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    interaction)

    @app_commands.command(name='botban', description='Bans a user from using the bot (Bot owner only).')
    @app_commands.describe(member='The member to ban from the bot.')
    @app_commands.guild_only()
    @utils.Checks.is_bot_owner()
    async def botban_command(self, interaction: discord.Interaction, member: discord.Member):
        """
        Bot Commands.
        :param interaction: Messages.
        :param member: Member.
        :return: Nothing.
        """
        if member.id not in self.bot.banlist['Users']:
            try:
                self.bot.banlist['Users'].append(member.id)
                json.dump(
                    self.bot.banlist,
                    open(os.path.join(
                        sys.path[0], 'resources',
                        'ConfigData', 'BotBanned.json'),
                        "w"))
                try:
                    message_data = str(
                        self.corecommands_text['bot_ban_command_data'][
                            0]).format(member)
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.resolve_send_message_error(
                        self.bot, interaction)
                except Exception as e:
                    str(e)
                    try:
                        messagedata = str(
                            self.corecommands_text[
                                'bot_ban_command_data'][1]).format(
                            member)
                        message_data = messagedata + str(
                            self.corecommands_text[
                                'bot_ban_command_data'][2])
                        await interaction.response.send_message(message_data)
                    except discord.Forbidden:
                        await self.bot.resolve_send_message_error(
                            self.bot, interaction)
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(
                    self.bot, interaction)

    @app_commands.command(name='botunban', description='Unbans a user to use the bot (Bot owner only).')
    @app_commands.describe(member='The member to unban on the bot.')
    @app_commands.guild_only()
    @utils.Checks.is_bot_owner()
    async def botunban_command(self, interaction: discord.Interaction, member: discord.Member):
        """
        Bot Commands.
        :param interaction: Messages.
        :param member: Member.
        :return: Nothing.
        """
        if member.id in self.bot.banlist['Users']:
            try:
                self.bot.banlist['Users'].remove(member.id)
                json.dump(
                    self.bot.banlist,
                    open(os.path.join(
                        sys.path[0], 'resources',
                        'ConfigData', 'BotBanned.json'),
                        "w"))
                try:
                    message_data = str(
                        self.corecommands_text['bot_unban_command_data'][
                            0]).format(member)
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.resolve_send_message_error(
                        self.bot, interaction)
            except Exception as e:
                str(e)
                try:
                    messagedata = str(
                        self.corecommands_text['bot_unban_command_data'][1]).format(member)
                    message_data = messagedata + str(
                        self.corecommands_text['bot_unban_command_data'][2])
                    await interaction.response.send_message(message_data)
                except discord.Forbidden:
                    await self.bot.resolve_send_message_error(
                        self.bot, interaction)


async def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    await bot.add_cog(CoreCommands(bot))
