# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
import random

import discord
from discord.ext import commands
import nsfw_dl
from DecoraterBotUtils import utils, readers


class NSFW(commands.Cog):
    """
    NSFW Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.image = None
        self.nsfw_text = readers.PluginTextReader(
            file='nsfw.json').get_config

    @commands.command(name='rule34', pass_context=True)
    async def rule34_command(self, interaction: discord.Interaction, searchterm: str = ''):
        """
        /rule34 Search Command for DecoraterBot.
        """
        if searchterm != '':
            imageerr = None
            try:
                self.image = await nsfw_dl.rule34_search(
                    searchterm, self.bot.http.__session)
            except nsfw_dl.errors.NoResultsFound:
                self.image = None
                imageerr = self.nsfw_text['nsfw_plugin_data'][0]
            if self.image is -1:
                await interaction.response.send_message(
                    content=self.nsfw_text['nsfw_plugin_data'][1])
            else:
                if self.image is not None:
                    await interaction.response.send_message(
                        content='http:' + random.choice(self.image))
                else:
                    if imageerr is not None:
                        await interaction.response.send_message(
                            content=imageerr)
                    else:
                        await interaction.response.send_message(
                            content=self.nsfw_text['nsfw_plugin_data'][2])
        else:
            self.image = await nsfw_dl.rule34_random(self.bot.http.__session)
            if self.image is not None:
                await interaction.response.send_message(
                    content='http:' + self.image)
            else:
                await interaction.response.send_message(
                    content=self.nsfw_text['nsfw_plugin_data'][2])


async def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    await bot.add_cog(NSFW(bot))
