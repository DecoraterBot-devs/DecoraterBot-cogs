# coding=utf-8
"""
credits Plugin for DecoraterBot.
"""
import traceback

from discord.ext import commands


class Credits:
    """
    Credits Commands Plugin Class.
    """
    def __init__(self, bot):
        self.bot = bot
        # self.command_list = ['credits', 'givecredits', 'balance']
        self.credits_text = self.bot.PluginTextReader(
            file='credits.json')

    # def botcommand(self):
    #     """Stores all command names in a dictionary."""
    #     self.bot.add_commands(self.command_list)

    # def __unload(self):
    #     """
    #     Clears registered commands.
    #     """
    #     self.bot.remove_commands(self.command_list)

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
                    (self.credits_text['credits_plugin_data'][0]
                    ).format(
                        ctx.message.author.name))
        except Exception:
            await self.bot.send_message(
                    ctx.message.channel,
                    (self.credits_text['credits_plugin_data'][3]
                    ).format(traceback.format_exc()))

    @commands.command(name='givecredits', pass_context=True)
    async def givecredits_command(self, ctx):
        """
        ::givecredits Command for DecoraterBot.
        """
        creditnum = ctx.message.content
        for mention in ctx.message.mentions:
            if mention.nick is not None:
                creditnum = creditnum.replace(
                    '<@!{0}> '.format(mention.id), '')
            else:
                creditnum = creditnum.replace(
                    '<@{0}> '.format(mention.id), '')
        creditnum = int(creditnum[len(ctx.prefix + 'givecredits'):].strip())
        current_credits = 0
        current_credits2 = 0
        try:
            current_credits = self.bot.credits.getcredits(
                str(ctx.message.author.id), 'credits')
        except (KeyError, TypeError):
            pass
        try:
            current_credits2 = self.bot.credits.getcredits(
                str(ctx.message.mentions[0].id), 'credits')
        except (KeyError, TypeError):
            pass
        if creditnum > -1:
            if current_credits > creditnum:
                try:
                    self.bot.credits.setcredits(
                        str(ctx.message.author.id), 'credits',
                        current_credits - creditnum)
                    self.bot.credits.setcredits(
                        str(ctx.message.mentions[0].id), 'credits',
                        current_credits2 + creditnum)
                    await self.bot.send_message(
                            ctx.message.channel,
                            (self.credits_text['credits_plugin_data'][1]
                            ).format(ctx.message.author.name, creditnum,
                            ctx.message.mentions[0].name))
                except Exception:
                    await self.bot.send_message(
                            ctx.message.channel,
                            (self.credits_text['credits_plugin_data'][3]
                            ).format(traceback.format_exc()))
            else:
                await self.bot.send_message(
                    ctx.message.channel,
                    (self.credits_text['credits_plugin_data'][5]
                    ).format(creditnum,
                             ctx.message.mentions[0].name))
        else:
            await self.bot.send_message(
                ctx.message.channel,
                (self.credits_text['credits_plugin_data'][4]))

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
                    self.credits_text['credits_plugin_data'][2].format(
                        ctx.message.author.name, current_credits))
        except Exception:
            await self.bot.send_message(
                    ctx.message.channel,
                    (self.credits_text['credits_plugin_data'][3]
                    ).format(traceback.format_exc()))


def setup(bot):
    """
    DecoraterBot's Credits Plugin.
    """
    new_cog = Credits(bot)
    # new_cog.botcommand()
    bot.add_cog(new_cog)
