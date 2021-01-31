from discord.ext import commands, tasks
from discord import utils

import discord

from tools import database as db
from tools.log import log

import config as cfg


class EventSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_id = 731877822930354268
        self.roles = {
            '❤️': 731862587683242064,
            '🎮': 731876639255822386,
            '🍩': 731877205306507274
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = payload.member

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=self.roles[emoji])

            if not member.roles.__contains__(role) and message.id == self.post_id:
                await member.add_roles(role)
            else:
                await message.remove_reaction(payload.emoji, member)

        except KeyError as e:
            print(f'[ERROR]: Unknown emoji on role-reaction post')
        except Exception as e:
            await log(self.bot, repr(e))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(cfg.NET_CUBE_GUILD_ID)
        member = utils.get(guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=self.roles[emoji])

            if message.id == self.post_id:
                await member.remove_roles(role)

        except KeyError as e:
            print(f'[ERROR]: Unknown emoji on role-reaction post')
        except Exception as e:
            await log(self.bot, repr(e))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(cfg.NEW_USERS_CHANNEL_ID)
        role = utils.get(member.guild.roles, name='Souls')

        db.add_user(member.id)

        await member.add_roles(role)
        await channel.send(
            f'Пользователь {member.mention} присоединился к серверу, был добавлен в базу и получил роль Souls.'
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(cfg.NEW_USERS_CHANNEL_ID)
        await channel.send(
            f'Пользователь {member.mention} покинул сервер.\n' \
            f'Чтобы удалить пользователя из базы, используйте\n!delete_from_db {member.id}.'
        )


def setup(bot):
    bot.add_cog(EventSystemCog(bot))
