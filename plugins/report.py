# coding=utf-8
"""
Bug Reporting plugin for DecoraterBot.

This is for getting DecoraterBot's new bugtracker.
"""

import discord
from discord.ext import commands


class Report:
    """
    Report Commands Extension.
    """
    def __init__(self, bot):
        self.bot = bot
        self.report_text = self.bot.PluginTextReader(
            file='report.json')

    @commands.command(name='report', pass_context=True, no_pm=True)
    async def report_command(self, ctx):
        await self.bot.send_message(ctx.message.channel,
                                    self.report_text['report_plugin_data'][0])

def setup(bot):
    """
    DecoraterBot's Bug Reporting Plugin.
    """
    new_cog = Report(bot)
    bot.add_cog(new_cog)
