# coding=utf-8
"""
Normal commands plugin for DecoraterBot.
"""
import random
import sys
import os
import time
from typing import cast

import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils.client import BotClient


class Commands(commands.Cog):
    """
    Normal commands cog for DecoraterBot.
    """

    @app_commands.command(
        name=app_commands.locale_str('coin', str_id=13),
        description=app_commands.locale_str('Flips a coin.', str_id=14))
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(attach_files=True)
    async def coin_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        msg = random.randint(0, 1)
        # when msg is 0.
        heads_coin = os.path.join(
            sys.path[0], 'resources', 'images', 'coins', 'Heads.png')
        # when msg is 1.
        tails_coin = os.path.join(
            sys.path[0], 'resources', 'images', 'coins', 'Tails.png')
        coin = heads_coin if msg != 1 else tails_coin
        await interaction.response.send_message(files=[discord.File(coin)])

    @app_commands.command(
        name=app_commands.locale_str('commands', str_id=15),
        description=app_commands.locale_str('Returns the link to all of the bot\'s commands.', str_id=16))
    async def commands_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        message_data = await interaction.translate(app_commands.locale_str('', str_id=7))
        await interaction.response.send_message(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('source', str_id=17),
        description=app_commands.locale_str('Returns the link to the source code to the bot.', str_id=18))
    async def source_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        message_data: str = await interaction.translate(app_commands.locale_str('', str_id=8))
        message_data = message_data.format(interaction.user.mention)
        await interaction.response.send_message(content=message_data)

    # @app_commands.command(
    #     name='pyversion',
    #     description='Returns the version of python the bot is using.')
    # @app_commands.guild_only()
    # async def pyversion_command(self, interaction: discord.Interaction):
    #     """
    #     Bot Commands.
    #     :param interaction: Messages.
    #     :return: Nothing.
    #     """
    #     bits = ctypes.sizeof(ctypes.c_voidp)
    #     python_platform = "32-Bit" if bits == 4 else "64-Bit"
    #     vers = "```py\nPython v{0} {1}```".format(
    #         platform.python_version(), python_platform)
    #     await interaction.response.send_message(content=vers)

    @app_commands.command(
        name=app_commands.locale_str('stats', str_id=19),
        description=app_commands.locale_str(
            'Returns the number of servers, text channels, and members seen by the discord bot.',
            str_id=20))
    @app_commands.guild_only()
    async def stats_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        server_count = str(len(interaction.client.guilds))
        member_count = 0
        for guild in interaction.client.guilds:
            member_count += guild.member_count
        text_channels_count = str(len(set(
            [channel for channel in interaction.client.get_all_channels() if
             channel.type == discord.ChannelType.text])))
        message_data = await interaction.translate(app_commands.locale_str('', str_id=9))
        message_data = message_data.format(server_count, member_count, text_channels_count)
        await interaction.response.send_message(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('uptime', str_id=21),
        description=app_commands.locale_str('Displays the bot\'s uptime.', str_id=22))
    async def uptime_command(self, interaction: discord.Interaction):
        """
        Command.
        """
        stop = time.time()
        seconds = stop - cast(BotClient, interaction.client).uptime_count_begin
        days: int = int(((seconds / 60) / 60) / 24)
        hours: int = int((seconds / 60) / 60 - (days * 24))
        minutes: int = int((seconds / 60) % 60)
        seconds: int = int(seconds % 60)
        message_data = await interaction.translate(app_commands.locale_str('', str_id=10))
        message_data = message_data.format(days, hours, minutes, seconds)
        await interaction.response.send_message(content=message_data)

    @app_commands.command(
        name=app_commands.locale_str('userinfo', str_id=23),
        description=app_commands.locale_str('Displays user information of the current or a specific user.', str_id=24))
    @app_commands.describe(member=app_commands.locale_str(
        'The optional user to display the information on.',
        str_id=25))
    @app_commands.guild_only()
    async def userinfo_command(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        Bot Commands.
        :param interaction: Messages.
        :param member: Optional User.
        :return: Nothing.
        """
        await self.userinfo_helper(interaction, member if member is not None else interaction.user)

    @coin_command.error
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                await interaction.translate(app_commands.locale_str('', str_id=12)))

    # Helpers.
    @staticmethod
    async def userinfo_helper(interaction: discord.Interaction, _member: discord.Member):
        seen_in = str(len(_member.mutual_guilds))
        message_data = await interaction.translate(app_commands.locale_str('', str_id=11))
        message_data = message_data.format(
            _member, seen_in,
            discord.utils.format_dt(_member.joined_at),
            discord.utils.format_dt(_member.created_at),
            'None' if _member.voice is None else _member.voice.channel.name, '\n')
        embed = discord.Embed(description=message_data)
        embed.colour = 0xff3d00
        embed.set_thumbnail(url=_member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """
    DecoraterBot's various commands Plugin.
    """
    await bot.add_cog(Commands())
