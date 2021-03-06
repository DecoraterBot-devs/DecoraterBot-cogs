# coding=utf-8
"""
Webhooks Plugin for DecoraterBot.
"""
import os
import sys

import discord
from discord.ext import commands
from discord_webhooks import *
from DecoraterBotUtils import utils


class WebHooks:
    """
    Webhook Commands Extension.
    """
    def __init__(self, bot):
        self.webhook_class = Webhook(bot)
        self.webhook_text = utils.PluginTextReader(
            file='webhooks.json')

    @commands.command(name='sendtext', pass_context=True, no_pm=True)
    async def webhooktext_command(self, ctx):
        """
        ::sendtext request command for DecoraterBot.
        """
        msgdata = ctx.message.content[len(ctx.prefix + "sendtext"):].strip()
        # if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                await self.webhook_class.request_webhook(
                    '/284510404162355200/F2CFGqlX9UpC_hRpLIbFLzTnXncgqFdaLz'
                    '09fOI92fihzfQT6lT0VB2ZjW4FtEZPcurS',
                    content=msgdata)
        else:
            await ctx.bot.send_message(
                ctx.message.channel,
                self.webhook_text['webhook_plugin_data'][0])

    @commands.command(name='sendimages', pass_context=True, no_pm=True)
    async def webhookimages_command(self, ctx):
        """
        ::sendimages request command for DecoraterBot.
        """
        # if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                file = open(os.path.join(
                    sys.path[0], 'resources', 'images', 'other', 'image.jpg'),
                    'rb')
                data = file.read()
                await self.webhook_class.request_webhook(
                    '/284510404162355200/F2CFGqlX9UpC_hRpLIbFLzTnXncgqFdaLz'
                    '09fOI92fihzfQT6lT0VB2ZjW4FtEZPcurS',
                    file=data)
        else:
            await ctx.bot.send_message(
                ctx.message.channel,
                self.webhook_text['webhook_plugin_data'][0])

    @commands.command(name='sendannouncement', pass_context=True, no_pm=True)
    async def webhookannouncement_command(self, ctx):
        """
        ::sendannouncement request command for DecoraterBot.
        """
        msgdata = ctx.message.content[
                  len(ctx.prefix + "sendannouncement"):].strip()
        # if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
        #     return
        role2 = discord.utils.find(lambda role: role.name == 'Webhook Manager',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            if ctx.message.server.id == '273134655702827008':
                await self.webhook_class.request_webhook(
                    '/294680827579727873/Op_LqGeUQiC2MgeNS-EFhbaNj1ZGH5VGH0'
                    '_5eshfdkSQYPPGo6r0RllOdHGXPrlV0XVW',
                    content=msgdata)
        else:
            await ctx.bot.send_message(
                ctx.message.channel,
                self.webhook_text['webhook_plugin_data'][0])


def setup(bot):
    """
    DecoraterBot's Webhook Plugin.
    """
    new_cog = WebHooks(bot)
    bot.add_cog(new_cog)
