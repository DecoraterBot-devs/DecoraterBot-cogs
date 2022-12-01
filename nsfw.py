# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands
import nsfw_dl


class NSFW(commands.Cog):
    """
    NSFW Commands Plugin Class.
    """

    @app_commands.command(
        name='nsfw',
        description='Searches a service for some nsfw images.',
        nsfw=True)
    @app_commands.describe(
        name='The name of the service to look for the image from.',
        searchterm='The tag to search with.')
    async def nsfw_command(self, interaction: discord.Interaction, name: str = '', searchterm: str = ''):
        """
        /nsfw Search Command for DecoraterBot for specific loaders.
        """
        await interaction.response.defer(thinking=True)
        loader = f'{name.capitalize()}Search' if searchterm != '' else f'{name.capitalize()}Random'
        if name in nsfw_dl.SOURCES.keys():
            if loader not in nsfw_dl.SOURCES[name]:
                searchterm = ''
                loader = loader.replace('Search', 'Random')
        await self.nsfw_helper(interaction, loader, searchterm)

    async def nsfw_helper(self, interaction: discord.Interaction, loader: str, searchterm: str):
        try:
            if searchterm != '':
                async with nsfw_dl.NSFWDL() as dl:
                    await self.image_helper(await dl.download(loader, args=searchterm), interaction)
            else:
                async with nsfw_dl.NSFWDL() as dl:
                    await self.image_helper(await dl.download(loader), interaction)
        except nsfw_dl.errors.NoResultsFound:
            await interaction.followup.send(
                content='Sorry, could not find an image from the search.')
        except nsfw_dl.errors.NoLoader:
            sources = ''
            for source in nsfw_dl.SOURCES.keys():
                sources += f'- {source}\n'
            await interaction.followup.send(
                content=f'name must be one of:\n{sources}')

    @staticmethod
    async def image_helper(image, interaction: discord.Interaction):
        await interaction.followup.send(
            content=image if image is not None else 'Error while getting an image.')


async def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    await bot.add_cog(NSFW())
