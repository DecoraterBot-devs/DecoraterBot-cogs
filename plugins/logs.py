# coding=utf-8
"""
logging Plugin for DecoraterBot.

This is the default logger for DecoraterBot.
"""
import traceback
import json
import re
import sys
import json
import os

from colorama import Fore, Back, Style
import discord

from .. import BotErrors


# Some loggers lack the ability to get the server
# the event fired on.


class CogLogger:
    """
    Main cog logging Class.
    """
    def __init__(self, bot):
        self.bot = bot
        try:
            self.LogDataFile = open(
                '{0}{1}resources{1}ConfigData{1}LogData.json'.format(
                self.bot.path, self.bot.sepa))
            self.LogData = json.load(self.LogDataFile)
            self.LogData = self.LogData[self.bot.BotConfig.language]
            self.LogDataFile.close()
        except FileNotFoundError:
            print(str(self.bot.consoletext['Missing_JSON_Errors'][2]))
            sys.exit(2)

    def log_writter(self, filename, data):
        """
        Log file writter.

        This is where all the common
        log file writes go to.
        """
        str(self)
        file = open(filename, 'a', encoding='utf-8')
        size = os.path.getsize(filename)
        if size >= 32102400:
            file.seek(0)
            file.truncate()
        file.write(data)
        file.close()

    def log_data_reader(entry, index, *args):
        """
        log data reader that also
        does the needed formatting.

        method specifically to fix the
        stupid Codacy duplication bug.
        """
        return str(self.LogData[entry][index]).format(
            *args)

    def logs(self, message):
        """
        Logs Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = str(self.LogData['On_Message_Logs'][0]).format(
            message.author.name, message.author.id, str(
                message.timestamp), message.content)
        if message.channel.is_private is False:
            logs003 = str(self.LogData['On_Message_Logs'][1]).format(
                message.author.name, message.author.id, str(
                    message.timestamp), message.channel.server.name,
                message.channel.name, message.content)
        if message.content is not None:
            logfile = '{0}{1}resources{1}Logs{1}log.log'.format(
                self.bot.path, self.bot.sepa)
            try:
                if message.channel.is_private is True:
                    self.log_writter(logfile, logs001)
                else:
                    self.log_writter(logfile, logs003)
            except PermissionError:
                return

    def edit_logs(self, before, after):
        """
        Logs Edited Messages.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        logfile = '{0}{1}resources{1}Logs{1}edit_log.log'.format(
            self.bot.path, self.bot.sepa)
        editlog001 = str(self.LogData['On_Message_Logs'][0]).format(
            before.author.name, before.author.id,
            str(before.timestamp), str(before.content),
            str(after.content))
        if before.channel.is_private is False:
            editlog003 = str(self.LogData['On_Message_Logs'][1]).format(
                before.author.name, before.author.id,
                str(before.timestamp), before.channel.server.name,
                before.channel.name, str(before.content),
                str(after.content))
        try:
            try:
                if before.content == after.content:
                    self.resolve_embed_logs(before)
                else:
                    try:
                        self.log_writter(logfile, editlog003)
                    except PermissionError:
                        return
            except Exception as e:
                # Empty string that is not used nor assigned
                # to a variable. (for now)
                str(e)
                if before.channel.is_private is False:
                    print(str(self.LogData['On_Edit_Logs_Error'][0]))
                else:
                    if before.content == after.content:
                        self.resolve_embed_logs(before)
                    else:
                        self.log_writter(logfile, editlog001)
        except PermissionError:
            return

    def delete_logs(self, message):
        """
        Logs Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        dellogs001 = str(self.LogData['On_Message_Logs'][0]).format(
            message.author.name, message.author.id,
            str(message.timestamp), message.content)
        dellogspm = dellogs001
        dellogsservers = None
        if message.channel.is_private is False:
            dellogs003 = str(self.LogData['On_Message_Logs'][1]).format(
                message.author.name, message.author.id,
                str(message.timestamp),
                message.channel.server.name,
                message.channel.name, message.content)
            dellogsservers = dellogs003
        if message.content is not None:
            try:
                logfile = '{0}{1}resources{1}Logs{1}delete_log.log'.format(
                    self.bot.path, self.bot.sepa)
                if message.channel.is_private is True:
                    self.log_writter(logfile, dellogspm)
                else:
                    self.log_writter(logfile, dellogsservers)
            except PermissionError:
                return

    def resolve_embed_logs(self, before):
        """
        Resolves if the message was edited or not.
        :param before: Messages.
        :return: Nothing.
        """
        if before.channel.is_private is True:
            data = str(self.LogData['Embed_Logs'][0])
        else:
            data = str(self.LogData['Embed_Logs'][1])
        logfile = '{0}{1}resources{1}Logs{1}embeds.log'.format(self.bot.path,
                                                               self.bot.sepa)
        try:
            self.log_writter(logfile, data + "\n")
        except PermissionError:
            return

    async def send_logs(self, message):
        """
        Sends Sent Messages.
        :param message: Messages.
        :return: Nothing.
        """
        logs001 = self.log_data_reader(
            'Send_On_Message_Logs', 0,
            message.author.name, message.author.id,
            str(message.timestamp),
            message.channel.server.name, message.channel.name,
            message.content)
        sndmsglogs = logs001
        try:
            await self.bot.send_message(
                discord.Object(id='153055192873566208'), content=sndmsglogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    async def send_edit_logs(self, before, after):
        """
        Sends Edited Messages.
        :param before: Messages.
        :param after: Messages.
        :return: Nothing.
        """
        old = str(before.content)
        new = str(after.content)
        editlog001 = str(self.LogData['Send_On_Message_Edit_Logs'][0]).format(
            before.author.name, before.author.id,
            str(before.timestamp),
            before.channel.server.name,
            before.channel.name, old, new)
        sendeditlogs = editlog001
        if before.content != after.content:
            try:
                await self.bot.send_message(
                    discord.Object(id='153055192873566208'),
                    content=sendeditlogs)
            except discord.errors.NotFound:
                return
            except discord.errors.HTTPException:
                return

    async def send_delete_logs(self, message):
        """
        Sends Deleted Messages.
        :param message: Messages.
        :return: Nothing.
        """
        dellogs001 = self.log_data_reader(
            'Send_On_Message_Delete_Logs', 0,
            message.author.name, message.author.id, str(message.timestamp),
            message.channel.server.name, message.channel.name,
            message.content)
        senddeletelogs = dellogs001
        try:
            await self.bot.send_message(
                discord.Object(id='153055192873566208'),
                content=senddeletelogs)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def on_bot_error(self, funcname, tbinfo, err):
        """
            This Function is for Internal Bot use only.
            It is for catching any Errors and writing them to a file.

            Usage
            =====
            :param funcname: Must be a string with the name of the function
            that caused a Error.
                raises the Errors that happened if empty string or None is
                given.
            :param tbinfo: string data of the traceback info. Must be a
                string for this to not Error itself.
                raises the Errors that happened if empty string or None is
                given.
            :param err: Error Data from Traceback. (RAW)
        """
        if bool(funcname):
            if bool(tbinfo):
                exception_data = 'Ignoring exception caused at {0}:\n' \
                                 '{1}'.format(funcname, tbinfo)
                logfile = '{0}{1}resources{1}Logs{1}error_log.log'.format(
                    self.bot.path, self.bot.sepa)
                try:
                    self.log_writter(logfile, exception_data)
                except PermissionError:
                    return
            else:
                raise err
        else:
            raise err

    def onban(self, member):
        """
        Logs Bans.
        :param member: Members.
        :return: Nothing.
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        ban_log_data = str(self.LogData['Ban_Logs'][0]).format(mem_name,
                                                               mem_id, mem_dis,
                                                               mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}bans.log'.format(self.bot.path,
                                                             self.bot.sepa)
        self.log_writter(logfile, ban_log_data)

    async def send_ban_logs(self, channel, member):
        """
        sends the ban log data to a specific channel.
        """
        ban_log_data = str(self.LogData['Send_Ban_Logs'][0]).format(
            member.name, member.id, member.discriminator)
        try:
            await self.bot.send_message(
                channel, content=ban_log_data)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def onavailable(self, server):
        """
        Logs Available Servers.
        :param server:
        :return: Nothing.
        """
        available_log_data = str(
            self.LogData['On_Server_Available'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}available_servers.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, available_log_data)

    def onunavailable(self, server):
        """
        Logs Unavailable Servers
        :param server: Servers.
        :return: Nothing.
        """
        unavailable_log_data = str(
            self.LogData['On_Server_Unavailable'][0]).format(server)
        logfile = '{0}{1}resources{1}Logs{1}unavailable_servers.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, unavailable_log_data)

    def onunban(self, server, user):
        """
        Logs Unbans.
        :param server: Server.
        :param user: Users.
        :return: Nothing.
        """
        unban_log_data = str(self.LogData['Unban_Logs'][0]
                             ).format(user.name, user.id, user.discriminator,
                                      server.name)
        logfile = '{0}{1}resources{1}Logs{1}unbans.log'.format(self.bot.path,
                                                               self.bot.sepa)
        self.log_writter(logfile, unban_log_data)

    async def send_unban_logs(self, channel, user):
        """
        sends the unban log data to a specific channel.
        """
        unban_log_data = str(self.LogData['Send_Unban_Logs'][0]).format(
            user.name, user.id, user.discriminator)
        try:
            await self.bot.send_message(
                channel, content=unban_log_data)
        except discord.errors.NotFound:
            return
        except discord.errors.HTTPException:
            return

    def ongroupjoin(self, channel, user):
        """
        Logs group join.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        mem_name = user.name
        mem_id = user.id
        mem_dis = user.discriminator
        mem_channel_name = channel.name
        group_join_log_data = str(self.LogData['Group_Join_Logs'][0]).format(
            mem_name, mem_id, mem_dis, mem_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}group_join.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, group_join_log_data)

    def ongroupremove(self, channel, user):
        """
        Logs group remove.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        mem_name = user.name
        mem_id = user.id
        mem_dis = user.discriminator
        mem_channel_name = channel.name
        group_remove_log_data = str(self.LogData['Group_Remove_Logs'][0]).format(
            mem_name, mem_id, mem_dis, mem_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}group_remove.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, group_remove_log_data)

    def ontyping(self, channel, user, when):
        """
        Logs when a user is typing.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        typing_log_data = str(self.LogData['On_typing'][0]).format(
            user.name, user.id, user.discriminator, channel.name,
            str(when))
        logfile = '{0}{1}resources{1}Logs{1}typing.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, typing_log_data)

    def onvoicestateupdate(self, before, after):
        """
        Logs When someone updates their voice state.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        mem_name = before.user.name
        mem_id = before.user.id
        mem_dis = before.user.discriminator
        before_channel_name = before.channel.name
        after_channel_name = after.channel.name
        voice_update_log_data = str(self.LogData['voice_update'][0]).format(
            mem_name, mem_id, mem_dis, before_channel_name,
            after_channel_name)
        logfile = '{0}{1}resources{1}Logs{1}voice_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, voice_update_log_data)

    def onchanneldelete(self, channel):
        """
        Logs Channel Deletion.
        :param channel: Channel.
        """
        channel_delete_log_data = str(self.LogData['channel_delete'][0]).format(
            channel.name, channel.id)
        logfile = '{0}{1}resources{1}Logs{1}channel_delete.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_delete_log_data)

    def onchannelcreate(self, channel):
        """
        Logs Channel Creation.
        :param channel: Channel.
        """
        channel_create_log_data = str(self.LogData['channel_create'][0]).format(
            channel.name, channel.id)
        logfile = '{0}{1}resources{1}Logs{1}channel_create.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_create_log_data)

    def onchannelupdate(self, before, after):
        """
        Logs Channel Updates.
        :param before: Channel before.
        :param after: Channel after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        channel_update_log_data = str(self.LogData['channel_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}channel_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, channel_update_log_data)

    def onmemberupdate(self, before, after):
        """
        Logs Member Updates.
        :param before: Member before.
        :param after: Member after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        member_update_log_data = str(self.LogData['member_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}member_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, member_update_log_data)

    def onserverjoin(self, server):
        """
        Logs server Joins.
        :param server: Server.
        :return: Nothing.
        """
        server_join_log_data = str(self.LogData['server_join'][0]).format(
            self.bot.user.name, self.bot.user.id, server.name)
        logfile = '{0}{1}resources{1}Logs{1}server_join.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_join_log_data)

    def onserverremove(self, server):
        """
        Logs server Removes.
        :param server: Server.
        :return: Nothing.
        """
        server_remove_log_data = str(self.LogData['server_remove'][0]).format(
            self.bot.user.name, self.bot.user.id, server.name)
        logfile = '{0}{1}resources{1}Logs{1}server_remove.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_remove_log_data)

    def onserverupdate(self, before, after):
        """
        Logs Server Updates.
        :param before: Server before.
        :param after: Server after.
        :return: Nothing.
        """
        server_update_log_data = str(self.LogData['server_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}server_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_update_log_data)

    def onserverrolecreate(self, role):
        """
        Logs role Creation.
        :param role: Role.
        :return: Nothing.
        """
        role_create_log_data = str(self.LogData['role_create'][0]).format(
            role.name, role.id)
        logfile = '{0}{1}resources{1}Logs{1}role_create.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_create_log_data)

    def onserverroledelete(self, role):
        """
        Logs role Deletion.
        :param role: Role.
        :return: Nothing.
        """
        role_delete_log_data = str(self.LogData['role_delete'][0]).format(
            role.name, role.id)
        logfile = '{0}{1}resources{1}Logs{1}role_delete.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_delete_log_data)

    def onserverroleupdate(self, before, after):
        """
        Logs Role updates.
        :param before: Role before.
        :param after: Role after.
        :return: Nothing.
        """
        # change of permittions trigger this???
        role_update_log_data = str(self.LogData['role_update'][0]).format(
            before.name, before.id, after.name)
        logfile = '{0}{1}resources{1}Logs{1}role_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, role_update_log_data)

    def onsocketrawreceive(self, msg):
        """
        Logs socket Raw recieves.
        :param msg: Message from socket.
        :return: Nothing.
        """
        raw_receive_log_data = str(self.LogData['raw_receive'][0]).format(
            msg)
        logfile = '{0}{1}resources{1}Logs{1}raw_receive.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, raw_receive_log_data)

    def onsocketrawsend(self, payload):
        """
        Logs socket raw sends.
        :param payload: Payload that was sent.
        :return: Nothing.
        """
        raw_send_log_data = str(self.LogData['raw_send'][0]).format(
            payload)
        logfile = '{0}{1}resources{1}Logs{1}raw_send.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, raw_send_log_data)

    def onresumed(self):
        """
        Logs when bot resumes.
        :return: Nothing.
        """
        resumed_log_data = str(self.LogData['resumed'][0])
        logfile = '{0}{1}resources{1}Logs{1}resumed.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, resumed_log_data)

    def onserveremojisupdate(self, before, after):
        """
        Logs Server emoji updates.
        :param before: Emoji before.
        :param after: Emoji after.
        :return: Nothing.
        """
        server_emojis_update_log_data = str(
            self.LogData['server_emojis_update'][0]).format(
            before.name, before.id, before.server.name,
            after.name)
        logfile = '{0}{1}resources{1}Logs{1}server_emojis_update.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, server_emojis_update_log_data)

    def onreactionadd(self, reaction, user):
        """
        Logs Reactions Added.
        :param reaction: Reaction.
        :param user: User.
        :return: Nothing.
        """
        reaction_add_log_data = str(
            self.LogData['reaction_add'][0]).format(
            user.name, user.id, user.server, reaction.emoji.name,
            reaction.emoji.id, reaction.emoji.server.name)
        logfile = '{0}{1}resources{1}Logs{1}reaction_add.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, reaction_add_log_data)

    def onreactionremove(self, reaction, user):
        """
        Logs Reaction Removals.
        :param reaction: Reaction.
        :param user: User.
        :return: Nothing.
        """
        reaction_remove_log_data = str(
            self.LogData['reaction_remove'][0]).format(
            user.name, user.id, user.server, reaction.emoji.name,
            reaction.emoji.id, reaction.emoji.server.name)
        logfile = '{0}{1}resources{1}Logs{1}reaction_remove.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, reaction_remove_log_data)

    def onreactionclear(self, message, reactions):
        """
        Logs Reaction clears.
        :param message: Message.
        :param reactions: Reactions.
        :return: Nothing.
        """
        reactionnames = [
            reaction.emoji.name for reaction in reactions]
        reactionids = [
            reaction.emoji.id for reaction in reactions]
        reactionservers = [
            reaction.emoji.server.name for reaction in reactions]
        reaction_clear_log_data = str(
            self.LogData['reaction_clear'][0]).format(
            message.author.name, message.author.id, message.author.server,
            reactionnames, reactionids, reactionservers)
        logfile = '{0}{1}resources{1}Logs{1}reaction_clear.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, reaction_clear_log_data)

    def onmemberjoin(self, member):
        """
        Logs Member Joins.
        :param member: Member.
        :return: Nothing.
        """
        member_join_log_data = str(self.LogData['member_join'][0]).format(
            member.name, member.id, member.discriminator,
            member.server.name)
        logfile = '{0}{1}resources{1}Logs{1}member_join.log'.format(
            self.bot.path, self.bot.sepa)
        self.log_writter(logfile, member_join_log_data)

    def onkick(self, member):
        """
        Logs Kicks.
        :param member: Members.
        :return: Nothing.
        """
        mem_name = member.name
        mem_id = member.id
        mem_dis = member.discriminator
        mem_svr_name = member.server.name
        kick_log_data = str(self.LogData['Kick_Logs'][0]).format(mem_name,
                                                                 mem_id,
                                                                 mem_dis,
                                                                 mem_svr_name)
        logfile = '{0}{1}resources{1}Logs{1}kicks.log'.format(self.bot.path,
                                                              self.bot.sepa)
        self.log_writter(logfile, kick_log_data)


class BotLogger:
    """
    Logging Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.logs_text = self.bot.PluginTextReader(
            file='commands.json')
        self.logger = CogLogger(self.bot)

    async def on_command_error(self, error, ctx):
        """..."""
        if ctx.command is not None:
            tbinfo = traceback.format_exception(
                type(error), error, error.__traceback__)
            await self.bot.send_message(
                ctx.message.channel,
                "exception in command {0}:```py\n{1}```".format(
                    ctx.command,
                    self.command_traceback_helper(tbinfo)))

    async def on_message(self, message):
        """
        Bot Event.
        :param message: Messages.
        :return: Nothing.
        """
        if self.bot.user.mention in message.content:
            await self.bot_mentioned_helper(message)
        # if len(message.mentions) > 5:
        #    await self.mention_ban_helper(message)
        if not message.channel.is_private:
            try:
                if message.channel.server and message.channel.server.id == \
                        "81812480254291968":
                    if message.author.id == self.bot.user.id:
                        return
                    elif message.channel.id == "153055192873566208":
                        pass
                    elif message.channel.id == "87382611688689664":
                        pass
                    else:
                        if self.bot.BotConfig.logging:
                            await self.logger.send_logs(self.bot, message)
                elif message.channel.server and message.channel.server.id == \
                        "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        if self.bot.logging:
                            self.logger.logs(message)
                        await self.cheesy_commands_helper(message)
                    else:
                        # await self.bot.everyone_mention_logger(message)
                        if self.bot.BotConfig.logging:
                            self.logger.logs(message)
                else:
                    if self.bot.BotConfig.logging:
                        self.logger.logs(message)
            except Exception as e:
                if self.bot.BotConfig.pm_command_errors:
                    if self.bot.BotConfig.discord_user_id is not None:
                        owner = self.bot.BotConfig.discord_user_id
                        exception_data2 = str(traceback.format_exc())
                        message_data = '```py\n{0}\n```'.format(
                            exception_data2)
                        try:
                            await self.bot.send_message(discord.User(id=owner),
                                                        content=message_data)
                        except discord.errors.Forbidden:
                            pass
                        except discord.errors.HTTPException:
                            funcname = 'on_message'
                            tbinfo = str(traceback.format_exc())
                            await self.logger.on_bot_error(funcname,
                                                               tbinfo, e)
                    else:
                        return
                else:
                    funcname = 'on_message'
                    tbinfo = str(traceback.format_exc())
                    await self.logger.on_bot_error(funcname, tbinfo, e)
        if message.channel.is_private:
            if self.bot.BotConfig.is_official_bot:
                # possible regex patterns for discord server invites
                patterns = [
                    '(https?:\/\/)?discord\.gg\/[a-zA-Z0-9\-]{2,16}',
                    '(https?:\/\/)?discordapp\.com\/invite\/[a-zA-Z0-9\-]{2,16}'
                ]
                for pattern in patterns:
                    regex = re.compile(pattern)
                    searchres = regex.search(message.content)
                    if searchres is not None:
                        await self.bot.send_message(
                            message.channel, content=str(
                                self.logs_text[
                                    'join_command_data'
                                ][3]))

    async def on_message_edit(self, before, after):
        """
        Bot Event.
        :param before: Message.
        :param after: Message.
        :return: Nothing.
        """
        try:
            if before.channel.is_private is not False:
                if self.bot.BotConfig.logging:
                    self.logger.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == \
                    "81812480254291968":
                if before.author.id == self.bot.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    await self.logger.send_edit_logs(before,
                                                         after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.logger.edit_logs(before, after)
        except Exception as e:
            funcname = 'on_message_edit'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if message.channel.is_private is not False:
                if self.bot.BotConfig.logging:
                    self.logger.delete_logs(message)
            elif message.channel.server and message.channel.server.id == \
                    "81812480254291968":
                if message.author.id == self.bot.user.id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    await self.logger.send_delete_logs(message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.logger.delete_logs(message)
        except Exception as e:
            funcname = 'on_message_delete'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_delete:
            self.logger.onchanneldelete(channel)

    async def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_create:
            self.logger.onchannelcreate(channel)

    async def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_update:
            self.logger.onchannelupdate(before, after)

    async def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logbans:
                self.logger.onban(member)
            if member.server.id == "71324306319093760":
                await self.verify_cache_cleanup(member)
            for channel in member.server.channels:
                if channel.name == 'mod-log':
                    await self.logger.send_ban_logs(channel, member)
        except Exception as e:
            funcname = 'on_member_ban'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logunbans:
                self.logger.onunban(server, user)
            for channel in server.channels:
                if channel.name == 'mod-log':
                    await self.logger.send_unban_logs(channel, user)
        except Exception as e:
            funcname = 'on_member_unban'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_member_remove(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            try:
                banslist = await self.bot.get_bans(member.server)
                if member in banslist:
                    return
                else:
                    if self.bot.BotConfig.logkicks:
                        self.logger.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden,
                    BotErrors.CommandTimeoutError):
                if self.bot.BotConfig.logkicks:
                    self.logger.onkick(member)
            if member.server and member.server.id == "71324306319093760":
                await self.verify_cache_cleanup_2(member)
        except Exception as e:
            funcname = 'on_member_remove'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_member_update:
            self.logger.onmemberupdate(before, after)

    async def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_member_join:
                self.logger.onmemberjoin(member)
            if member.server.id == '71324306319093760' and member.bot is not \
                    True:
                file_path_join_1 = '{0}resources{0}ConfigData{0}' \
                                   'serverconfigs{0}'.format(self.bot.sepa)
                filename_join_1 = 'servers.json'
                serveridslistfile = open(
                    self.bot.path + file_path_join_1 + filename_join_1)
                serveridslist = json.load(serveridslistfile)
                serveridslistfile.close()
                serverid = str(serveridslist['config_server_ids'][0])
                file_path_join_2 = '{0}resources{0}ConfigData{0}' \
                                   'serverconfigs{0}{1}{0}verificat' \
                                   'ions{0}'.format(self.bot.sepa, serverid)
                filename_join_2 = 'verifymessages.json'
                filename_join_3 = 'verifycache.json'
                filename_join_4 = 'verifycache.json'
                memberjoinmessagedatafile = open(
                    self.bot.path + file_path_join_2 + filename_join_2)
                memberjoinmessagedata = json.load(memberjoinmessagedatafile)
                memberjoinmessagedatafile.close()
                msg_info = str(memberjoinmessagedata['verify_messages'][0])
                message_data = msg_info.format(member.id, member.server.name)
                des_channel = str(
                    memberjoinmessagedata['verify_messages_channel'][0])
                joinedlistfile = open(
                    self.bot.path + file_path_join_2 + filename_join_3)
                newlyjoinedlist = json.load(joinedlistfile)
                joinedlistfile.close()
                await self.bot.send_message(discord.Object(id=des_channel),
                                            content=message_data)
                if member.id in newlyjoinedlist['users_to_be_verified']:
                    # since this person is already in the list lets
                    #  not readd them.
                    pass
                else:
                    newlyjoinedlist['users_to_be_verified'].append(member.id)
                    json.dump(newlyjoinedlist, open(
                        self.bot.path + file_path_join_2 + filename_join_4,
                        "w"))
        except Exception as e:
            funcname = 'on_member_join'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_available:
            self.logger.onavailable(server)

    async def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_unavailable:
            self.logger.onunavailable(server)

    async def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_join:
            self.logger.onserverjoin(server)
        try:
            await self.bot.dbapi.send_stats(
                len(self.bot.servers),
                self.bot.user.id)
        except:
            pass

    async def on_server_remove(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_remove:
            self.logger.onserverremove(server)
        try:
            await self.bot.dbapi.send_stats(
                len(self.bot.servers),
                self.bot.user.id)
        except:
            pass

    async def on_server_update(self, before, after):
        """
        Bot Event.
        :param before: Server.
        :param after: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_update:
            self.logger.onserverupdate(before, after)

    async def on_ready(self):
        """
        Bot Event.
        :return: Nothing.
        """
        try:
            await self.on_bot_login()
        except Exception as e:
            funcname = 'on_ready'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_bot_login(self):
        """
        Function that does the on_ready event stuff after logging in.
        :return: Nothing.
        """
        if self.bot.logged_in_:
            self.bot.logged_in_ = False
            bot_name = self.bot.user.name
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + str(
                self.bot.consoletext['Window_Login_Text'][0]).format(
                bot_name, self.bot.user.id, discord.__version__))
            sys.stdout = open(
                '{0}{1}resources{1}Logs{1}console.log'.format(
                    self.bot.path, self.bot.sepa), 'w')
            sys.stderr = open(
                '{0}{1}resources{1}Logs{1}unhandled_tracebacks.log'.format(
                    self.bot.path, self.bot.sepa),
                'w')
            try:
                await self.bot.dbapi.send_stats(
                    len(self.bot.servers),
                    self.bot.user.id)
            except:
                pass
        if not self.bot.logged_in_:
            game_name = str(
                self.bot.consoletext['On_Ready_Game'][0]).format(
                self.bot.command_prefix)
            stream_url = "https://twitch.tv/decoraterbot"
            await self.bot.change_presence(
                game=discord.Game(name=game_name, type=1, url=stream_url))

    async def on_server_role_create(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_create:
            self.logger.onserverrolecreate(role)

    async def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_delete:
            self.logger.onserverroledelete(role)

    async def on_error(self, event, *args, **kwargs):
        """
        Bot Event.
        :param event: Event.
        :param args: Args.
        :param kwargs: Other Args.
        :return: Nothing.
        """
        str(args)
        str(kwargs)
        funcname = event
        tbinfo = str(traceback.format_exc())
        self.logger.on_bot_error(funcname, tbinfo, None)

    async def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_update:
            self.logger.onserverroleupdate(before, after)

    async def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_join:
                self.logger.ongroupjoin(channel, user)
        except Exception as e:
            funcname = 'on_group_join'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_remove:
                self.logger.ongroupremove(channel, user)
        except Exception as e:
            funcname = 'on_group_remove'
            tbinfo = str(traceback.format_exc())
            self.logger.on_bot_error(funcname, tbinfo, e)

    async def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_voice_state_update:
            self.logger.onvoicestateupdate(before, after)

    async def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_typing:
            self.logger.ontyping(channel, user, when)

    async def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_receive:
            self.logger.onsocketrawreceive(msg)

    async def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_send:
            self.logger.onsocketrawsend(payload)

    async def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_resumed:
            self.logger.onresumed()

    # new events (Since Discord.py v0.13.0+).

    async def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_emojis_update:
            self.logger.onserveremojisupdate(before, after)

    # added in Discord.py v0.14.3.

    async def on_reaction_add(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_add:
            self.logger.onreactionadd(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_remove:
            self.logger.onreactionremove(reaction, user)

    # added in Discord.py v0.15.0.

    async def on_reaction_clear(self, message, reactions):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_clear:
            self.logger.onreactionclear(message, reactions)

    # Helpers.

    def command_traceback_helper(self, tbinfo):
        """
        Helps itterate trhough an list of every
        line in a command's traceback.
        """
        tracebackdata = ""
        for line in tbinfo:
            tracebackdata = tracebackdata + line
        return tracebackdata

    async def mention_ban_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id == self.bot.user.id:
            return
        if message.channel.server.id == "105010597954871296":
            return
        if message.author.id == self.bot.owner_id:
            return
        else:
            try:
                await self.bot.ban(message.author)
                try:
                    message_data = str(
                        self.logs_text['mention_spam_ban'][0]).format(
                        message.author)
                    await self.bot.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error_old(
                        self.bot, message)
            except discord.errors.Forbidden:
                try:
                    msgdata = str(
                        self.logs_text['mention_spam_ban'][1]).format(
                        message.author)
                    message_data = msgdata
                    await self.bot.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error_old(
                        self.bot, message)
            except discord.HTTPException:
                try:
                    msgdata = str(
                        self.logs_text['mention_spam_ban'][2]).format(
                        message.author)
                    message_data = msgdata
                    await self.bot.send_message(message.channel,
                                            content=message_data)
                except discord.errors.Forbidden:
                    await self.bot.BotPMError.resolve_send_message_error_old(
                        self.bot, message)

    async def bot_mentioned_helper(self, message):
        """
        Bot Commands.
        :param message: Messages.
        :return: Nothing.
        """
        if message.author.id in self.bot.banlist['Users']:
            return
        elif message.author.bot:
            return
        else:
            for command in self.bot.commands_list:
                if message.content.startswith(command):
                    return
                else:
                    break
            else:
                if message.channel.server.id == "140849390079180800":
                    return
                elif message.author.id == self.bot.user.id:
                    return
                elif message.channel.server.id == "110373943822540800":
                    if message.author.id == "103607047383166976":
                        return
                    else:
                        info2 = str(
                            self.logs_text['On_Bot_Mention_Message_Data'][
                                0]).format(message.author)
                        await self.bot.send_message(message.channel, content=info2)
                elif message.channel.server.id == '101596364479135744':
                    if message.author.id == "110368240768679936":
                        return
                    else:
                        info2 = str(
                            self.logs_text['On_Bot_Mention_Message_Data'][
                                0]).format(message.author)
                        await self.bot.send_message(message.channel, content=info2)
                else:
                    info2 = str(
                        self.logs_text['On_Bot_Mention_Message_Data'][
                            0]).format(message.author)
                    try:
                        await self.bot.send_message(message.channel, content=info2)
                    except discord.errors.Forbidden:
                        await self.bot.BotPMError.resolve_send_message_error_old(
                            self.bot, message)

    async def cheesy_commands_helper(self, message):
        """
        Listens fCheese.lab Specific Server commands.
        :param message: Message.
        :return: Nothing.
        """
        serveridslistfile = open(
            '{0}{1}resources{1}ConfigData{1}serverconfigs{1}servers.'
            'json'.format(self.bot.path, self.bot.sepa))
        serveridslist = json.load(serveridslistfile)
        serveridslistfile.close()
        serverid = str(serveridslist['config_server_ids'][0])
        file_path = (
            '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}'
            'verifications{0}'.format(self.bot.sepa, serverid))
        filename_1 = 'verifycache.json'
        filename_2 = 'verifycommand.json'
        filename_3 = 'verifyrole.json'
        filename_4 = 'verifymessages.json'
        filename_5 = 'verifycache.json'
        joinedlistfile = open(self.bot.path + file_path + filename_1)
        newlyjoinedlist = json.load(joinedlistfile)
        joinedlistfile.close()
        memberjoinverifymessagefile = open(self.bot.path + file_path + filename_2)
        memberjoinverifymessagedata = json.load(memberjoinverifymessagefile)
        memberjoinverifymessagefile.close()
        memberjoinverifyrolefile = open(self.bot.path + file_path + filename_3)
        memberjoinverifyroledata = json.load(memberjoinverifyrolefile)
        memberjoinverifyrolefile.close()
        memberjoinverifymessagefile2 = open(self.bot.path + file_path + filename_4)
        memberjoinverifymessagedata2 = json.load(memberjoinverifymessagefile2)
        memberjoinverifymessagefile2.close()
        role_name = str(memberjoinverifyroledata['verify_role_id'][0])
        msg_command = str(memberjoinverifymessagedata['verify_command'][0])
        try:
            if '>' or '<' or '`' in message.content:
                msgdata = message.content.replace('<', '').replace('>',
                                                                   '').replace(
                    '`', '')
            else:
                msgdata = message.content
            if msg_command == msgdata:
                if message.author.id in newlyjoinedlist[
                        'users_to_be_verified']:
                    await self.bot.delete_message(message)
                    role2 = discord.utils.find(
                        lambda role: role.id == role_name,
                        message.channel.server.roles)
                    msg_data = str(
                        memberjoinverifymessagedata2['verify_messages'][
                            1]).format(
                        message.server.name)
                    await self.bot.add_roles(message.author, role2)
                    await self.bot.send_message(message.author, content=msg_data)
                    newlyjoinedlist['users_to_be_verified'].remove(
                        message.author.id)
                    json.dump(newlyjoinedlist,
                              open(self.path + file_path + filename_5, "w"))
                else:
                    await self.bot.delete_message(message)
                    await self.bot.send_message(message.channel, content=str(
                        memberjoinverifymessagedata2['verify_messages'][2]))
            else:
                if message.author.id != self.bot.user.id:
                    if message.author.id in newlyjoinedlist[
                            'users_to_be_verified']:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(message.channel, content=str(
                            memberjoinverifymessagedata2['verify_messages'][
                                3]).format(message.author.mention))
        except NameError:
            await self.bot.send_message(message.channel, content=str(
                memberjoinverifymessagedata2['verify_messages'][4]).format(
                message.author.mention))

    # Cache Cleanup.

    async def verify_cache_cleanup_2(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = open(
                '{0}{1}resources{1}ConfigData{1}serverconfigs{1}'
                'servers.json'.format(self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = (
                '{0}resources{0}ConfigData{0}serverconfigs{0}{1}{0}'
                'verifications{0}'.format(self.sepa, serverid))
            filename_1 = 'verifycache.json'
            joinedlistfile = open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                await self.send_message(
                    discord.Object(id='141489876200718336'),
                    content="{0} has left the {1} Server.".format(
                        member.mention, member.server.name))
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(
                    self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs{1}" \
                           "71324306319093760{2}".format(self.path, self.sepa,
                                                         file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup_2'
            tbinfo = str(traceback.format_exc())
            self.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def verify_cache_cleanup(self, member):
        """
        Cleans Up Verify Cache.
        :param member: Member.
        :return: Nothing.
        """
        try:
            serveridslistfile = open(
                '{0}{1}resources{1}ConfigData{1}serverconfigs{1}'
                'servers.json'.format(
                    self.path, self.sepa))
            serveridslist = json.load(serveridslistfile)
            serveridslistfile.close()
            serverid = str(serveridslist['config_server_ids'][0])
            file_path = '{0}resources{0}ConfigData{0}serverconfigs{0}{1}' \
                        '{0}verifications{0}'.format(self.sepa, serverid)
            filename_1 = 'verifycache.json'
            joinedlistfile = open(self.path + file_path + filename_1)
            newlyjoinedlist = json.load(joinedlistfile)
            joinedlistfile.close()
            if member.id in newlyjoinedlist['users_to_be_verified']:
                newlyjoinedlist['users_to_be_verified'].remove(member.id)
                file_name = "{0}verifications{0}verifycache.json".format(
                    self.sepa)
                filename = "{0}{1}resources{1}ConfigData{1}serverconfigs" \
                           "{1}71324306319093760{2}".format(self.path,
                                                            self.sepa,
                                                            file_name)
                json.dump(newlyjoinedlist, open(filename, "w"))
        except Exception as e:
            funcname = 'verify_cache_cleanup'
            tbinfo = str(traceback.format_exc())
            self.DBLogs.on_bot_error(funcname, tbinfo, e)


def setup(bot):
    """
    DecoraterBot's logging Plugin.
    """
    bot.add_cog(BotLogger(bot))
