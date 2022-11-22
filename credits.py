# coding=utf-8
"""
credits Plugin for DecoraterBot.
"""
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils import utils


class Credits(commands.Cog):
    """
    Credits Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.credits_text = utils.PluginTextReader(
            file='credits.json')

    @app_commands.command(name='credits', description='Gives the user 500 daily credits.')
    @utils.Checks.is_user_bot_banned()
    async def credits_command(self, interaction: discord.Interaction):
        """
        /credits Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(interaction.user.id), 'credits')
            except (KeyError, TypeError):
                pass
            self.bot.credits.setcredits(
                str(interaction.user.id), 'credits', current_credits + 500)
            await interaction.response.send_message(
                    self.credits_text['credits_plugin_data'][0].format(
                        interaction.user.name))
        except Exception:
            await interaction.response.send_message(
                    self.credits_text['credits_plugin_data'][3].format(
                        traceback.format_exc()))

    @app_commands.command(
        name='givecredits',
        description='Allows a user to give some or all of their credits to another user.')
    @app_commands.describe(
        user='The user to give some or all of your credits to.',
        creditnum='The number of credits to give.')
    @utils.Checks.is_user_bot_banned()
    async def givecredits_command(self, interaction: discord.Interaction, user: discord.User, creditnum: int):
        """
        /givecredits Command for DecoraterBot.
        """
        current_credits = 0
        current_credits2 = 0
        try:
            current_credits = self.bot.credits.getcredits(
                str(interaction.user.id), 'credits')
        except (KeyError, TypeError):
            pass
        try:
            current_credits2 = self.bot.credits.getcredits(
                str(user.id), 'credits')
        except (KeyError, TypeError):
            pass
        if creditnum > -1:
            if current_credits > creditnum:
                try:
                    self.bot.credits.setcredits(
                        str(interaction.user.id), 'credits',
                        current_credits - creditnum)
                    self.bot.credits.setcredits(
                        str(user.id), 'credits',
                        current_credits2 + creditnum)
                    await interaction.response.send_message(
                        self.credits_text['credits_plugin_data'][1].format(
                            interaction.user.name, creditnum, user.name))
                except Exception:
                    await interaction.response.send_message(
                        self.credits_text['credits_plugin_data'][3].format(
                            traceback.format_exc()))
            else:
                await interaction.response.send_message(
                    self.credits_text['credits_plugin_data'][5].format(creditnum, user.name))
        else:
            await interaction.response.send_message(
                self.credits_text['credits_plugin_data'][4])

    @app_commands.command(name='balance', description='Allows the user to check their credit balance.')
    @utils.Checks.is_user_bot_banned()
    async def balance_command(self, interaction: discord.Interaction):
        """
        /balance Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(interaction.user.id), 'credits')
            except (KeyError, TypeError):
                pass
            await interaction.response.send_message(
                    self.credits_text['credits_plugin_data'][2].format(
                        interaction.user.name, current_credits))
        except Exception:
            await interaction.response.send_message(
                    self.credits_text['credits_plugin_data'][3].format(
                        traceback.format_exc()))


async def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    await bot.add_cog(Credits(bot))
