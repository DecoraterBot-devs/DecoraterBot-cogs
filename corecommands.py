# coding=utf-8
"""
Core Commands plugin for DecoraterBot.
"""
# from discord import app_commands
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

    # @app_commands.command(name='load', description='Loads a specific cog into the bot (Bot owner only).')
    # @app_commands.describe(module='The cog to load.')
    @commands.command(name='load', pass_context=True, no_pm=True)
    @commands.is_owner()
    # @Checks.is_bot_owner()
    # async def load_command(self, interaction: discord.Interaction, module: str):
    async def load_command(self, ctx: commands.Context, module: str):
        """
        Loads a specific cog into the bot (Bot owner only).
        """
        ret = await ctx.bot.load_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Loading')
            await ctx.send(reload_data)
            # await interaction.response.send_message(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Loaded {module}.'
            await ctx.send(message_data)
            # await interaction.response.send_message(message_data)

    # @app_commands.command(name='unload', description='Unloads a specific cog from the bot (Bot owner only).')
    # @app_commands.describe(module='The cog to unload.')
    @commands.command(name='unload', pass_context=True, no_pm=True)
    @commands.is_owner()
    # @Checks.is_bot_owner()
    # async def unload_command(self, interaction: discord.Interaction, module: str):
    async def unload_command(self, ctx: commands.Context, module: str):
        """
        Unloads a specific cog from the bot (Bot owner only).
        """
        ret = await ctx.bot.unload_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Unloading')
            await ctx.send(reload_data)
            # await interaction.response.send_message(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Unloaded {module}.'
            await ctx.send(message_data)
            # await interaction.response.send_message(message_data)

    # @app_commands.command(name='reload', description='Reloads a specific cog on the bot (Bot owner only).')
    # @app_commands.describe(module='The cog to reload.')
    @commands.command(name='reload', pass_context=True, no_pm=True)
    @commands.is_owner()
    # @Checks.is_bot_owner()
    # async def reload_command(self, interaction: discord.Interaction, module: str):
    async def reload_command(self, ctx: commands.Context, module: str):
        """
        Reloads a specific cog on the bot (Bot owner only).
        """
        ret = await ctx.bot.reload_bot_extension(module)
        if ret is not None:
            reload_data = self.reload_command_data[1].format(
                ret).replace('Reloading', 'Reloading')
            await ctx.send(reload_data)
            # await interaction.response.send_message(reload_data)
        else:
            message_data = f'{self.reload_command_data[0]} Reloaded {module}.'
            await ctx.send(message_data)
            # await interaction.response.send_message(message_data)

    # @app_commands.command(name='sync', description='Syncs all of the bot's global commands (Bot owner only).')
    @commands.command(name='sync', pass_context=True, no_pm=True)
    @commands.is_owner()
    # @Checks.is_bot_owner()
    # async def sync_command(self, interaction: discord.Interaction):
    async def sync_command(self, ctx: commands.Context):
        """
        Syncs all of the bot's global commands (Bot owner only).
        """
        # await interaction.response.defer(thinking=True)
        synced = await ctx.bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands globally.')
        # await interaction.followup.send(f'Synced {len(synced)} commands globally.')

    @load_command.error
    @unload_command.error
    @reload_command.error
    # async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # if isinstance(error, app_commands.CheckFailure):
        if isinstance(error, commands.NotOwner):
            await ctx.send(self.reload_command_data[2])
            # await interaction.response.send_message(self.reload_command_data[2])


async def setup(bot):
    """
    DecoraterBot's Core Commands Plugin.
    """
    await bot.add_cog(CoreCommands())
