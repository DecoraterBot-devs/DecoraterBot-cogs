# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
from discord.ext import commands


class CoreCommands(commands.Cog):
    """
    Core Commands class for DecoraterBot.
    """
    def __init__(self):
        self.reload_command_data = [
            ':ok:',
            'Reloading Plugin Failed.\n```py\n{0}\n```',
            'Sorry, Only my owner can load, unload, and reload modules.']

    @commands.command(name='load', pass_context=True, no_pm=True)
    @commands.is_owner()
    async def load_command(self, ctx: commands.Context, module: str):
        """
        Loads a specific cog into the bot (Bot owner only).
        """
        ret = await ctx.bot.load_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Loading')
            await ctx.send(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Loaded {module}.'
            await ctx.send(message_data)

    @commands.command(name='unload', pass_context=True, no_pm=True)
    @commands.is_owner()
    async def unload_command(self, ctx: commands.Context, module: str):
        """
        Unloads a specific cog from the bot (Bot owner only).
        """
        ret = await ctx.bot.unload_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Unloading')
            await ctx.send(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Unloaded {module}.'
            await ctx.send(message_data)

    @commands.command(name='reload', pass_context=True, no_pm=True)
    @commands.is_owner()
    async def reload_command(self, ctx: commands.Context, module: str):
        """
        Reloads a specific cog on the bot (Bot owner only).
        """
        ret = await ctx.bot.reload_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Reloading')
            await ctx.send(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Reloaded {module}.'
            await ctx.send(message_data)

    @commands.command(name='sync', pass_context=True, no_pm=True)
    @commands.is_owner()
    async def sync_command(self, ctx: commands.Context):
        """
        Syncs all of the bot's global commands (Bot owner only).
        """
        synced = await ctx.bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands globally.')

    @load_command.error
    @unload_command.error
    @reload_command.error
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            await ctx.send(self.reload_command_data[2])


async def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    await bot.add_cog(CoreCommands())
