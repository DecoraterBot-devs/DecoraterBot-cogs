### Plugin Commands for DecoraterBot

Commands are usually using the `::` prefix.

List of current Plugin Commands.

|   	| Plugin Commands (plugins/credits.py)	|
|:---------------:	|:------------------------------------------------------------------------------------------------:	|
| ``::credits``	| Gives Daily Credits even if the Tatsumaki bot is present in the server this command is sent from.	|
| ``::balance``	| Gives your current Credit Balance.	|
| ``::givecredits <mention user(required)> <amount(required)>``	| Transfers Credits from you to another user.	|

|   	| Plugin Commands (plugins/moderation.py)	|
|:---------------:	|:------------------------------------------------------------------------------------------------:	|
| ``::prune <number of messages to remove>``	| Prune a specific number of messages. Max is 100 due to Ratelimits. (Servers only)	|
| ``::kick <mention person here>``	| Kicks the User mentioned.	|
| ``::ban <mention person here>``	| Bans the User mentioned.	|
| ``::softban <mention person here>``	| Bans and then Immediately Unbans the user mentioned. (prune kick)	|
| ``::warn <mention(s)> <reason>``	| Warns a user or user(s) mentioend for a particular reason provided. (Does not work yet) |
| ``::mute <mention>``	| Mutes an user mentioned for a certain amount of time. Requires a role named ``Muted`` to work. (Does not work yet) |
| ``::clear``	| Clears all messages from bot within a 100 message limit.	|

|   	| Plugin Commands (plugins/voice.py)	|
|:--------------------------------------------:	|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|
| ``::JoinVoiceChannel``	| Allows the bot to Join a Voice Channel. (You must be in a Voice Channel for it to work)	|
| ``::play <youtube url here>``	| URL or Serch Term for a video to Play. Note: This does not support youtube Playlists currently.	|
| ``::pause``	| Pauses any playing Youtube Video/Audio/Music.	|
| ``::unpause``	| Resumes any paused Youtube Video/Audio/Music.	|
| ``::stop``	| Stops any playing Youtube Video/Audio/Music.	|
| ``::move``	| Moves the bot to a Voice Channel that you are in or moved to yourself.	|
| ``::LeaveVoiceChannel``	| Makes the bot leave the Voice Channel it is in.	|
| ``::Playlist``	| Shows the current Playlist entries.	|
| ``::vol (int value somewhere between 0~200)``	| Sets the Volume of the playing Youtube Video/Audio/Music.	|

<!-- Some commands are commented out here and in the source code until I think more about them.
I have to decide if I want to officially remove them or keep them and modify them. -->

