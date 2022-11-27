# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands
import nsfw_dl
from nsfw_dl import errors


class NSFW(commands.Cog):
    """
    NSFW Commands Plugin Class.
    """

    @app_commands.command(
        name='rule34',
        description='Searches rule34 for some images.',
        nsfw=True)
    @app_commands.describe(searchterm='The tag to search with.')
    async def rule34_command(self, interaction: discord.Interaction, searchterm: str = ''):
        """
        /rule34 Search Command for DecoraterBot.
        """
        await interaction.response.defer(thinking=True)
        if searchterm != '':
            try:
                with nsfw_dl.NSFWDL() as dl:
                    await self.image_helper(
                        dl.download(
                            "Rule34Search",
                            args=searchterm),
                        interaction)
            except nsfw_dl.errors.NoResultsFound:
                await interaction.followup.send(
                    content='Sorry, could not find an image from the search.')
        else:
            with nsfw_dl.NSFWDL() as dl:
                await self.image_helper(
                    dl.download("Rule34Random"),
                    interaction)

    @staticmethod
    async def image_helper(image, interaction: discord.Interaction):
        await interaction.followup.send(
            content=image if image is not None else 'Error while getting an image.')


async def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    await bot.add_cog(NSFW())
