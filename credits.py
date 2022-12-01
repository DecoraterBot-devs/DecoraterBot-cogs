# coding=utf-8
"""
credits Plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands
from DecoraterBotUtils.readers import BaseConfigReader


class Credits(commands.Cog):
    """
    Credits Commands Plugin Class.
    """

    @app_commands.command(name='credits', description='Gives the user 500 daily credits.')
    async def credits_command(self, interaction: discord.Interaction):
        """
        /credits Command for DecoraterBot.
        """
        current_credits: int = 0
        async with BaseConfigReader(file='credits.json') as _credits:
            try:
                current_credits = _credits[str(interaction.user.id)]['credits']
            except (KeyError, TypeError):
                pass
            _credits[str(interaction.user.id)]['credits'] = current_credits + 500
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
        current_credits: int = 0
        current_credits2: int = 0
        async with BaseConfigReader(file='credits.json') as _credits:
            try:
                current_credits = _credits[str(interaction.user.id)]['credits']
            except (KeyError, TypeError):
                pass
            try:
                current_credits2 = _credits[str(user.id)]['credits']
            except (KeyError, TypeError):
                pass
            if -1 < creditnum < current_credits:
                _credits[str(interaction.user.id)]['credits'] = current_credits - creditnum
                _credits[str(user.id)]['credits'] = current_credits2 + creditnum
        if creditnum > -1:
            if current_credits > creditnum:
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
        current_credits: int = 0
        async with BaseConfigReader(file='credits.json') as _credits:
            try:
                current_credits = _credits[str(interaction.user.id)]['credits']
            except (KeyError, TypeError):
                pass
        await interaction.response.send_message(
            f'{interaction.user.name}, you have :dollar: {current_credits} credits!')


async def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    await bot.add_cog(Credits())
