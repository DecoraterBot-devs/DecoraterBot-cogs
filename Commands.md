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
| ``::game <'string here'> \| type=<1 for Twitch or 2 for Youtube (Soon™)>``	| Changes game status. (Works in PM and servers)	|
| ``::debug``	| Debugs Python Code. (Bot owner only) (Works in PM and servers)	|
| ``::eval``	| Evaluates Python Code without Subproccessing the Python Interpreter. (Bot owner only) (Works in PM and servers)	|
| ``::color ::pink/::brown <role name here>``	| Changes the Colors of a Role. (Was Originally a Testing Command) (Servers only)	|
| ``::meme <picture (required)> \| <top text (required)> \| <bottom text (required)>``	| Gives a meme with the text you provide. meme picture list can be found [here](http://pastebin.com/gCL2jMEL). (BooBot's but it works for this too) You can also do things like ``::meme [mention someone here] \| [top text] \| [bottom text]``	|
| ``::remgame``	| Removes any game from the bot's status.	|
| ``::join <invite url or code>``	| For Joining Servers, However with Official API it does not work so that is why Credentials has a ``True`` and a ``False`` Option for if it is a bot account or not. If it is set to ``True`` it will send you a url to validate it to join the server via [OAuth2](http://oauth.net/2/).	|
| ``::update``	| Command that says that the bot has updated. Probably should remove this due to spamming of it is possible?	|
| ``::say <whatever you want here>``	| Makes the bot Say whatever you want. Note: You cannot have ``::`` in this nor any Mentions to prevent any abuse of the API.	|
| ``::type``	| Makes the bot send a ``typing`` status to the channel the command was sent from.	|
| ``::pyversion``	| Makes the bot Reply with the Version of the Python Interpreter used as well as the bits of it. (32 or 64 bit versions)	|
| ``::Libs``	| Makes the bot Reply with the Libraries used. (Not Currently up to date)	|
| ``::userinfo <mention user (optional if you want to see your own info)>``	| Shows your or the person you mentioned user information.	|
| ``::ignorechannel``	| Ignores the channel that this command was sent from.	|
| ``::unignorechannel``	| Allows the bot to listen to commands from a Ignored Channel and Remvoes it from the ``Ignore`` List.	|
| ``::as``	| Changes bot's avatar to Asura's image.	|
| ``::rs``	| Changes bot's avatar to Rune Slayer's image.	|
| ``::stats``	| Gives the bot's current stats including the number of servers it is currently in.	|
| ``::ai``	| Changes bot's avatar to Aisha's base image.	|
| ``::lk``	| Changes bot's avatar to Lord Knight's image.	|
| ``::vp``	| Changes bot's avatar to Void Princess's image.	|
| ``::ws``	| Changes bot's avatar to Wind Sneeker's image.	|
| ``::tinyurl <URL to shorten here>``	| Makes the bot shorten the URL Provided. (Supports ``<`` and ``>`` between the URL to excape embedding of it with [oEmbed](http://oembed.com/))	|
| ``::giveme``	| Old command that should me removed or changed to be for any and all servers.	|
| ``::remove``	| Old command that should me removed or changed to be for any and all servers.	|

|   	| Plugin Commands (plugins/corecommands.py)	|
|:------:	|:-:	|
| ``::uptime``	| Makes the bot Reply withh the uptime of the bot's process.	|
| ``::load <plugin name>``	| Allows loading of bot plugins. (Bot owner only)	|
| ``::unload <plugin name>``	| Allows unloading of bot plugins. (Bot owner only)	|
| ``::reload <plugin name>``	| Allows reloading of bot plugins. (Bot owner only)	|
| ``::install <plugin name>``	| Allows installing of bot plugins. (Bot owner only)(not finished yet)	|


