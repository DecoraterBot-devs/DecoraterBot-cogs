# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
import random

from discord.ext import commands
import nsfw_dl
from DecoraterBotUtils.utils import *


class NSFW:
    """
    NSFW Commands Plugin Class.
    """
    def __init__(self):
        self.image = None
        self.nsfw_text = PluginTextReader(
            file='nsfw.json')

    @commands.command(name='rule34', pass_context=True)
    async def rule34_command(self, ctx):
        """
        ::rule34 Search Command for DecoraterBot.
        """
        searchterm = ctx.message.content[len(ctx.prefix + 'rule34 '):].strip()
        if searchterm != '':
            imageerr = None
            try:
                self.image = await nsfw_dl.rule34_search(
                    searchterm, ctx.bot.http.session)
            except nsfw_dl.errors.NoResultsFound:
                self.image = None
                imageerr = self.nsfw_text['nsfw_plugin_data'][0]
            if self.image is -1:
                await ctx.bot.send_message(
                    ctx.message.channel,
                    content=self.nsfw_text['nsfw_plugin_data'][1])
            else:
                if self.image is not None:
                    await ctx.bot.send_message(
                        ctx.message.channel,
                        content='http:' + random.choice(self.image))
                else:
                    if imageerr is not None:
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=imageerr)
                    else:
                        await ctx.bot.send_message(
                            ctx.message.channel,
                            content=self.nsfw_text['nsfw_plugin_data'][2])
        else:
            self.image = await nsfw_dl.rule34_random(ctx.bot.http.session)
            if self.image is not None:
                await ctx.bot.send_message(ctx.message.channel,
                                            content='http:' + self.image)
            else:
                await ctx.bot.send_message(ctx.message.channel,
                                            content=self.nsfw_text[
                                                        'nsfw_plugin_data'
                                                    ][2])


def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    bot.add_cog(NSFW())
