# coding=utf-8
"""
moderation plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils import utils, readers


# This module's warn, and mute commands do not work for now.
# I would like it if someone would help me fix them and pull
# request the fixtures to this file to make them work.


class Moderation(commands.Cog):
    """
    Moderation Commands Extension to the
    default DecoraterBot Moderation commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.moderation_text = readers.PluginTextReader(
            file='moderation.json').get_config

    @app_commands.command(
        name='ban',
        description='Bans a specific user from the guild (Requires \'Bot Commander\' role).')
    @app_commands.describe(
        member='The member to ban from the guild.',
        reason='The reason for the ban.')
    @app_commands.guild_only()
    @app_commands.checks.has_role('Bot Commander')
    @utils.Checks.is_user_bot_banned()
    async def ban_command(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """
        Bot Commands.
        :param interaction: Interaction.
        :param member: Member.
        :param reason: reason.
        :return: Nothing.
        """
        if member is not None:
            try:
                await interaction.guild.ban(member, delete_message_days=7, reason=reason)
                reply_data = self.moderation_text['ban_command_data'][0].format(
                    member)
            except discord.Forbidden:
                reply_data = self.moderation_text['ban_command_data'][1]
            except discord.HTTPException:
                reply_data = self.moderation_text['ban_command_data'][2]
        else:
            reply_data = self.moderation_text['ban_command_data'][3]
        try:
            await interaction.response.send_message(content=reply_data)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                interaction)

    @app_commands.command(
        name='softban',
        description='Soft Bans a specific user from the guild (Requires \'Bot Commander\' role).')
    @app_commands.describe(
        member='The member to soft ban from the guild.',
        reason='The reason for the soft ban.')
    @app_commands.guild_only()
    @app_commands.checks.has_role('Bot Commander')
    @utils.Checks.is_user_bot_banned()
    async def softban_command(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """
        Bot Commands.
        :param interaction: Interaction.
        :param member: Member.
        :param reason: reason.
        :return: Nothing.
        """
        if member is not None:
            try:
                await interaction.guild.ban(member, delete_message_days=7, reason=reason)
                await interaction.guild.unban(member, reason=reason)
                reply_data = self.moderation_text['softban_command_data'][0].format(
                    member)
            except discord.Forbidden:
                reply_data = self.moderation_text['softban_command_data'][1]
            except discord.HTTPException:
                reply_data = self.moderation_text['softban_command_data'][2]
        else:
            reply_data = self.moderation_text['softban_command_data'][3]
        try:
            await interaction.response.send_message(content=reply_data)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                interaction)

    @app_commands.command(
        name='kick',
        description='Kicks a specific user from the guild (Requires \'Bot Commander\' role).')
    @app_commands.describe(
        member='The member to kick from the guild.',
        reason='The reason for the kick.')
    @app_commands.guild_only()
    @app_commands.checks.has_role('Bot Commander')
    @utils.Checks.is_user_bot_banned()
    async def kick_command(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """
        Bot Commands.
        :param interaction: Interaction.
        :param member: Member.
        :param reason: reason.
        :return: Nothing.
        """
        if member is not None:
            try:
                await interaction.guild.kick(member, reason=reason)
                reply_data = self.moderation_text['kick_command_data'][0].format(
                    member)
            except discord.Forbidden:
                reply_data = self.moderation_text['kick_command_data'][1]
            except discord.HTTPException:
                reply_data = self.moderation_text['kick_command_data'][2]
        else:
            reply_data = self.moderation_text['kick_command_data'][3]
        try:
            await interaction.response.send_message(content=reply_data)
        except discord.Forbidden:
            await self.bot.resolve_send_message_error(
                interaction)

    @app_commands.command(
        name='prune',
        description='Mass delete messages sent by any user (Requires \'Bot Commander\' role).')
    @app_commands.describe(num='The amount of messages to prune.')
    @app_commands.guild_only()
    @app_commands.checks.has_role('Bot Commander')
    @utils.Checks.is_user_bot_banned()
    async def prune_command(self, interaction: discord.Interaction, num: int = 1):
        """
        Bot Commands.
        :param interaction: Interaction.
        :param num: Some number.
        :return: Nothing.
        """
        await interaction.response.defer(thinking=True)
        reply_data = await self.prune_command_iterator_helper(interaction, num)
        if reply_data is not None:
            try:
                await interaction.response.send_message(content=reply_data)
            except discord.Forbidden:
                await self.bot.resolve_send_message_error(
                        interaction)

    @app_commands.command(
        name='clear',
        description='Clears the messages that was sent by the bot.')
    @app_commands.guild_only()
    @utils.Checks.is_user_bot_banned()
    async def clear_command(self, interaction: discord.Interaction):
        """
        Bot Commands.
        :param interaction: Messages.
        :return: Nothing.
        """
        await interaction.response.defer(thinking=True)
        reply_data = await self.clear_command_iterator_helper(interaction)
        if reply_data is not None:
            try:
                await interaction.response.send_message(content=reply_data)
            except discord.Forbidden:
                await self.bot.resolve_send_message_error(
                    interaction)

    # Helpers.
    async def prune_command_iterator_helper(self, interaction: discord.Interaction, num: int):
        """
        Prunes Messages.
        :param interaction: Interaction Context.
        :param num: Some number.
        :return: message string on Error, nothing otherwise.
        """
        try:
            await interaction.channel.purge(
                limit=num + 1,
                reason='Recent user messages purge.')
            return None
        except discord.HTTPException:
            messages = [message async for message in
                        interaction.channel.history(limit=num + 1)]
            try:
                await interaction.channel.delete_messages(messages)
            except discord.HTTPException:
                return self.moderation_text['prune_command_data'][0]
        finally:
            return f"Deleted {num + 1} messages."

    async def clear_command_iterator_helper(self, interaction: discord.Interaction):
        """
        Clears the bot's messages.
        :param interaction: Message Context.
        :return: Nothing.
        """
        try:
            await interaction.channel.purge(
                limit=100,
                check=lambda e: e.author == self.bot.user,
                reason=f'{self.bot.user.name} message clear.')
        except discord.HTTPException:
            messages = [message async for message in interaction.channel.history(
                limit=100,
                check=lambda e: e.author == self.bot.user)]
            try:
                await interaction.channel.delete_messages(
                    messages=messages,
                    reason=f'{self.bot.user.name} message clear.')
            except discord.HTTPException:
                return "Failed to delete the bot's messages."
        finally:
            return "Deleted the bot's messages."


async def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    await bot.add_cog(Moderation(bot))
