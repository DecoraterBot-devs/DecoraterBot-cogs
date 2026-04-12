# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands


class CoreCommands(commands.Cog):
    """
    Core Commands class for DecoraterBot.
    """

    @app_commands.command(
        name=app_commands.locale_str('load', str_id=40),
        description=app_commands.locale_str('Loads a specific cog into the bot (Bot owner only).', str_id=41))
    @app_commands.guild_only()
    async def load_command(self, interaction: discord.Interaction, module: str):
        """
        Loads a specific cog into the bot (Bot owner only).
        """
        await interaction.response.defer(thinking=True)
        if interaction.client.is_owner(interaction.user):
            ret = await interaction.client.load_bot_extension(module)
            message_data: str = ((await interaction.translate(
                app_commands.locale_str('', str_id=42 if ret is not None else 43)))
                                 .format(ret if ret is not None else module))
            await interaction.followup.send(content=message_data)
        else:
            message_data = await interaction.translate(app_commands.locale_str('', str_id=39))
            await interaction.followup.send(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('unload', str_id=44),
        description=app_commands.locale_str('Unloads a specific cog from the bot (Bot owner only).', str_id=45))
    @app_commands.guild_only()
    async def unload_command(self, interaction: discord.Interaction, module: str):
        """
        Unloads a specific cog from the bot (Bot owner only).
        """
        await interaction.response.defer(thinking=True)
        if interaction.client.is_owner(interaction.user):
            ret = await interaction.client.unload_bot_extension(module)
            message_data: str = ((
                await interaction.translate(
                    app_commands.locale_str('', str_id=46 if ret is not None else 47)))
                                 .format(ret if ret is not None else module))
            await interaction.followup.send(content=message_data)
        else:
            message_data = await interaction.translate(app_commands.locale_str('', str_id=39))
            await interaction.followup.send(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('reload', str_id=48),
        description=app_commands.locale_str('Reloads a specific cog on the bot (Bot owner only).', str_id=49))
    @app_commands.guild_only()
    async def reload_command(self, interaction: discord.Interaction, module: str):
        """
        Reloads a specific cog on the bot (Bot owner only).
        """
        await interaction.response.defer(thinking=True)
        if interaction.client.is_owner(interaction.user):
            ret = await interaction.client.reload_bot_extension(module)
            message_data: str = ((
                await interaction.translate(
                    app_commands.locale_str('', str_id=50 if ret is not None else 51)))
                                 .format(ret if ret is not None else module))
            await interaction.followup.send(content=message_data)
        else:
            message_data = await interaction.translate(app_commands.locale_str('', str_id=39))
            await interaction.followup.send(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('sync', str_id=52),
        description=app_commands.locale_str("Syncs all the bot's global commands (Bot owner only).", str_id=53))
    @app_commands.guild_only()
    async def sync_command(self, interaction: discord.Interaction):
        """
        Syncs all the bot's global commands (Bot owner only).
        """
        await interaction.response.defer(thinking=True)
        if interaction.client.is_owner(interaction.user):
            synced = await interaction.client.tree.sync()
            message_data: str = ((await interaction.translate(
                app_commands.locale_str('', str_id=54))).format(len(synced)))
            await interaction.followup.send(content=message_data)
        else:
            message_data = await interaction.translate(app_commands.locale_str('', str_id=39))
            await interaction.followup.send(content=message_data)


async def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    await bot.add_cog(CoreCommands())
