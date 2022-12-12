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


class Commands(commands.Cog):
    """
    Normal commands cog for DecoraterBot.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='coin', description='Flips a coin.')
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
        name='commands',
        description='Returns the link to all of the bot\'s commands.')
    async def commands_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        message_data = 'All of the bot\'s commands are listed at <https://github.com/DecoraterBot-devs/DecoraterBot-docs/blob/master/Commands.md>.'
        await interaction.response.send_message(content=message_data)

    @app_commands.command(
        name='source',
        description='Returns the link to the source code to the bot.')
    async def source_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        message_data = f'{interaction.user.mention} <https://github.com/DecoraterBot-Devs/DecoraterBot/>'
        await interaction.response.send_message(content=message_data)

    @app_commands.command(
        name='pyversion',
        description='Returns the version of python the bot is using.')
    @app_commands.guild_only()
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
        await interaction.response.send_message(content=vers)

    @app_commands.command(
        name='stats',
        description='Returns the number of servers, text channels, and members seen by the discord bot.')
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
        textchannels_count = str(len(set(
            [channel for channel in interaction.client.get_all_channels() if
             channel.type == discord.ChannelType.text])))
        message_data = f'Connected to {server_count} servers with {member_count} members in {textchannels_count} text-channels.'
        await interaction.response.send_message(content=message_data)

    @app_commands.command(name='uptime', description='Displays the bot\'s uptime.')
    async def uptime_command(self, interaction: discord.Interaction):
        """
        Command.
        """
        stop = time.time()
        seconds = stop - self.bot.uptime_count_begin
        days: int = int(((seconds / 60) / 60) / 24)
        hours: int = int((seconds / 60) / 60 - (days * 24))
        minutes: int = int((seconds / 60) % 60)
        seconds: int = int(seconds % 60)
        await interaction.response.send_message(
            f'Uptime: **{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds**')

    @app_commands.command(
        name='userinfo',
        description='Displays user information of the current or a specific user.')
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
                'This bot does not have Permission to Attach Files.')

    # Helpers.
    @staticmethod
    async def userinfo_helper(interaction: discord.Interaction, _member: discord.Member):
        seenin = str(len(_member.mutual_guilds))
        voicechannel = "None" if _member.voice is None else _member.voice.channel.name
        message_data = 'Display Name: {0.display_name}#{0.discriminator}\nID: {0.id}\nStatus: {0.status}\nVoice Channels: {4}\nJoined: {2}\nCreated At: {3}\nSeen In: {1} servers.\nBot: {0.bot}'.format(
            _member, seenin,
            discord.utils.format_dt(_member.joined_at),
            discord.utils.format_dt(_member.created_at),
            voicechannel)
        embed = discord.Embed(description=message_data)
        embed.colour = 0xff3d00
        embed.set_thumbnail(url=_member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """
    DecoraterBot's various commands Plugin.
    """
    await bot.add_cog(Commands(bot))
