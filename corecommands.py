# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils import Checks


class CoreCommands(commands.Cog):
    """
    Core Commands class for DecoraterBot.
    """
    def __init__(self, bot):
        self.bot = bot
        self.reload_command_data = [
            ':ok:',
            'Reloading Plugin Failed.\n```py\n{0}\n```',
            'No Module specified to reload.',
            'Sorry, Only my owner can load, unload, and reload modules.']

    @app_commands.command(name='load', description='Loads a specific cog into the bot (Bot owner only).')
    @app_commands.describe(module='The cog to load.')
    @Checks.is_bot_owner()
    async def load_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            try:
                ret = await self.bot.load_bot_extension(module)
            except ImportError:
                ret = str(traceback.format_exc())
        if self.bot._somebool is True:
            if ret is not None:
                reload_data = self.reload_command_data[1].format(
                    ret).replace('Reloading', 'Loading')
                await interaction.response.send_message(reload_data)
            else:
                message_data = f'{self.reload_command_data[0]} Loaded {module}.'
                await interaction.response.send_message(message_data)
        else:
            await interaction.response.send_message(
                self.reload_command_data[2].replace('reload', 'load'))

    @app_commands.command(name='unload', description='Unloads a specific cog from the bot (Bot owner only).')
    @app_commands.describe(module='The cog to unload.')
    @Checks.is_bot_owner()
    async def unload_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            ret = await self.bot.unload_bot_extension(module)
        if self.bot._somebool is True:
            if ret is not None:
                reload_data = self.reload_command_data[1].format(
                    ret).replace('Reloading', 'Unloading')
                await interaction.response.send_message(reload_data)
            else:
                message_data = f'{self.reload_command_data[0]} Unloaded {module}.'
                await interaction.response.send_message(message_data)
        else:
            await interaction.response.send_message(
                self.reload_command_data[2].replace('reload', 'unload'))

    @app_commands.command(name='reload', description='Reloads a specific cog on the bot (Bot owner only).')
    @app_commands.describe(module='The cog to reload.')
    @Checks.is_bot_owner()
    async def reload_command(self, interaction: discord.Interaction, module: str):
        """
        Command.
        """
        self.bot._somebool = False
        ret = ""
        if module != '':
            self.bot._somebool = True
            try:
                ret = await self.bot.reload_bot_extension(module)
            except ImportError:
                ret = str(traceback.format_exc())
        if self.bot._somebool is True:
            if ret is not None:
                reload_data = self.reload_command_data[1].format(
                    ret).replace('Reloading', 'Reloading')
                await interaction.response.send_message(reload_data)
            else:
                message_data = f'{self.reload_command_data[0]} Reloaded {module}.'
                await interaction.response.send_message(message_data)
        else:
            await interaction.response.send_message(self.reload_command_data[2])

    @app_commands.command(name='sync', description='Syncs all of the bot\'s global commands (Bot owner only).')
    @Checks.is_bot_owner()
    async def sync_command(self, interaction: discord.Interaction):
        synced = await interaction.client.tree.sync()
        await interaction.response.send_message(f'Synced {len(synced)} commands globally.')

    @load_command.error
    @unload_command.error
    @reload_command.error
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(self.reload_command_data[3])


async def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    await bot.add_cog(CoreCommands(bot))
