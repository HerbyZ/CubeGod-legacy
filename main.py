from discord.ext import commands, tasks

import discord
import os

import config as cfg


class CubeGod(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.launch()

    def launch(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('cog.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

        self.run(cfg.BOT_TOKEN)
    
    async def on_ready(self):
        self.dynamic_status.start()
        print(f'Logged in as "{self.user}"')

    async def on_command_error(self, ctx, error):
        author = ctx.message.author
        await ctx.message.delete()

        if isinstance(error, commands.CommandNotFound):
            await author.send(
                f'**:x: Команды {ctx.message.content} не существует.**' \
                f'\n**Для получения списка команд, введите !help.**'
            )
        elif isinstance(error, commands.MissingPermissions):
            await author.send(f'**:x: У вас нет прав на использование команды {ctx.message.content}**')
        elif isinstance(error, commands.MemberNotFound):
            await author.send(f'**:x: Пользователь не найден. Проверьте формат ввода никнейма, должно быть: ник#тэг**')          
        else:
            print(repr(error))

    @tasks.loop(seconds=10)
    async def dynamic_status(self):
        await self.change_presence(
            activity=discord.Game(name=next(cfg.BOT_STATUSES)),
            status=discord.Status.online
        )


if __name__ == '__main__':
    CubeGod(command_prefix='!')