|   	| Plugin Commands (plugins/commands.py)	|
|:------:	|:-:	|
| ``::attack <mention user>``	| Attacks the user mentioned.	|
| ``::coin``	| Flips an coin that can land on Heads or Tails.	|
| ``::commands``	| Links to the bot's commands (this file).	|
| ``::help``	| Alias to ``::commands``.	|
| ``::AgarScrub``	| Links to an image.	|
| ``::botban <mention user>``	| Bans a specific user from using the bot.	|
| ``::botunban <mention user>``	| Unbans a specific user for them to the bot.	|
| ``::discrim``	| Searches other servers for people with your same discriminator.	|
| ``::kill``	| Kills you with an randomly generated a kill message. (Works in PM and servers)	|
| ``::changelog``	| Bot information and command changes. (Works in PM and servers)	|
| ``::source``	| Shows GitHub Repositories. (Works in PM and servers)	|
| ``::game <'string here'> \| type=<1 for Twitch or 2 for Youtube (Soon™)>``	| Changes game status. (Bot owner only) (Works in PM and servers)	|
| ``::debug``	| Debugs Python Code. (Bot owner only) (Works in PM and servers)	|
| ``::eval``	| Evaluates Python Code without Subproccessing the Python Interpreter. (Bot owner only) (Works in PM and servers)	|
| ``::meme <picture (required)> \| <top text (required)> \| <bottom text (required)>``	| Gives a meme with the text you provide. meme picture list can be found [here](http://pastebin.com/gCL2jMEL). (BooBot's but it works for this too) You can also do things like ``::meme [mention someone here] \| [top text] \| [bottom text]``	|
| ``::remgame``	| Removes any game from the bot's status. (Bot owner only)	|
| ``::join <invite url or code>``	| For Joining Servers, However with Official API it does not work so that is why Credentials has a ``True`` and a ``False`` Option for if it is a bot account or not. If it is set to ``True`` it will send you a url to validate it to join the server via [OAuth2](http://oauth.net/2/).	|
| ``::update``	| Command that says that the bot has updated. Probably should remove this due to spamming of it is possible?	|
| ``::say <whatever you want here>``	| Makes the bot Say whatever you want. Note: You cannot have ``::`` in this nor any Mentions to prevent any abuse of the API.	|
| ``::type``	| Makes the bot send a ``typing`` status to the channel the command was sent from.	|
| ``::pyversion``	| Makes the bot Reply with the Version of the Python Interpreter used as well as the bits of it. (32 or 64 bit versions)	|
| ``::Libs``	| Makes the bot Reply with the Libraries used. (Not Currently up to date)	|
| ``::userinfo <mention user (optional if you want to see your own info)>``	| Shows your or the person you mentioned user information.	|
| ``::ignorechannel``	| Ignores the channel that this command was sent from.	|
| ``::unignorechannel``	| Allows the bot to listen to commands from a Ignored Channel and Remvoes it from the ``Ignore`` List.	|
| ``::as``	| Changes bot's avatar to Asura's image. (Bot owner only)	|
| ``::rs``	| Changes bot's avatar to Rune Slayer's image. (Bot owner only)	|
| ``::stats``	| Gives the bot's current stats including the number of servers it is currently in.	|
| ``::ai``	| Changes bot's avatar to Aisha's base image. (Bot owner only)	|
| ``::lk``	| Changes bot's avatar to Lord Knight's image. (Bot owner only)	|
| ``::vp``	| Changes bot's avatar to Void Princess's image. (Bot owner only)	|
| ``::ws``	| Changes bot's avatar to Wind Sneeker's image. (Bot owner only)	|
| ``::tinyurl <URL to shorten here>``	| Makes the bot shorten the URL Provided. (Supports ``<`` and ``>`` between the URL to excape embedding of it with [oEmbed](http://oembed.com/))	|
| ``::listservers`` | Lists the names of the servers that the bot sees you in. |
<!--
| ``::color ::pink/::brown <role name here>``	| Changes the Colors of a Role. (Was Originally a Testing Command) (Servers only)	|
| ``::giveme``	| Old command that should me removed or changed to be for any and all servers.	|
| ``::remove``	| Old command that should me removed or changed to be for any and all servers.	|
-->

|   	| Plugin Commands (plugins/corecommands.py)	|
|:------:	|:-:	|
| ``::uptime``	| Makes the bot Reply withh the uptime of the bot's process.	|
| ``::load <plugin name>``	| Allows loading of bot plugins. (Bot owner only)	|
| ``::unload <plugin name>``	| Allows unloading of bot plugins. (Bot owner only)	|
| ``::reload <plugin name>``	| Allows reloading of bot plugins. (Bot owner only)	|
| ``::install <plugin name>``	| Allows installing of bot plugins. (Bot owner only)(not finished yet)	|
| ``::uninstall <plugin name>``	| Allows uninstalling bot plugins. (Bot owner only)(not finished yet)	|


### Plugin Events for DecoraterBot

Most cogs can register their own events. This means they can listen for their own custom stuff.

## plugins/logs.py

Here is a list of the Discortd.py Events that are used in this plugin as well as what they are used for.
Note: Events that use Optional Logs are Controlled by ``\\resources\\ConfigData\\Credentials.json``

Documentation on Setting it up is **not** Complete and is present in the Core Repository for the bot located [here](https://github.com/DecoraterBot-devs/DecoraterBot).

Note: *At any moment in time some of the events can be removed or split into new events when breaking changes to discord.py happens. This means that when that does happen a new release version of this plugin should be released sometime soon after.*

| Event	| Usage	|
|:--------------------------:	|:----------------------------------------------------------------------------------------------------------------------:	|
| ``on_message``	| Commands. This is how the Bot Actually Responds to the commands. Also has Built in Error Handler for this Event. Also has optional logs.	|
| ``on_message_delete``	| Optional Logs & Built in Error Handler.	|
| ``on_message_edit``	| Optional Logs & Built in Error Handler.	|
| ``on_channel_delete``	| Optional Logs.	|
| ``on_channel_create``	| Optional Logs.	|
| ``on_channel_update``	| Optional Logs.	|
| ``on_member_ban``	| Optional Logs & Cheese.lab verifications (removing users from verify cache list)	|
| ``on_member_unban``	| Optional Logs & Built in Error Handler.	|
| ``on_member_remove``	| Optional Logs & Cheese.lab verifications (removing users from verify cache list)	|
| ``on_member_update``	| Optional Logs.	|
| ``on_member_join``	| Optional Logs & Cheese.lab verification stuff (Old).	|
| ``on_server_available``	| Optional Logs.	|
| ``on_server_unavailable``	| Optional Logs.	|
| ``on_server_join``	| Optional Logs.	|
| ``on_server_remove``	| Optional Logs.	|
| ``on_server_update``	| Optional Logs.	|
| ``on_server_role_create``	| Optional Logs.	|
| ``on_server_role_delete``	| Optional Logs.	|
| ``on_server_role_update``	| Optional Logs.	|
| ``on_group_join``	| Optional Logs.	|
| ``on_group_remove``	| Optional Logs.	|
| ``on_error``	| Optional Logs.	|
| ``on_voice_state_update``	| Optional Logs.	|
| ``on_typing``	| Optional Logs.	|
| ``on_socket_raw_receive``	| Optional Logs.	|
| ``on_socket_raw_send``	| Optional Logs.	|
| ``on_ready``	| Bot Status messages on 2 Servers & Initial Streaming Status saying to ``type ::commands for info``.	|
| ``on_resumed``	| Optional Logs.	|
| ``on_server_emojis_update``	| Optional Logs.	|
| ``on_reaction_add``	| Optional Logs.	|
| ``on_reaction_remove``	| Optional Logs.	|
| ``on_reaction_clear``	| Optional Logs.	|


