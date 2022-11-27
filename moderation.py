# coding=utf-8
"""
moderation plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    """
    Moderation Commands Extension to the
    default DecoraterBot Moderation commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='ban',
        description='Bans a specific user from the guild.')
    @app_commands.describe(
        member='The member to ban from the guild.',
        reason='The reason for the ban.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
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
                reply_data = f'{member.name} was banned from the server.'
            except discord.HTTPException:
                reply_data = 'Banning failed.'
        else:
            reply_data = 'No user specified to ban.'
        await interaction.response.send_message(content=reply_data)

    @app_commands.command(
        name='softban',
        description='Soft Bans a specific user from the guild.')
    @app_commands.describe(
        member='The member to soft ban from the guild.',
        reason='The reason for the soft ban.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
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
                reply_data = f'{member.name} was softbanned from the server.'
            except discord.HTTPException:
                reply_data = 'Softbanning failed.'
        else:
            reply_data = 'No user specified to Softban.'
        await interaction.response.send_message(content=reply_data)

    @app_commands.command(
        name='kick',
        description='Kicks a specific user from the guild.')
    @app_commands.describe(
        member='The member to kick from the guild.',
        reason='The reason for the kick.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
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
                reply_data = f'{member.name} was kicked from the server.'
            except discord.HTTPException:
                reply_data = 'Kicking failed.'
        else:
            reply_data = 'No user specified to kick.'
        await interaction.response.send_message(content=reply_data)

    @app_commands.command(
        name='prune',
        description='Mass delete messages sent by any user.')
    @app_commands.describe(num='The amount of messages to prune.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(send_messages=True, manage_messages=True)
    @app_commands.checks.bot_has_permissions(send_messages=True, manage_messages=True)
    async def prune_command(self, interaction: discord.Interaction, num: app_commands.Range[int, 1, 100] = 1):
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
                await interaction.channel.send(content=reply_data)
            except discord.Forbidden:
                await self.bot.resolve_send_message_error(
                        interaction)

    @app_commands.command(
        name='clear',
        description='Clears the messages that was sent by the bot.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(send_messages=True)
    @app_commands.checks.bot_has_permissions(send_messages=True)
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
                await interaction.channel.send(content=reply_data)
            except discord.Forbidden:
                await self.bot.resolve_send_message_error(
                    interaction)

    # Helpers.
    @staticmethod
    async def prune_command_iterator_helper(interaction: discord.Interaction, num: int):
        """
        Prunes Messages.
        :param interaction: Interaction Context.
        :param num: Some number.
        :return: message string on Error, nothing otherwise.
        """
        deleted = await interaction.channel.purge(
            limit=num + 1,
            reason='Recent user messages purge.')
        return f"Deleted {len(deleted)} messages."

    async def clear_command_iterator_helper(self, interaction: discord.Interaction):
        """
        Clears the bot's messages.
        :param interaction: Message Context.
        :return: Nothing.
        """
        await interaction.channel.purge(
            limit=100,
            check=lambda e: e.author == self.bot.user,
            reason=f'{self.bot.user.name} message clear.')
        return "Deleted the bot's messages."

    @ban_command.error
    @softban_command.error
    async def on_ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                content="The bot needs the 'ban members' permission for this.")
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                content="You need the 'ban members' permission for this.")

    @kick_command.error
    async def on_kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                content="The bot needs the 'kick members' permission for this.")
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                content="You need the 'kick members' permission for this.")

    @prune_command.error
    async def on_prune_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                content="The bot needs the 'manage messages' and the 'send messages' permissions for this.")
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                content="You need the 'manage messages' and the 'send messages' permissions for this.")

    @clear_command.error
    async def on_clear_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                content="The bot needs the 'send messages' permission for this.")
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                content="You need the 'send messages' permission for this.")


async def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    await bot.add_cog(Moderation(bot))
