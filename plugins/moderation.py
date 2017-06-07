# coding=utf-8
"""
moderation plugin for DecoraterBot.
"""
import regex

import discord
from discord.ext import commands
from DecoraterBotUtils import utils


# This module's warn, and mute commands do not work for now.
# And the clear command does not fall back to delete_messages
# when purge_from fails to delete messages over 14 days old.
# I would like it if someone would help me fix them and pull
# request the fixtures to this file to make them work.


class Moderation:
    """
    Moderation Commands Extension to the
        default DecoraterBot Moderation commands.
    """
    def __init__(self):
        self.moderation_text = utils.PluginTextReader(
            file='moderation.json')

    @commands.command(name='ban', pass_context=True, no_pm=True)
    async def ban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        reply_data = ""
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                listdata = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, listdata)
                try:
                    await ctx.bot.ban(member2, delete_message_days=7)
                    reply_data = str(
                        self.moderation_text[
                            'ban_command_data'
                        ][0]).format(member2)
                except discord.Forbidden:
                    reply_data = str(
                        self.moderation_text[
                            'ban_command_data'
                        ][1])
                except discord.HTTPException:
                    reply_data = str(
                        self.moderation_text[
                            'ban_command_data'
                        ][2])
                break
            else:
                reply_data = str(
                    self.moderation_text[
                        'ban_command_data'
                    ][3])
        else:
            reply_data = str(
                self.moderation_text[
                    'ban_command_data'
                ][4])
        try:
            await ctx.bot.send_message(
                ctx.message.channel, content=reply_data)
        except discord.Forbidden:
            await ctx.bot.BotPMError.resolve_send_message_error(
                ctx)

    @commands.command(name='softban', pass_context=True, no_pm=True)
    async def softban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        reply_data = ""
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, memberlist)
                try:
                    await ctx.bot.ban(member2, delete_message_days=7)
                    await ctx.bot.unban(member2.server, member2)
                    reply_data = str(
                        self.moderation_text['softban_command_data'][
                            0]).format(member2)
                except discord.Forbidden:
                    reply_data = str(
                        self.moderation_text['softban_command_data'][1])
                except discord.HTTPException:
                    reply_data = str(
                        self.moderation_text['softban_command_data'][2])
                break
            else:
                reply_data = str(
                    self.moderation_text[
                        'softban_command_data'
                    ][3])
        else:
            reply_data = str(
                self.moderation_text[
                    'softban_command_data'
                ][4])
        try:
            await ctx.bot.send_message(
                ctx.message.channel, content=reply_data)
        except discord.Forbidden:
            await ctx.bot.BotPMError.resolve_send_message_error(
                ctx)

    @commands.command(name='kick', pass_context=True, no_pm=True)
    async def kick_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        reply_data = ""
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            for disuser in ctx.message.mentions:
                memberlist = ctx.message.channel.server.members
                member2 = discord.utils.find(
                    lambda member: member.name == disuser.name, memberlist)
                try:
                    await ctx.bot.kick(member2)
                    reply_data = str(
                        self.moderation_text['kick_command_data'][
                            0]).format(member2)
                except discord.Forbidden:
                    reply_data = str(
                        self.moderation_text[
                            'kick_command_data'
                        ][1])
                except discord.HTTPException:
                    reply_data = str(
                        self.moderation_text[
                            'kick_command_data'
                        ][2])
                break
            else:
                reply_data = str(
                    self.moderation_text[
                        'kick_command_data'
                    ][3])
        else:
            reply_data = str(
                self.moderation_text[
                    'kick_command_data'
                ][4])
        try:
            await ctx.bot.send_message(
                ctx.message.channel, content=reply_data)
        except discord.Forbidden:
            await ctx.bot.BotPMError.resolve_send_message_error(
                ctx)

    @commands.command(name='prune', pass_context=True, no_pm=True)
    async def prune_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        reply_data = ""
        if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in ctx.bot.banlist['Users']:
            return
        else:
            role2 = discord.utils.find(
                lambda role: role.name == 'Bot Commander',
                ctx.message.channel.server.roles)
            # if ctx.message.author.id == owner_id:
            #     opt = ctx.message.content[len(_bot_prefix + "prune "):].strip()
            #     num = 1
            #     if opt:
            #         try:
            #             num = int(opt)
            #         except:
            #             return
            #     reply_data = await self.prune_command_iterater_helper(ctx, num)
            # else:
            if role2 in ctx.message.author.roles:
                opt = ctx.message.content[
                      len(ctx.prefix + "prune "):].strip()
                num = 1
                if opt:
                    try:
                        num = int(opt)
                    except Exception as e:
                        str(e)
                        return
                reply_data = await self.prune_command_iterater_helper(ctx, num)
            else:
                reply_data = str(
                    self.moderation_text[
                        'prune_command_data'
                    ][1])
            if reply_data is not None:
                try:
                    await ctx.bot.send_message(
                        ctx.message.channel, content=reply_data)
                except discord.Forbidden:
                    await ctx.bot.BotPMError.resolve_send_message_error(
                        ctx)

    @commands.command(name='clear', pass_context=True, no_pm=True)
    async def clear_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.author.id in ctx.bot.banlist['Users']:
            return
        else:
            await self.clear_command_iterater_helper(ctx)

    @commands.command(name='warn', pass_context=True)
    async def warn_command(self, ctx):
        """
        ::warn Command for DecoraterBot.
        """
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            match = regex.match('warn[ ]+(<@(.+?)>[ ])+(.+)',
                                ctx.message.content[len(ctx.prefix):].strip())
            if match:
                warning = match.captures(3)[0]
                targets = match.captures(2)
                for target in targets:
                    await ctx.bot.send_message(target, content=warning)

    @commands.command(name='mute', pass_context=True)
    async def mute_command(self, ctx):
        """
        ::mute Search Command for DecoraterBot.
        """
        role2 = discord.utils.find(lambda role: role.name == 'Bot Commander',
                                   ctx.message.channel.server.roles)
        if role2 in ctx.message.author.roles:
            match = regex.match(ctx.prefix + 'mute[ ]+(<@(.+?)>[ ])+(.+)',
                                ctx.message.content)
            if match:
                mute_time = match.captures(3)[0]
                # targets = match.captures(2)
                if mute_time is not None:
                    # s = seconds
                    # m = minutes
                    # h = hours
                    # d = days
                    # w = weeks
                    # M = months
                    # y = years
                    pattern = '(\d+)(s|m|h|d|w|M|y)'
                    searchres = regex.match(pattern, mute_time)
                    if searchres is not None:
                        # TODO: Finish this command.
                        return

    # Helpers.

    async def prune_command_iterater_helper(self, ctx, num):
        """
        Prunes Messages.
        :param self:
        :param ctx: Message Context.
        :param num:
        :return: message string on Error, nothing otherwise.
        """
        try:
            await ctx.bot.purge_from(ctx.message.channel, limit=num + 1)
            return None
        except discord.HTTPException as e:
            # messages = []
            # async for message in ctx.bot.logs_from(ctx.message.channel,
            #                                         limit=num + 1):
            #     messages.append(message)
            # for message in messages:
            #     try:
            #         await ctx.bot.delete_message(message)
            #     except discord.HTTPException:
            if str(e).find("status code: 400") != -1:
                return str(
                    self.moderation_text[
                        'prune_command_data'
                    ][2]))
            else:
                return str(
                    self.moderation_text[
                        'prune_command_data'
                    ][0]))

    async def clear_command_iterater_helper(self, ctx):
        """
        Clears the bot's messages.
        :param ctx: Message Context.
        :return: Nothing.
        """
        type(self)
        try:
            await ctx.bot.purge_from(
                ctx.message.channel, limit=100,
                check=lambda e: e.author == (
                    ctx.message.server.me))
        except discord.HTTPException:
            return


def setup(bot):
    """
    DecoraterBot's Moderation Plugin.
    """
    bot.add_cog(Moderation())
