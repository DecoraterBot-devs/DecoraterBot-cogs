# coding=utf-8
"""
nsfw plugin for DecoraterBot.
"""
from discord.ext import commands
import random
import nsfw_dl


class NSFWCommands:
    """
    NSFW Commands Plugin Class.
    """
    def __init__(self, bot):
        self.image = None
        self.bot = bot
        self.command_list = ['rule34']
        self.nsfw_text = self.bot.PluginTextReader(
            file='nsfw.json')

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.add_commands(self.command_list)

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.remove_commands(self.command_list)

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
                    searchterm, self.bot.http.session)
            except nsfw_dl.errors.NoResultsFound:
                self.image = None
                imageerr = self.nsfw_text['nsfw_plugin_data'][0]
            if self.image is -1:
                await self.bot.send_message(
                    ctx.message.channel,
                    content=self.nsfw_text['nsfw_plugin_data'][1])
            else:
                if self.image is not None:
                    await self.bot.send_message(
                        ctx.message.channel,
                        content='http:' + random.choice(self.image))
                else:
                    if imageerr is not None:
                        await self.bot.send_message(ctx.message.channel,
                                                    content=imageerr)
                    else:
                        await self.bot.send_message(
                            ctx.message.channel,
                            content=self.nsfw_text['nsfw_plugin_data'][2])
        else:
            self.image = await nsfw_dl.rule34_random(self.bot.http.session)
            if self.image is not None:
                await self.bot.send_message(ctx.message.channel,
                                            content='http:' + self.image)
            else:
                await self.bot.send_message(ctx.message.channel,
                                            content=self.nsfw_text[
                                                        'nsfw_plugin_data'
                                                    ][2])


def setup(bot):
    """
    DecoraterBot's NSFW Plugin.
    """
    new_cog = NSFWCommands(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
