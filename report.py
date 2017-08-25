# coding=utf-8
"""
Bug Reporting plugin for DecoraterBot.

This is for getting DecoraterBot's new bugtracker.
"""

import discord
from discord.ext import commands
from DecoraterBotUtils.utils import *


class Report:
    """
    Report Commands Extension.
    """
    def __init__(self):
        self.report_text = PluginTextReader(
            file='report.json')

    @commands.command(name='report', pass_context=True, no_pm=True)
    async def report_command(self, ctx):
        await ctx.bot.send_message(
            ctx.message.channel,
            self.report_text['report_plugin_data'][0])

def setup(bot):
    """
    DecoraterBot's Bug Reporting Plugin.
    """
    bot.add_cog(Report())
