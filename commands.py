# coding=utf-8
"""
Normal commands plugin for DecoraterBot.
"""
import platform
import random
import sys
import ctypes
import os
import time

import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils import Checks, readers


class Commands(commands.Cog):
    """
    Normal commands cog for DecoraterBot.
    """
    def __init__(self, bot):
        self.bot = bot
        self.commands_text = readers.PluginTextReader(
            file='commands.json').get_config
        self.version = str(bot.consoletext['WindowVersion'][0])
        self.rev = str(bot.consoletext['Revision'][0])
        self.sourcelink = str(self.commands_text['source_command_data'][0])
        self.botcommands = str(
            self.commands_text['commands_command_data'][
                0])
        self.changelog = str(self.commands_text['changelog_data'][0])
        self.info = "``" + str(bot.consoletext['WindowName'][
            0]) + self.version + self.rev + "``"

    @app_commands.command(name='coin', description='Flips a coin.')
    @app_commands.guild_only()
    @Checks.is_user_bot_banned()
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
        try:
            await interaction.response.send_message(files=[discord.File(coin)])
        except discord.Forbidden:
            try:
                message_data = str(
                    self.commands_text['coin_command_data'][0])
                await interaction.response.send_message(content=message_data)
            except discord.Forbidden:
                await self.bot.resolve_send_message_error(
                    self.bot, interaction)

    @app_commands.command(
        name='commands',
        description='Returns the link to all of the bot\'s commands.')
    @Checks.is_user_bot_banned()
    async def commands_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        try:
            await interaction.response.send_message(content=self.botcommands)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                self.bot, interaction)

    @app_commands.command(
        name='source',
        description='Returns the link to the source code to the bot.')
    @Checks.is_user_bot_banned()
    async def source_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        try:
            msgdata = self.sourcelink.format(interaction.user)
            message_data = msgdata
            await interaction.response.send_message(content=message_data)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                self.bot, interaction)

    @app_commands.command(
        name='pyversion',
        description='Returns the version of python the bot is using.')
    @app_commands.guild_only()
    @Checks.is_user_bot_banned()
    async def pyversion_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        bits = ctypes.sizeof(ctypes.c_voidp)
        python_platform = "32-Bit" if bits == 4 else "64-Bit"
        vers = "```py\nPython v{0} {1}```".format(
            platform.python_version(), python_platform)
        try:
            await interaction.response.send_message(content=vers)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                self.bot, interaction)

    @app_commands.command(
        name='stats',
        description='Returns the number of servers, text channels, and members seen by the discord bot.')
    @app_commands.guild_only()
    @Checks.is_user_bot_banned()
    async def stats_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        server_count = str(len(self.bot.guilds))
        member_count = 0
        for guild in self.bot.guilds:
            member_count += guild.member_count
        textchannels_count = str(len(set(
            [channel for channel in self.bot.get_all_channels() if
             channel.type == discord.ChannelType.text])))
        formatted_data = str(
            self.commands_text['stats_command_data'][0]
        ).format(server_count, member_count, textchannels_count)
        await interaction.response.send_message(content=formatted_data)

    @app_commands.command(name='uptime', description='Displays the bot\'s uptime.')
    @Checks.is_user_bot_banned()
    async def uptime_command(self, interaction: discord.Interaction):
        """
        Command.
        """
        stop = time.time()
        seconds = stop - self.bot.uptime_count_begin
        days = int(((seconds / 60) / 60) / 24)
        hours = str(int((seconds / 60) / 60 - (days * 24)))
        minutes = str(int((seconds / 60) % 60))
        seconds = str(int(seconds % 60))
        days = str(days)
        time_001 = str(self.commands_text['Uptime_command_data'][0]).format(
            days, hours, minutes, seconds)
        try:
            await interaction.response.send_message(time_001)
        except discord.Forbidden:
            return

    @app_commands.command(
        name='userinfo',
        description='Displays user information of the current or a specific user.')
    @app_commands.guild_only()
    @Checks.is_user_bot_banned()
    async def userinfo_command(self, interaction: discord.Interaction, member: discord.Member=None):
        """
        Bot Commands.
        :param interaction: Messages.
        :param member: Optional User.
        :return: Nothing.
        """
        await self.userinfo_helper(interaction, member if member is not None else interaction.user)

    # Helpers.
    async def userinfo_helper(self, interaction: discord.Interaction, _member: discord.Member):
        seenin = str(len(_member.mutual_guilds))
        voicechannel = "None" if _member.voice is None else _member.voice.channel.name
        msgdata_1 = self.commands_text['userinfo_command_data'][0].format(
            _member, seenin,
            discord.utils.format_dt(_member.joined_at),
            discord.utils.format_dt(_member.created_at),
            voicechannel)
        message_data = msgdata_1 if str(_member.activity) != 'None' else msgdata_1.replace(
            "Playing ", "")
        try:
            embed = discord.Embed(description=message_data)
            embed.colour = 0xff3d00
            embed.set_thumbnail(url=_member.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                self.bot, interaction)


async def setup(bot):
    """
    DecoraterBot's various commands Plugin.
    """
    await bot.add_cog(Commands(bot))
