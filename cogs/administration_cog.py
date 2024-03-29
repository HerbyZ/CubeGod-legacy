from discord.ext import commands

import os
import sys

from tools.log import log

import config as cfg


class AdministrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Restarts bot
    @commands.command(name='restart')
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        await ctx.message.delete()
        await log(self.bot, f'Bot was restarted.')
        os.system('cls')
        os.system('start.cmd')
        sys.exit(0)

    # Clears console
    @commands.command(name='clear_console')
    @commands.has_permissions(administrator=True)
    async def clear_console(self, ctx):
        os.system('cls')

    # Deletes entry with specified member_id from db
    @commands.command(name='delete_from_db')
    @commands.has_permissions(administrator=True)
    async def delete_from_db(self, ctx, member_id: int):
        author = ctx.message.author
        if not author.bot:
            await ctx.send('Команда в разработке...')

    @commands.command(name='unload_cog')
    @commands.has_permissions(administrator=True)
    async def unload_cog(self, ctx, extension_name):
        extension_name = extension_name.lower()

        if not extension_name.endswith('_cog'):
            extension_name += '_cog'

        try:
            author = ctx.message.author
            log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)

            self.bot.unload_extension(f'cogs.{extension_name}')
            await ctx.message.delete()
            await log_channel.send(f'{author.mention} has unloaded cog {extension_name}.')
        except commands.ExtensionNotLoaded:
            await ctx.send('**:x: Extension is not loaded.**')
        except Exception as e:
            log(self.bot, repr(e))

    @commands.command(name='load_cog')
    @commands.has_permissions(administrator=True)
    async def load_cog(self, ctx, extension_name: str):
        extension_name = extension_name.lower()
        
        if not extension_name.endswith('_cog'):
            extension_name += '_cog'

        try:
            log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)
            author = ctx.message.author

            self.bot.load_extension(f'cogs.{extension_name}')
            await ctx.message.delete()
            await log_channel.send(f'{author.mention} has loaded cog {extension_name}.')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send('**:x: Extension already loaded.**')
        except commands.ExtensionNotFound:
            await ctx.send('**:x: Extension not found.**')
        except Exception as e:
            log(self.bot, repr(e))

    @commands.command(name='reload_cog')
    @commands.has_permissions(administrator=True)
    async def reload_cog(self, ctx, extension_name):
        extension_name = extension_name.lower()
        
        if not extension_name.endswith('_cog'):
            extension_name += '_cog'

        try:
            log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)
            author = ctx.message.author

            self.bot.reload_extension(f'cogs.{extension_name}')
            await ctx.message.delete()
            await log_channel.send(f'{author.mention} has reloaded cog {extension_name}.')
        except commands.ExtensionNotLoaded:
            await ctx.send('**:x: Extension is not loaded.**')
        except commands.ExtensionNotFound:
            await ctx.send('**:x: Extension not found.**')
        except Exception as e:
            log(self.bot, repr(e))


def setup(bot):
    bot.add_cog(AdministrationCog(bot))
