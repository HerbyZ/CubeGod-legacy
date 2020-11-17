from discord.ext import commands

import discord

import config as cfg


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = cfg.DATABASE

    # Отправляет сообщение в указанный канал от лица бота
    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, channel: discord.TextChannel, *, text):
        channel = ctx.message.channel if channel is None else channel
        log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)
        author = ctx.message.author

        await ctx.message.delete()
        await channel.send(text)
        await log_channel.send(
            f'{author.mention} отправил сообщение от лица бота в канал {channel.mention}.\nТекст:{text}'
        )

    # Очищает сообщения в указанном канале, если он не указан, очищает в текущем
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100, channel: discord.TextChannel = None):
        log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)
        author = ctx.message.author
        channel = ctx.message.channel if channel is None else channel

        await ctx.message.delete()
        await channel.purge(limit=amount)

        await log_channel.send(f'Пользователь {author.mention} очистил сообщения ({amount}) в канале {channel.mention}')

    # Выгоняет пользователя с сервера
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        author = ctx.message.author
        log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)

        try:
            await member.kick(reason=reason)
            await ctx.message.delete()
            await log_channel.send(f'Пользователь {member.mention} был изгнан с сервера пользователем {author}.')
        except commands.MissingRequiredArgument:
            await ctx.send(':x: Вы не указали пользователя. Для более подробной информации введите !help kick')

    # Банит пользователя на сервере
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        author = ctx.message.author
        log_channel = self.bot.get_channel(cfg.LOG_CHANNEL_ID)

        try:
            await member.ban(reason=reason)
            await ctx.message.delete()
            await log_channel.send(f'Пользователь {member.mention} был изгнан с сервера пользователем {author}.')
            self.db.ban_user(member.id, reason)  # Добавление юзера в таблицу забаненных в базе данных
        except commands.MissingRequiredArgument:
            await ctx.send(':x: Вы не указали пользователя. Для более подробной информации введите !help ban')

    # Репорт
    @commands.command(name='report')
    @commands.cooldown(1, 120, commands.BucketType.member)
    async def report(self, ctx, against: discord.Member, *, text):
        report_channel = self.bot.get_channel(cfg.REPORT_CHANNEL_ID)
        author = ctx.message.author
        embed = discord.Embed(
            title=f'Report against {against.name}#{against.discriminator}',
            colour=discord.Colour.red()
        )
        embed.add_field(name='Text', value=text)
        embed.set_footer(
            text=f'Author - {author.name}#{author.discriminator}',
            icon_url=author.avatar_url
        )

        await ctx.message.delete()
        await report_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
