# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
import discord
from discord import app_commands
from discord.ext import commands
import nsfw_dl
from nsfw_dl import errors
from DecoraterBotUtils import Checks, readers


class NSFW(commands.Cog):
    """
    NSFW Commands Plugin Class.
    """
    def __init__(self):
        self.nsfw_text = readers.PluginTextReader(
            file='nsfw.json').get_config

    @app_commands.command(
        name='rule34',
        description='Searches rule34 for some images.',
        nsfw=True)
    @Checks.is_user_bot_banned()
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
                    content=self.nsfw_text['nsfw_plugin_data'][0])
        else:
            with nsfw_dl.NSFWDL() as dl:
                await self.image_helper(
                    dl.download("Rule34Random"),
                    interaction)

    async def image_helper(self, image, interaction: discord.Interaction):
        await interaction.followup.send(
            content=image if image is not None else self.nsfw_text['nsfw_plugin_data'][2])


async def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    await bot.add_cog(NSFW())
