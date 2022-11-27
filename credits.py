# coding=utf-8
"""
credits Plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands


class Credits(commands.Cog):
    """
    Credits Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='credits', description='Gives the user 500 daily credits.')
    async def credits_command(self, interaction: discord.Interaction):
        """
        /credits Command for DecoraterBot.
        """
        current_credits = 0
        try:
            current_credits = self.bot.credits.getcredits(
                str(interaction.user.id), 'credits')
        except (KeyError, TypeError):
            pass
        self.bot.credits.setcredits(
            str(interaction.user.id), 'credits', current_credits + 500)
        await interaction.response.send_message(
                f':atm:  |  {interaction.user.name}, you received your :dollar: 500 daily credits!')

    @app_commands.command(
        name='givecredits',
        description='Allows a user to give some or all of their credits to another user.')
    @app_commands.describe(
        user='The user to give some or all of your credits to.',
        creditnum='The number of credits to give.')
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
                self.bot.credits.setcredits(
                    str(interaction.user.id), 'credits',
                    current_credits - creditnum)
                self.bot.credits.setcredits(
                    str(user.id), 'credits',
                    current_credits2 + creditnum)
                await interaction.response.send_message(
                    f'{interaction.user.name}, you have transferred :dollar: {creditnum} credits to {user.name}!')
            else:
                await interaction.response.send_message(
                    f'You do not have enough credits to transfer :dollar: {creditnum} to {user.name}.')
        else:
            await interaction.response.send_message('You cannot transfer negative credits.')

    @app_commands.command(name='balance', description='Allows the user to check their credit balance.')
    async def balance_command(self, interaction: discord.Interaction):
        """
        /balance Command for DecoraterBot.
        """
        current_credits = 0
        try:
            current_credits = self.bot.credits.getcredits(
                str(interaction.user.id), 'credits')
        except (KeyError, TypeError):
            pass
        await interaction.response.send_message(
            f'{interaction.user.name}, you have :dollar: {current_credits} credits!')


async def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    await bot.add_cog(Credits(bot))
