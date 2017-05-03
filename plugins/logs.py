# coding=utf-8
"""
logging Plugin for DecoraterBot.

This is the default logger for DecoraterBot.
"""
import traceback
import json
import re
import sys

from colorama import Fore, Back, Style
import discord

from .. import BotErrors


class BotLogger:
    """
    Logging Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.logs_text = self.bot.PluginTextReader(
            file='commands.json')

    async def on_command_error(self, exception, context):
        """..."""
        type(exception)
        if context.command is not None:
            tbinfo = traceback.format_exc()
            await self.bot.send_message(
                context.message.channel,
                "exception in command {0}:```py\n{1}```".format(
                    context.command, tbinfo))

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
                            await self.bot.DBLogs.send_logs(self.bot, message)
                elif message.channel.server and message.channel.server.id == \
                        "71324306319093760":
                    if message.channel.id == '141489876200718336':
                        if self.bot.logging:
                            self.bot.DBLogs.logs(message)
                        await self.cheesy_commands_helper(message)
                    else:
                        # await self.bot.everyone_mention_logger(message)
                        if self.bot.BotConfig.logging:
                            self.bot.DBLogs.logs(message)
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.logs(message)
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
                            await self.bot.DBLogs.on_bot_error(funcname,
                                                               tbinfo, e)
                    else:
                        return
                else:
                    funcname = 'on_message'
                    tbinfo = str(traceback.format_exc())
                    await self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)
        if message.channel.is_private:
            if self.bot.BotConfig.is_official_bot:
                # possible regex patterns for discord server invites
                patterns = [
                    '(https?:\/\/)?discord\.gg\/'
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
                    self.bot.DBLogs.edit_logs(before, after)
            elif before.channel.server and before.channel.server.id == \
                    "81812480254291968":
                if before.author.id == self.bot.user.id:
                    return
                elif before.channel.id == "153055192873566208":
                    return
                elif before.channel.id == "87382611688689664":
                    return
                else:
                    await self.bot.DBLogs.send_edit_logs(before,
                                                         after)
            else:
                if before.channel.is_private is not False:
                    return
                elif before.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.edit_logs(before, after)
        except Exception as e:
            funcname = 'on_message_edit'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_message_delete(self, message):
        """
        Bot Event.
        :param message: Message.
        :return: Nothing.
        """
        try:
            if message.channel.is_private is not False:
                if self.bot.BotConfig.logging:
                    self.bot.DBLogs.delete_logs(message)
            elif message.channel.server and message.channel.server.id == \
                    "81812480254291968":
                if message.author.id == self.bot.user.id:
                    return
                elif message.channel.id == "153055192873566208":
                    return
                elif message.channel.id == "87382611688689664":
                    return
                else:
                    await self.bot.DBLogs.send_delete_logs(self.bot, message)
            else:
                if message.channel.is_private is not False:
                    return
                elif message.channel.server.id == '95342850102796288':
                    return
                else:
                    if self.bot.BotConfig.logging:
                        self.bot.DBLogs.delete_logs(message)
        except Exception as e:
            funcname = 'on_message_delete'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_channel_delete(self, channel):
        """
        Bot Event.
        :param channel: Channels.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_delete:
            self.bot.DBLogs.onchanneldelete(channel)

    async def on_channel_create(self, channel):
        """
        Bot Event.
        :param channel: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_create:
            self.bot.DBLogs.onchannelcreate(channel)

    async def on_channel_update(self, before, after):
        """
        Bot Event.
        :param before: Channel.
        :param after: Channel.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_channel_update:
            self.bot.DBLogs.onchannelupdate(before, after)

    async def on_member_ban(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logbans:
                self.bot.DBLogs.onban(member)
            if member.server.id == "71324306319093760":
                await self.verify_cache_cleanup(member)
            for channel in member.server.channels:
                if channel.name == 'mod-log':
                    await self.bot.DBLogs.send_ban_logs(channel, member)
        except Exception as e:
            funcname = 'on_member_ban'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_member_unban(self, server, user):
        """
        Bot Event.
        :param server: Server.
        :param user: User.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.logunbans:
                self.bot.DBLogs.onunban(server, user)
            for channel in server.channels:
                if channel.name == 'mod-log':
                    await self.bot.DBLogs.send_unban_logs(channel, user)
        except Exception as e:
            funcname = 'on_member_unban'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

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
                        self.bot.DBLogs.onkick(member)
            except (discord.errors.HTTPException, discord.errors.Forbidden,
                    BotErrors.CommandTimeoutError):
                if self.bot.BotConfig.logkicks:
                    self.bot.DBLogs.onkick(member)
            if member.server and member.server.id == "71324306319093760":
                await self.verify_cache_cleanup_2(member)
        except Exception as e:
            funcname = 'on_member_remove'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_member_update(self, before, after):
        """
        Bot Event.
        :param before: Member.
        :param after: Member.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_member_update:
            self.bot.DBLogs.onmemberupdate(before, after)

    async def on_member_join(self, member):
        """
        Bot Event.
        :param member: Member.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_member_join:
                self.bot.DBLogs.onmemberjoin(member)
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
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_server_available(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_available:
            self.bot.DBLogs.onavailable(server)

    async def on_server_unavailable(self, server):
        """
        Bot Event.
        :param server: Servers.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_unavailable:
            self.bot.DBLogs.onunavailable(server)

    async def on_server_join(self, server):
        """
        Bot Event.
        :param server: Server.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_join:
            self.bot.DBLogs.onserverjoin(server)
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
            self.bot.DBLogs.onserverremove(server)
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
            self.bot.DBLogs.onserverupdate(before, after)

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
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

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
            self.bot.DBLogs.onserverrolecreate(role)

    async def on_server_role_delete(self, role):
        """
        Bot Event.
        :param role: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_delete:
            self.bot.DBLogs.onserverroledelete(role)

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
        self.bot.DBLogs.on_bot_error(funcname, tbinfo, None)

    async def on_server_role_update(self, before, after):
        """
        Bot Event.
        :param before: Role.
        :param after: Role.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_role_update:
            self.bot.DBLogs.onserverroleupdate(before, after)

    async def on_group_join(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_join:
                self.bot.DBLogs.ongroupjoin(channel, user)
        except Exception as e:
            funcname = 'on_group_join'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_group_remove(self, channel, user):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :return: Nothing.
        """
        try:
            if self.bot.BotConfig.log_group_remove:
                self.bot.DBLogs.ongroupremove(channel, user)
        except Exception as e:
            funcname = 'on_group_remove'
            tbinfo = str(traceback.format_exc())
            self.bot.DBLogs.on_bot_error(funcname, tbinfo, e)

    async def on_voice_state_update(self, before, after):
        """
        Bot Event.
        :param before: State.
        :param after: State.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_voice_state_update:
            self.bot.DBLogs.onvoicestateupdate(before, after)

    async def on_typing(self, channel, user, when):
        """
        Bot Event.
        :param channel: Channels.
        :param user: Users.
        :param when: Time.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_typing:
            self.bot.DBLogs.ontyping(channel, user, when)

    async def on_socket_raw_receive(self, msg):
        """
        Bot Event.
        :param msg: Message.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_receive:
            self.bot.DBLogs.onsocketrawreceive(msg)

    async def on_socket_raw_send(self, payload):
        """
        Bot Event.
        :param payload: Payload.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_socket_raw_send:
            self.bot.DBLogs.onsocketrawsend(payload)

    async def on_resumed(self):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_resumed:
            self.bot.DBLogs.onresumed()

    # new events (Since Discord.py v0.13.0+).

    async def on_server_emojis_update(self, before, after):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_server_emojis_update:
            self.bot.DBLogs.onserveremojisupdate(before, after)

    # added in Discord.py v0.14.3.

    async def on_reaction_add(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_add:
            self.bot.DBLogs.onreactionadd(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_remove:
            self.bot.DBLogs.onreactionremove(reaction, user)

    # added in Discord.py v0.15.0.

    async def on_reaction_clear(self, message, reactions):
        """
        Bot Event.
        :return: Nothing.
        """
        if self.bot.BotConfig.log_reaction_clear:
            self.bot.DBLogs.onreactionclear(message, reactions)

    # Helpers.

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
