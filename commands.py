# coding=utf-8
"""
Normal commands plugin for DecoraterBot.
"""
import json
import platform
import random
import subprocess
import sys
import traceback
import re
import ctypes
import os

import discord
from discord.ext import commands
from DecoraterBotUtils import utils
try:
    import TinyURL
    disabletinyurl = False
except ImportError:
    disabletinyurl = True
    TinyURL = None


class Commands:
    """
    Normal commands cog for DecoraterBot.
    """
    def __init__(self, bot):
        self.commands_text = utils.PluginTextReader(
            file='commands.json')
        self.version = str(bot.consoletext['WindowVersion'][0])
        self.rev = str(bot.consoletext['Revision'][0])
        self.sourcelink = str(self.commands_text['source_command_data'][0])
        self.botcommands = str(
            self.commands_text['commands_command_data'][
                0])
        self.changelog = str(self.commands_text['changelog_data'][0])
        self.info = "``" + str(bot.consoletext['WindowName'][
            0]) + self.version + self.rev + "``"
        self.logger = utils.CogLogger(bot)

    @commands.command(name='attack', pass_context=True, no_pm=True)
    async def attack_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Message Context.
        :return: Nothing.
        """
        if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in ctx.bot.banlist['Users']:
            return
        else:
            for user in ctx.message.mentions:
                await ctx.bot.send_message(user, content=str(
                    self.commands_text['attack_command_data'][0]))
                break
            else:
                await ctx.bot.send_message(ctx.message.author,
                                            content=str(
                                                self.commands_text[
                                                    'attack_command_data'][1]))

    @commands.command(name='coin', pass_context=True, no_pm=True)
    async def coin_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            msg = random.randint(0, 1)
            if msg == 0:
                heads_coin = os.path.join(
                    sys.path[0], 'resources', 'images', 'coins', 'Heads.png')
                try:
                    await ctx.bot.send_file(ctx.message.channel, heads_coin)
                except discord.Forbidden:
                    try:
                        message_data = str(
                            self.commands_text['coin_command_data'][0])
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx.bot, ctx)
            if msg == 1:
                tails_coin = os.path.join(
                    sys.path[0], 'resources', 'images', 'coins', 'Tails.png')
                try:
                    await ctx.bot.send_file(ctx.message.channel, tails_coin)
                except discord.Forbidden:
                    try:
                        message_data = str(
                            self.commands_text['coin_command_data'][0])
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=message_data)
                    except discord.Forbidden:
                        await ctx.bot.BotPMError.resolve_send_message_error(
                            ctx.bot, ctx)

    # @commands.group(name='color', pass_context=True, no_pm=True)
    # async def color_command(self, ctx):
    #     """
    #     Bot Commands.
    #     :param ctx: Messages.
    #     :return: Nothing.
    #     """
    #     if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
    #         return
    #     if ctx.message.author.id in ctx.bot.banlist['Users']:
    #         return
    #     if ctx.invoked_subcommand is None:
    #         return

    # @color_command.command(name='pink', pass_context=True, no_pm=True)
    # async def pink_subcommand(self, ctx):
    #     """
    #     Bot Commands.
    #     :param ctx: Messages.
    #     :return: Nothing.
    #     """
    #     if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
    #         return
    #     desrole = ctx.message.content[
    #               len(
    #                   ctx.prefix + "color " +
    #                   ctx.prefix + "pink "):].strip()
    #     role2 = discord.utils.find(lambda role: role.name == desrole,
    #                                ctx.message.channel.server.roles)
    #     try:
    #         await ctx.bot.edit_role(ctx.message.channel.server, role2,
    #                                  color=discord.Colour(int('ff3054', 16)))
    #     except discord.Forbidden:
    #         try:
    #             message_data = str(
    #                 self.commands_text['color_command_data'][0])
    #             await ctx.bot.send_message(ctx.message.channel,
    #                                         content=message_data)
    #         except discord.Forbidden:
    #             await ctx.bot.BotPMError.resolve_send_message_error(ctx.bot,
    #                                                                  ctx)
    #     except discord.HTTPException:
    #         return
    #     except AttributeError:
    #         return

    # @color_command.command(name='brown', pass_context=True, no_pm=True)
    # async def brown_subcommand(self, ctx):
    #     """
    #     Bot Commands.
    #     :param ctx: Messages.
    #     :return: Nothing.
    #     """
    #     if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
    #         return
    #     desrole = ctx.message.content[
    #               len(
    #                   ctx.prefix + "color " +
    #                   ctx.prefix + "brown "):].strip()
    #     role2 = discord.utils.find(lambda role: role.name == desrole,
    #                                ctx.message.channel.server.roles)
    #     try:
    #         await ctx.bot.edit_role(ctx.message.channel.server, role2,
    #                                  color=discord.Colour(int('652d2d', 16)))
    #     except discord.Forbidden:
    #         try:
    #             message_data = str(
    #                 self.commands_text['color_command_data'][0])
    #             await ctx.bot.send_message(ctx.message.channel,
    #                                         content=message_data)
    #         except discord.Forbidden:
    #             await ctx.bot.BotPMError.resolve_send_message_error(ctx.bot,
    #                                                                  ctx)
    #     except discord.HTTPException:
    #         pass
    #     except AttributeError:
    #         pass

    @commands.command(name='eval', pass_context=True, no_pm=True)
    async def eval_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in ctx.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == ctx.bot.BotConfig.discord_user_id:
            debugcode = ctx.message.content[
                        len(ctx.prefix + "eval "):].strip()
            if debugcode.rfind(
                    'await ctx.bot.send_message(ctx.message.channel, content='
            ) is not -1:
                debugcode = debugcode[len(
                    "await ctx.bot.send_message(ctx.message.channel, content="
                ):].strip()
                debugcode = debugcode.strip(")")
                if debugcode.find("'") is not -1:
                    debugcode = debugcode.strip("'")
                elif debugcode.find('"') is not -1:
                    debugcode = debugcode.strip('"')
                if debugcode.find('ctx.message.author.mention') is not -1:
                    debugcode = debugcode.replace(
                        'ctx.message.author.mention + "',
                        ctx.message.author.mention)
                    await ctx.bot.send_message(ctx.message.channel,
                                                content=debugcode)
            else:
                botowner = discord.utils.find(
                    (lambda member: member.id ==
                        ctx.bot.BotConfig.discord_user_id),
                    ctx.message.channel.server.members)
                try:
                    try:
                        debugcode = eval(debugcode)
                    except SystemExit:
                        pass
                    debugcode = "```py\n" + str(debugcode) + "\n```"
                    try:
                        await ctx.bot.send_message(ctx.message.channel,
                                                    content=debugcode)
                    except discord.Forbidden:
                        msgdata = str(
                            self.commands_text['eval_command_data'][0])
                        message_data = msgdata.format(
                            ctx.message.channel.server.name,
                            ctx.message.channel.name)
                        await self.bot.send_message(botowner,
                                                    content=message_data)
                        await self.bot.send_message(botowner,
                                                    content=debugcode)
                    except discord.HTTPException:
                        if len(debugcode) > 2000:
                            result_info = str(
                                self.commands_text['eval_command_data'][1])
                            await self.bot.send_message(ctx.message.channel,
                                                        content=result_info)
                except Exception as e:
                    str(e)
                    debugcode = traceback.format_exc()
                    debugcode = str(debugcode)
                    try:
                        await self.bot.send_message(ctx.message.channel,
                                                    content="```py\n" +
                                                            debugcode +
                                                            "\n```")
                    except discord.Forbidden:
                        msgdata = str(
                            self.commands_text['eval_command_data'][0])
                        message_data = msgdata.format(
                            ctx.message.channel.server.name,
                            ctx.message.channel.name)
                        await self.bot.send_message(botowner,
                                                    content=message_data)
                        await self.bot.send_message(botowner,
                                                    content="```py\n" +
                                                            debugcode +
                                                            "\n```")
        else:
            try:
                result_info = str(self.commands_text['eval_command_data'][2])
                await self.bot.send_message(ctx.message.channel,
                                            content=result_info)
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='debug', pass_context=True, no_pm=True)
    async def debug_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            debugcode_new = "# coding=utf-8\n" + ctx.message.content[len(
                ctx.prefix + "debug "):].strip()
            botowner = discord.utils.find(
                lambda member: member.id == self.bot.BotConfig.discord_user_id,
                ctx.message.channel.server.members)
            try:
                evalcodefile = os.path.join(
                    sys.path[0], 'resources', 'exec_files', 'exec_temp.py')
                eval_temp_code = open(evalcodefile, 'w+', encoding='utf-8')
                debugcode_new += '\n'
                eval_temp_code.write(debugcode_new)
                eval_temp_code.close()
                execoutputfile = os.path.join(
                    sys.path[0], 'resources', 'exec_files',
                    'exec_output_temp.txt')
                eval_temp_result_output = open(execoutputfile, 'w',
                                               encoding='utf-8')
                out = eval_temp_result_output
                p = subprocess.Popen(os.path.join(
                    sys.path[4], 'python') + ' ' + evalcodefile,
                    stdout=out,
                    stderr=out, shell=True)
                p.wait()
                eval_temp_result_output.close()
                eval_temp_result_read = open(execoutputfile, encoding='utf-8')
                eval_result = eval_temp_result_read.read()
                if eval_result is not '':
                    debugcode = eval_result
                else:
                    debugcode = 'None'
                eval_temp_result_read.close()
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content="```py\n" +
                                                        debugcode + "\n```")
                except discord.Forbidden:
                    msgdata = str(self.commands_text['eval_command_data'][0])
                    message_data = msgdata.format(
                        ctx.message.channel.server.name,
                        ctx.message.channel.name)
                    await self.bot.send_message(botowner, content=message_data)
                    await self.bot.send_message(botowner,
                                                content="```py\n" +
                                                        debugcode + "\n```")
                except discord.HTTPException:
                    if len(debugcode) > 2000:
                        result_info = str(
                            self.commands_text['eval_command_data'][1])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=result_info)
            except Exception as e:
                str(e)
                debugcode = traceback.format_exc()
                debugcode = str(debugcode)
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content="```py\n" +
                                                        debugcode + "\n```")
                except discord.Forbidden:
                    msgdata = str(self.commands_text['eval_command_data'][0])
                    message_data = msgdata.format(
                        ctx.message.channel.server.name,
                        ctx.message.channel.name)
                    await self.bot.send_message(botowner, content=message_data)
                    await self.bot.send_message(botowner,
                                                content="```py\n" +
                                                        debugcode + "\n```")
        else:
            try:
                result_info = str(
                    self.commands_text['debug_command_data'][0])
                await self.bot.send_message(ctx.message.channel,
                                            content=result_info)
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='game', pass_context=True, no_pm=False)
    async def game_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        elif ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        else:
            patterns = [
                '(https?:\/\/)?discord\.gg\/[a-zA-Z0-9\-]{2,16}',
                '(https?:\/\/)?discordapp\.com\/invite\/[a-zA-Z0-9\-]{2,16}'
            ]
            for pattern in patterns:
                regex = re.compile(pattern)
                searchres = regex.search(ctx.message.content)
            if searchres is not None:
                await self.bot.send_message(
                    ctx.message.channel, content=str(
                        self.commands_text[
                            'game_command_data'
                        ][3]))
            else:
                desgame, desgametype, stream_url, desgamesize = (
                    self.game_command_helper(ctx))
                if desgamesize < 1:
                    await self.bot.send_message(
                        ctx.message.channel, content=str(
                        self.commands_text[
                            'game_command_data'
                        ][3]))
                elif desgametype is not None:
                    if self.bot.BotConfig.log_games:
                        self.logger.gamelog(ctx, desgame)
                    await self.bot.change_presence(
                        game=discord.Game(name=desgame, type=desgametype,
                                          url=stream_url), status='online')
                    try:
                        await self.bot.send_message(
                            ctx.message.channel, content=str(
                                self.commands_text[
                                    'game_command_data'
                                ][1]).format(
                                desgame))
                    except discord.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)
                elif desgametype is None:
                    if self.bot.BotConfig.log_games:
                        self.logger.gamelog(ctx, desgame)
                    await self.bot.change_presence(
                        game=discord.Game(name=desgame), status='idle')
                    try:
                        await self.bot.send_message(
                            ctx.message.channel, content=str(
                                self.commands_text[
                                    'game_command_data'
                                ][0]).format(desgame))
                    except discord.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)

    @commands.command(name='remgame', pass_context=True, no_pm=False)
    async def remgame_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        elif ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        else:
            game_name = str(
                self.bot.consoletext['On_Ready_Game'][0]).format(
                self.bot.command_prefix)
            stream_url = "https://twitch.tv/decoraterbot"
            await self.bot.change_presence(
                game=discord.Game(name=game_name, type=1, url=stream_url))
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.commands_text[
                                                    'remgame_command_data'][0])
                                            )
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='join', pass_context=True, no_pm=False)
    async def join_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if self.bot.BotConfig.is_official_bot:
                await self.bot.send_message(ctx.message.channel,
                                            content=str(
                                                self.commands_text[
                                                    'join_command_data'][3]))
            else:
                code = ctx.message.content[
                       len(ctx.prefix + "join "):].strip()
                if code == '':
                    url = None
                else:
                    url = code
                if url is not None:
                    try:
                        await self.bot.accept_invite(url)
                        msg_data = str(
                            self.commands_text['join_command_data'][0])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msg_data)
                    except discord.NotFound:
                        msg_data = str(
                            self.commands_text['join_command_data'][1])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msg_data)
                else:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'join_command_data'][
                                                        2]))

    @commands.command(name='kill', pass_context=True, no_pm=False)
    async def kill_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            data = ctx.message.content[
                   len(ctx.prefix + "kill "):].strip()
            if ctx.message.channel.is_private:
                msg = random.randint(0, len(
                    self.commands_text['kill_command_data']) - 1)
                message_data = str(
                    self.commands_text['kill_command_data'][msg]).format(
                    ctx.message.author)
                await self.bot.send_message(ctx.message.channel,
                                            content=message_data)
            else:
                # if data.rfind(self.bot.user.name) != -1:
                #     try:
                #         msg_data = str(
                #             self.commands_text['kill_command_error'][0])
                #         await self.bot.send_message(ctx.message.channel,
                #                                     content=msg_data)
                #     except discord.Forbidden:
                #         await self.bot.BotPMError.resolve_send_message_error(
                #             self.bot, ctx)
                # else:
                msg = random.randint(0, len(
                    self.commands_text['kill_command_data']) - 1)
                try:
                    message_data = str(
                        self.commands_text['kill_command_data'][
                            msg]).format(
                        ctx.message.author)
                    await self.bot.send_message(
                        ctx.message.channel, content=message_data)
                except discord.Forbidden:
                    await self.bot.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='ignorechannel', pass_context=True, no_pm=False)
    async def ignorechannel_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id not in self.bot.ignoreslist["channels"]:
            try:
                self.bot.ignoreslist["channels"].append(ctx.message.channel.id)
                json.dump(self.bot.ignoreslist, open(os.path.join(
                    sys.path[0], 'resources', 'ConfigData','IgnoreList.json'), 
                    "w"))
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'Ignore_Channel_Data'][
                                                        0]))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
            except Exception as e:
                str(e)
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'Ignore_Channel_Data'][
                                                        1]))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='unignorechannel', pass_context=True, no_pm=False)
    async def unignorechannel_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            try:
                ignored = self.bot.ignoreslist["channels"]
                ignored.remove(ctx.message.channel.id)
                json.dump(self.bot.ignoreslist, open(os.path.join(
                    sys.path[0], 'resources', 'ConfigData',
                    'IgnoreList.json'), "w"))
                msg_info = str(
                    self.commands_text['Unignore_Channel_Data'][0])
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=msg_info)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
            except Exception as e:
                str(e)
                msg_info = str(
                    self.commands_text['Unignore_Channel_Data'][1])
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=msg_info)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='commands', aliases=['help'], pass_context=True, no_pm=False)
    async def commands_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                await self.bot.send_message(
                    ctx.message.channel,
                    content=self.botcommands)
            else:
                try:
                    if self.bot.BotConfig.pm_commands_list:
                        await self.bot.send_message(
                            ctx.message.author,
                            content=self.botcommands)
                        msgdata = str(
                            self.commands_text['commands_command_data'][
                                1])
                        message_data = msgdata.format(
                            ctx.message.author.mention)
                        try:
                            await self.bot.send_message(
                                ctx.message.channel, content=message_data)
                        except discord.Forbidden:
                            await self.bot.resolve_send_message_error(
                                self.bot, ctx)
                    else:
                        await self.bot.send_message(
                            ctx.message.channel,
                            content=self.botcommands)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='changelog', pass_context=True, no_pm=False)
    async def changelog_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            try:
                await self.bot.send_message(ctx.message.channel,
                                            content=self.changelog.format(
                                                self.version +
                                                self.rev))
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='update', pass_context=True, no_pm=True)
    async def update_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                return
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'update_command_data'][
                                                        0]).format(
                                                    self.info))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='Libs', pass_context=True, no_pm=False)
    async def libs_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            libs = str(self.commands_text['Libs_command_data'][0])
            try:
                await self.bot.send_message(ctx.message.channel, content=libs)
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='source', pass_context=True, no_pm=False)
    async def source_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            try:
                msgdata = self.sourcelink.format(ctx.message.author)
                message_data = msgdata
                await self.bot.send_message(ctx.message.channel,
                                            content=message_data)
            except discord.Forbidden:
                await self.bot.BotPMError.resolve_send_message_error(self.bot,
                                                                     ctx)

    @commands.command(name='type', pass_context=True, no_pm=False)
    async def type_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            await self.bot.send_typing(ctx.message.channel)

    @commands.command(name='pyversion', pass_context=True, no_pm=True)
    async def pyversion_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            if ctx.message.channel.is_private:
                return
            else:
                python_platform = None
                bits = ctypes.sizeof(ctypes.c_voidp)
                if bits == 8:
                    python_platform = "64-Bit"
                elif bits == 4:
                    python_platform = "32-Bit"
                vers = "```py\nPython v{0} {1}```".format(
                    platform.python_version(), python_platform)
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=vers)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    @commands.command(name='AgarScrub', pass_context=True, no_pm=True)
    async def agarscrub_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        try:
            reply = 'https://imgflip.com/i/12yq2n'
            await self.bot.send_message(ctx.message.channel, content=reply)
        except discord.Forbidden:
            await self.bot.BotPMError.resolve_send_message_error(self.bot, ctx)

    @commands.command(name='stats', pass_context=True, no_pm=True)
    async def stats_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        server_count = str(len(self.bot.servers))
        member_count = str(
            len(set([member for member in self.bot.get_all_members()])))
        textchannels_count = str(len(set(
            [channel for channel in self.bot.get_all_channels() if
             channel.type == discord.ChannelType.text])))
        formatted_data = str(
            self.commands_text['stats_command_data'][0]
        ).format(server_count, member_count, textchannels_count)
        await self.bot.send_message(ctx.message.channel,
                                    content=formatted_data)

    @commands.command(name='rs', pass_context=True, no_pm=False)
    async def rs_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename1 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'RS.jpg')
        file_object = open(filename1, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='as', pass_context=True, no_pm=False)
    async def as_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename2 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'AS.jpg')
        file_object = open(filename2, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='ai', pass_context=True, no_pm=False)
    async def ai_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename3 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'AI.jpg')
        file_object = open(filename3, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='lk', pass_context=True, no_pm=False)
    async def lk_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename4 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'LK.jpg')
        file_object = open(filename4, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='vp', pass_context=True, no_pm=False)
    async def vp_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename5 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'VP.jpg')
        file_object = open(filename5, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='ws', pass_context=True, no_pm=False)
    async def ws_command(self, ctx):
        """
        Bot Commands.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id != self.bot.BotConfig.discord_user_id:
            return
        filename6 = os.path.join(
            sys.path[0], 'resources', 'images', 'elsword', 'WS.jpg')
        file_object = open(filename6, 'rb')
        file_data = None
        if file_object is not None:
            file_data = file_object.read()
            file_object.close()
        await self.bot.edit_profile(avatar=file_data)

    @commands.command(name='meme', pass_context=True, no_pm=False)
    async def meme_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        desdata = ctx.message.content[
                  len(ctx.prefix + 'meme'):].strip()
        meme_error = False
        desdata = str(desdata)
        toptext = None
        bottext = None
        pic = None
        msg_mention_list_len = len(ctx.message.mentions) - 1
        if msg_mention_list_len == -1:
            msg_mention_list_len = 0
        if msg_mention_list_len > 0:
            if desdata.startswith(
                    ctx.message.mentions[msg_mention_list_len].mention):
                desdata = desdata.replace(" | ", "\n").replace('-',
                                                               '--').replace(
                    ' ', '-')
                desdata = desdata.splitlines()
                try:
                    pic = ctx.message.mentions[msg_mention_list_len].avatar_url
                except IndexError:
                    meme_error = True
                    msgdata = str(self.commands_text['meme_command_data'][0])
                    await self.bot.send_message(ctx.message.channel,
                                                content=msgdata)
                if not meme_error:
                    try:
                        toptext = desdata[1].replace('_', '__'
                                                     ).replace(
                            '?', '~q').replace(
                            '%', '~p').replace('#', '~h').replace('/', '~s')
                        for x in ctx.message.mentions:
                            toptext = toptext.replace(x.mention, x.name)
                        toptext = toptext.replace('<', '').replace('>',
                                                                   '').replace(
                            '@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(
                            self.commands_text['meme_command_data'][1])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msgdata)
                if not meme_error:
                    try:
                        bottext = desdata[2].replace('_', '__').replace(
                            '?', '~q').replace(
                            '%', '~p').replace(
                            '#', '~h').replace(
                            '/', '~s')
                        for x in ctx.message.mentions:
                            bottext = bottext.replace(x.mention, x.name)
                        bottext = bottext.replace('<', '').replace('>',
                                                                   '').replace(
                            '@', '')
                    except IndexError:
                        meme_error = True
                        msgdata = str(
                            self.commands_text['meme_command_data'][2])
                        await self.bot.send_message(ctx.message.channel,
                                                    content=msgdata)
                if not meme_error:
                    rep = "http://memegen.link/custom/{0}/{1}.jpg?alt=" \
                          "{2}".format(toptext, bottext, pic)
                    await self.bot.send_message(ctx.message.channel,
                                                content=rep)
        else:
            desdata = desdata.replace(" | ", "\n").replace('-', '--').replace(
                ' ', '-')
            desdata = desdata.splitlines()
            try:
                pic = str(desdata[0])
            except IndexError:
                meme_error = True
                msgdata = str(self.commands_text['meme_command_data'][0])
                await self.bot.send_message(ctx.message.channel,
                                            content=msgdata)
            if not meme_error:
                try:
                    toptext = desdata[1].replace(
                        '_', '__').replace(
                        '?', '~q').replace(
                        '%', '~p').replace('#', '~h').replace('/', '~s')
                    for x in ctx.message.mentions:
                        toptext = toptext.replace(x.mention, x.name)
                    toptext = toptext.replace('<', '').replace('>',
                                                               '').replace('@',
                                                                           '')
                except IndexError:
                    meme_error = True
                    msgdata = str(self.commands_text['meme_command_data'][1])
                    await self.bot.send_message(ctx.message.channel,
                                                content=msgdata)
            if not meme_error:
                try:
                    bottext = desdata[2].replace(
                        '_', '__').replace(
                        '?', '~q').replace(
                        '%', '~p').replace(
                        '#', '~h').replace(
                        '/', '~s')
                    for x in ctx.message.mentions:
                        bottext = bottext.replace(x.mention, x.name)
                    bottext = bottext.replace('<', '').replace('>',
                                                               '').replace('@',
                                                                           '')
                except IndexError:
                    meme_error = True
                    msgdata = str(self.commands_text['meme_command_data'][2])
                    await self.bot.send_message(ctx.message.channel,
                                                content=msgdata)
            if not meme_error:
                rep = "http://memegen.link/{0}/{1}/{2}.jpg".format(pic,
                                                                   toptext,
                                                                   bottext)
                await self.bot.send_message(ctx.message.channel, content=rep)

    @commands.command(name='discrim', pass_context=True, no_pm=True)
    async def discrim_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        for member in self.bot.get_all_members():
            if member.discriminator == ctx.message.author.discriminator:
                if member != ctx.message.author:
                    self.bot.member_list.append(member.name)
        if len(self.bot.member_list) > 0:
            await self.bot.send_message(ctx.message.channel,
                                        content=(
                                            "Found {0} members "
                                            "with the same discrimin"
                                            "ator of {1}: ```{2}```."
                                        ).format(
                                            len(self.bot.member_list),
                                            ctx.message.author.discriminator,
                                            self.bot.member_list))
            self.bot.member_list.clear()
        else:
            await self.bot.send_message(ctx.message.channel,
                                        content="Sorry, no members sh"
                                                "are your discriminator.")

    @commands.command(name='say', pass_context=True, no_pm=False)
    async def say_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            say = ctx.message.content[
                  len(ctx.prefix + "say "):].strip()
            if say.rfind(ctx.prefix) != -1:
                message_data = str(
                    self.commands_text['say_command_data'][0]).format(
                    ctx.message.author)
                await self.bot.send_message(ctx.message.channel,
                                            content=message_data)
            elif say.rfind("@") != -1:
                message_data = str(
                    self.commands_text['say_command_data'][1]).format(
                    ctx.message.author)
                await self.bot.send_message(ctx.message.channel,
                                            content=message_data)
            else:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=say)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
                except discord.HTTPException:
                    return

    @commands.command(name='botban', pass_context=True, no_pm=True)
    async def botban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            if len(ctx.message.mentions) < 1:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'bot_ban_command_data'
                                                    ][2]))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
            else:
                if ctx.message.mentions[0].id not in self.bot.banlist['Users']:
                    try:
                        self.bot.banlist['Users'].append(
                            ctx.message.mentions[0].id)
                        json.dump(
                            self.bot.banlist,
                            open(os.path.join(
                                sys.path[0], 'resources',
                                'ConfigData', 'BotBanned.json'),
                                "w"))
                        try:
                            message_data = str(
                                self.commands_text['bot_ban_command_data'][
                                    0]).format(
                                ctx.message.mentions[0])
                            await self.bot.send_message(ctx.message.channel,
                                                        content=message_data)
                        except discord.Forbidden:
                            await self.bot.resolve_send_message_error(
                                self.bot, ctx)
                        except Exception as e:
                            str(e)
                            try:
                                messagedata = str(
                                    self.commands_text[
                                        'bot_ban_command_data'][1]).format(
                                    ctx.message.mentions[0])
                                message_data = messagedata + str(
                                    self.commands_text[
                                        'bot_ban_command_data'][2])
                                await self.bot.send_message(
                                    ctx.message.channel, content=message_data)
                            except discord.Forbidden:
                                await self.bot.resolve_send_message_error(
                                    self.bot, ctx)
                    except discord.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error(
                            self.bot, ctx)

    @commands.command(name='botunban', pass_context=True, no_pm=True)
    async def botunban_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id == self.bot.BotConfig.discord_user_id:
            if len(ctx.message.mentions) < 1:
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=str(
                                                    self.commands_text[
                                                        'bot_unban_'
                                                        'command_data'][2]))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
            else:
                if ctx.message.mentions[0].id in self.bot.banlist['Users']:
                    try:
                        tobotunban = self.bot.banlist['Users']
                        tobotunban.remove(ctx.message.mentions[0].id)
                        json.dump(
                            self.bot.banlist,
                            open(os.path.join(
                                sys.path[0], 'resources',
                                'ConfigData', 'BotBanned.json'),
                                "w"))
                        try:
                            message_data = str(
                                self.commands_text['bot_unban_command_data'][
                                    0]).format(
                                ctx.message.mentions[0])
                            await self.bot.send_message(ctx.message.channel,
                                                        content=message_data)
                        except discord.Forbidden:
                            await self.bot.resolve_send_message_error(
                                self.bot, ctx)
                    except Exception as e:
                        str(e)
                        try:
                            messagedata = str(
                                self.commands_text['bot_unban_command_data'][
                                    1]).format(
                                ctx.message.mentions[0])
                            message_data = messagedata + str(
                                self.commands_text['bot_unban_command_data'][
                                    2])
                            await self.bot.send_message(ctx.message.channel,
                                                        content=message_data)
                        except discord.Forbidden:
                            await self.bot.resolve_send_message_error(
                                self.bot, ctx)

    @commands.command(name='listservers', pass_context=True, no_pm=True)
    async def listservers_command(self, ctx):
        """
        shows the list of servers both the bot and the message autor is in.
        """
        serverlist = "```py\n"
        serverlist += str([
            member.server.name for member in
            self.bot.get_all_members() if
            member.id == ctx.message.author.id])
        serverlist += "\n```"
        try:
            await self.bot.send_message(
                ctx.message.channel,
                content=serverlist)
        except discord.Forbidden:
            await self.bot.BotPMError.resolve_send_message_error(
                self.bot, ctx)

    @commands.command(name='userinfo', pass_context=True, no_pm=True)
    async def userinfo_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        if ctx.message.author.id in self.bot.banlist['Users']:
            return
        else:
            for disuser in ctx.message.mentions:
                userid = disuser.id
                seenin = len(
                    [member.server.name for member in
                     self.bot.get_all_members() if
                     member.id == userid])
                seenin = str(seenin)
                if str(disuser.game) != 'None':
                    desuser = disuser
                    msgdata_1 = str(
                        self.commands_text['userinfo_command_data'][
                            0]).format(desuser, seenin,
                                       desuser.joined_at.ctime(),
                                       desuser.created_at.ctime())
                    message_data = msgdata_1
                    data = message_data
                else:
                    desuser = disuser
                    msgdata_1 = str(
                        self.commands_text['userinfo_command_data'][
                            0]).format(desuser, seenin,
                                       desuser.joined_at.ctime(),
                                       desuser.created_at.ctime())
                    message_data = msgdata_1.replace("Playing ", "")
                    data = message_data
                try:
                    embed = discord.Embed(description=data)
                    embed.colour = 0xff3d00
                    embed.set_image(url=desuser.avatar_url)
                    await self.bot.send_message(ctx.message.channel,
                                                embed=embed)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)
                break
            else:
                seenin = len(
                    [member.server.name for member in
                     self.bot.get_all_members()
                     if member.id == ctx.message.author.id])
                seenin = str(seenin)
                if str(ctx.message.author.game) != 'None':
                    msgdata_1 = str(
                        self.commands_text['userinfo_command_data'][
                            0]).format(
                        ctx.message.author, seenin,
                        ctx.message.author.joined_at.ctime(),
                        ctx.message.author.created_at.ctime())
                    message_data = msgdata_1
                    data = message_data
                else:
                    msgdata_1 = str(
                        self.commands_text['userinfo_command_data'][
                            0]).format(
                        ctx.message.author, seenin,
                        ctx.message.author.joined_at.ctime(),
                        ctx.message.author.created_at.ctime())
                    message_data = msgdata_1.replace("Playing ", "")
                    data = message_data
                try:
                    embed = discord.Embed(description=data)
                    embed.colour = 0xff3d00
                    embed.set_image(url=ctx.message.author.avatar_url)
                    await self.bot.send_message(ctx.message.channel,
                                                embed=embed)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        self.bot, ctx)

    # This command has been optimized for TinyURL3 0.1.7

    @commands.command(name='tinyurl', pass_context=True, no_pm=False)
    async def tinyurl_command(self, ctx):
        """
        Bot Commands.
        :param ctx: Messages.
        :return: Nothing.
        """
        if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
            return
        helper = utils.TinyURLContainer(TinyURL)
        if disabletinyurl:
            return
        else:
            url = ctx.message.content[
                  len(ctx.prefix + "tinyurl "):].strip()
            if '<' and '>' in url:
                url = url.strip('<')
                url = url.strip('>')
            try:
                helper.create_one(url)
                helper.tinyurlerror = False
            except TinyURL.errors.URLError:
                helper.tinyurlerror = True
                try:
                    await self.bot.send_message(
                        ctx.message.channel,
                        content=str(
                            self.commands_text[
                                'tinyurl_command_data'
                            ][2]))
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        ctx)
            except TinyURL.errors.InvalidURL:
                helper.tinyurlerror = True
                try:
                    result = str(
                        self.commands_text['tinyurl_command_data'][1])
                    await self.bot.send_message(ctx.message.channel,
                                                content=result)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        ctx)
            if not helper.tinyurlerror:
                result = str(
                    self.commands_text['tinyurl_command_data'][0]).format(
                    helper.link)
                try:
                    await self.bot.send_message(ctx.message.channel,
                                                content=result)
                except discord.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error(
                        ctx)

    # Unused but too lazy to remove this.
    # Might make this more universal with per server config on these.

    # @commands.command(name='giveme', pass_context=True, no_pm=True)
    # async def giveme_command(self, ctx):
    #     """
    #     Bot Commands.
    #     :param ctx: Messages.
    #     :return: Nothing.
    #     """
    #     if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
    #         return
    #     if ctx.message.channel.server and ctx.message.channel.server.id == \
    #             "81812480254291968":
    #         desrole = ctx.message.content[
    #                   len(ctx.prefix + "giveme "):].strip()
    #         role2 = discord.utils.find(lambda role: role.name == 'Muted',
    #                                    ctx.message.channel.server.roles)
    #         role3 = discord.utils.find(lambda role: role.name == 'Students',
    #                                    ctx.message.channel.server.roles)
    #         if 'admin' in desrole:
    #             if 'Muted' in ctx.message.author.roles:
    #                 await self.bot.add_roles(ctx.message.author, role2)
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'giveme_command_data'][
    #                                                     0]))
    #             else:
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'giveme_command_data'][
    #                                                     5]))
    #         elif 'student' in desrole:
    #             if 'Students' in ctx.message.author.roles:
    #                 await self.bot.add_roles(ctx.message.author, role3)
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'giveme_command_data'][
    #                                                     1]))
    #             else:
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'giveme_command_data'][
    #                                                     6]))
    #     else:
    #         if ctx.message.channel.server and \
    #                         ctx.message.channel.server.id == \
    #                         "127233852182626304":
    #             desrole = ctx.message.content[
    #                       len(ctx.prefix + "giveme "):].strip()
    #             rolelist = ctx.message.channel.server.roles
    #             role2 = discord.utils.find(
    #                 lambda role: role.name == '3rd Party Developer', rolelist)
    #             role3 = discord.utils.find(
    #                 lambda role: role.name == 'Streamer', rolelist)
    #             if 'dev' in desrole:
    #                 if role2 not in ctx.message.author.roles:
    #                     await self.bot.add_roles(ctx.message.author, role2)
    #                     await self.bot.send_message(ctx.message.channel,
    #                                                 content=str(
    #                                                     self.commands_text[
    #                                                         'giveme_comma'
    #                                                         'nd_data'][2]))
    #                 else:
    #                     await self.bot.send_message(ctx.message.channel,
    #                                                 content=str(
    #                                                     self.commands_text[
    #                                                         'giveme_comm'
    #                                                         'and_data'][7]))
    #             elif 'stream' in desrole:
    #                 if role3 not in ctx.message.author.roles:
    #                     await self.bot.add_roles(ctx.message.author, role3)
    #                     await self.bot.send_message(ctx.message.channel,
    #                                                 content=str(
    #                                                     self.commands_text[
    #                                                         'giveme_comm'
    #                                                         'and_data'][3]))
    #                 else:
    #                     await self.bot.send_message(ctx.message.channel,
    #                                                 content=str(
    #                                                     self.commands_text[
    #                                                         'giveme_co'
    #                                                         'mmand_data'][8]))
    #         else:
    #             try:
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'giveme_command_data'][
    #                                                     4]))
    #             except discord.Forbidden:
    #                 await self.bot.BotPMError.resolve_send_message_error(
    #                     self.bot, ctx)

    # @commands.command(name='remove', pass_context=True, no_pm=True)
    # async def remove_command(self, ctx):
    #     """
    #     Bot Commands.
    #     :param ctx: Messages.
    #     :return: Nothing.
    #     """
    #     if ctx.message.channel.id in self.bot.ignoreslist["channels"]:
    #         return
    #     if ctx.message.channel.server and ctx.message.channel.server.id == \
    #             "127233852182626304":
    #         desrole = ctx.message.content[
    #                   len(ctx.prefix + "remove "):].strip()
    #         rolelist = ctx.message.channel.server.roles
    #         role2 = discord.utils.find(
    #             lambda role: role.name == '3rd Party Developer', rolelist)
    #         role3 = discord.utils.find(lambda role: role.name == 'Streamer',
    #                                    rolelist)
    #         if 'dev' in desrole:
    #             if role2 in ctx.message.author.roles:
    #                 await self.bot.remove_roles(ctx.message.author, role2)
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'remove_command_data'][
    #                                                     0]))
    #             else:
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'remove_command_data'][
    #                                                     2]))
    #         elif 'stream' in desrole:
    #             if role3 in ctx.message.author.roles:
    #                 await self.bot.remove_roles(ctx.message.author, role3)
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'remove_command_data'][
    #                                                     1]))
    #             else:
    #                 await self.bot.send_message(ctx.message.channel,
    #                                             content=str(
    #                                                 self.commands_text[
    #                                                     'remove_command_data'][
    #                                                     3]))
    #     else:
    #         return

    # Helpers.

    def game_command_helper(self, ctx):
        """
        Bot `::game` command Helper.
        :param ctx: Message Context.
        :return: game data.
        """
        desgame = ctx.message.content[len(ctx.prefix + "game "):].strip()
        desgametype = None
        stream_url = None
        desgamesize = len(desgame)
        if desgamesize > 0:
            if len(ctx.message.mentions) > 0:
                for x in ctx.message.mentions:
                    desgame = desgame.replace(x.mention, x.name)
            if desgame.find(" | type=") is not -1:
                if desgame.find(" | type=1") is not -1:
                    desgame = desgame.replace(" | type=1", "")
                    desgametype = 1
                    stream_url = ctx.bot.BotConfig.twitch_url
                    return desgame, desgametype, stream_url, desgamesize
                elif desgame.find(" | type=2") is not -1:
                    desgame = desgame.replace(" | type=2", "")
                    desgametype = 2
                    stream_url = ctx.bot.BotConfig.youtube_url
                    return desgame, desgametype, stream_url, desgamesize
            else:
                return desgame, desgametype, stream_url, desgamesize
        else:
            desgame = None
            return desgame, desgametype, stream_url, desgamesize


def setup(bot):
    """
    DecoraterBot's various commands Plugin.
    """
    new_cog = Commands(bot)
    bot.add_cog(new_cog)
