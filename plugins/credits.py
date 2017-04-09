# coding=utf-8
"""
credits plugin for DecoraterBot.
"""
import traceback

from discord.ext import commands


class Credits:
    """
    Credits Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        self.command_list = ['credits', 'givecredits', 'balance']

    def botcommand(self):
        """Stores all command names in a dictionary."""
        self.bot.add_commands(self.command_list)

    def __unload(self):
        """
        Clears registered commands.
        """
        self.bot.remove_commands(self.command_list)

    @commands.command(name='credits', pass_context=True)
    async def credits_command(self, ctx):
        """
        ::credits Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            self.bot.credits.setcredits(
                str(ctx.message.author.id), 'credits', current_credits + 500)
            await self.bot.send_message(
                    ctx.message.channel,
                    ":atm:  |  {0}, you received your :dollar: 500 daily "
                    "credits!".format(
                        ctx.message.author.name))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))

    @commands.command(name='givecredits', pass_context=True)
    async def givecredits_command(self, ctx):
        """
        ::givecredits Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            self.bot.credits.setcredits(
                str(ctx.message.author.id), 'credits',
                current_credits + 5000000)
            await self.bot.send_message(
                    ctx.message.channel,
                    ":atm:  |  {0}, you received :dollar: 5000000 "
                    "credits!".format(ctx.message.author.name))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))

    @commands.command(name='balance', pass_context=True)
    async def balance_command(self, ctx):
        """
        ::balance Command for DecoraterBot.
        """
        try:
            current_credits = 0
            try:
                current_credits = self.bot.credits.getcredits(
                    str(ctx.message.author.id), 'credits')
            except (KeyError, TypeError):
                pass
            await self.bot.send_message(
                    ctx.message.channel,
                    "{0}, you have {1} credits!".format(
                        ctx.message.author.name, current_credits))
        except Exception as ex:
            str(ex)
            await self.bot.send_message(
                    ctx.message.channel,
                    "Error: ```py\n{0}```".format(traceback.format_exc()))


def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    new_cog = Credits(bot)
    new_cog.botcommand()
    bot.add_cog(new_cog)
