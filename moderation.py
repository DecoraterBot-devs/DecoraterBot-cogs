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

    @app_commands.command(
        name=app_commands.locale_str('prune', str_id=34),
        description=app_commands.locale_str('Mass delete messages sent by any user.', str_id=35))
    @app_commands.describe(num=app_commands.locale_str('The amount of messages to prune.', str_id=36))
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
            await interaction.followup.send(content=reply_data)

    @app_commands.command(
        name=app_commands.locale_str('clear', str_id=37),
        description=app_commands.locale_str('Clears the messages that was sent by the bot.', str_id=38))
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
            await interaction.followup.send(content=reply_data)

    # Helpers.
    @staticmethod
    async def prune_command_iterator_helper(interaction: discord.Interaction, num: int) -> str:
        """
        Prunes Messages.
        :param interaction: Interaction Context.
        :param num: Some number.
        :return: message string with the number of messages deleted.
        """
        reason = await interaction.translate(app_commands.locale_str('', str_id=26))
        deleted = await interaction.channel.purge(
            limit=num,
            before=interaction.created_at,
            reason=reason)
        result: str = await interaction.translate(app_commands.locale_str('', str_id=27))
        return result.format(len(deleted))

    @staticmethod
    async def clear_command_iterator_helper(interaction: discord.Interaction) -> str:
        """
        Clears the bot's messages.
        :param interaction: Message Context.
        :return: message string with the number of messages deleted.
        """
        reason: str = await interaction.translate(app_commands.locale_str('', str_id=28))
        deleted = await interaction.channel.purge(
            limit=100,
            before=interaction.created_at,
            check=lambda e: e.author == interaction.client.user,
            reason=reason.format(interaction.client.user.name))
        result: str = await interaction.translate(app_commands.locale_str('', str_id=29))
        return result.format(len(deleted))

    @staticmethod
    async def automod_helper(execution: discord.AutoModAction, reason: str):
        if execution.action.type == discord.AutoModRuleActionType.send_alert_message:
            # ban the member.
            await execution.member.ban(
                delete_message_seconds=86400 * 7,
                reason=reason)
            await execution.guild.get_channel(execution.action.channel_id).send(
                content=f'Banned {execution.member.name} for \'{reason}\'.')

    # Events.
    @prune_command.error
    @clear_command.error
    async def on_cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.BotMissingPermissions):
            if interaction.command.name == app_commands.locale_str('prune', str_id=34):
                await interaction.response.send_message(
                    content=await interaction.translate(app_commands.locale_str('', str_id=30)))
            elif interaction.command.name == app_commands.locale_str('clear', str_id=37):
                await interaction.response.send_message(
                    content=await interaction.translate(app_commands.locale_str('', str_id=32)))
        elif isinstance(error, app_commands.MissingPermissions):
            if interaction.command.name == app_commands.locale_str('prune', str_id=34):
                await interaction.response.send_message(
                    content=await interaction.translate(app_commands.locale_str('', str_id=31)))
            elif interaction.command.name == app_commands.locale_str('clear', str_id=37):
                await interaction.response.send_message(
                    content=await interaction.translate(app_commands.locale_str('', str_id=33)))

    @commands.Cog.listener()
    async def on_automod_action(self, execution: discord.AutoModAction):
        if execution.rule_trigger_type == discord.enums.AutoModRuleTriggerType.mention_spam:
            await self.automod_helper(execution, '[AutoMod] Mention Spam')
        elif execution.rule_trigger_type == discord.enums.AutoModRuleTriggerType.harmful_link:
            await self.automod_helper(execution, '[AutoMod] Harmful Link')


async def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    await bot.add_cog(Moderation())
