from discord.ext import commands
from discord import utils
from tools.database import UserNotFound

import discord

from tools import database as db

import config as cfg


class LevelSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Level system
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!'): return
        if message.author.bot: return

        author = message.author
        author_id = author.id

        try:
            user = db.get_user(author_id)
            current_exp = user['experience']
            current_lvl = new_lvl = user['level']
            
            new_exp = current_exp + 1

            # Lvlup
            if new_exp >= 100:
                new_lvl = current_lvl + 1
                new_exp = 0

            # Rewarding system
            for i in cfg.LEVEL_REWARDS:
                if i[0] == current_lvl:
                    role_name = i[1]
                    role = utils.get(author.guild.roles, name=i[1])
                    if not author.roles.__contains__(role):
                        await author.add_roles(role)
                    
                    break
            
            # Updates entry in db
            db.update_user(author_id, level=new_lvl, experience=new_exp)
        except UserNotFound:
            # Adds user if not found
            db.add_user(author_id)

    @commands.command(name='rank')
    async def get_rank(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.message.author

        try:
            user = db.get_user(member.id)
            lvl = user['level']
            exp = user['experience']

            await ctx.send(f'Level: {lvl}; Exp: {exp}')
        except UserNotFound:
            await ctx.send('**:x: Юзер не найден...**')

    # TODO: Complete LevelSystemCog.set_lvl
    @commands.command(name='set_lvl')
    async def set_lvl(self, ctx, member: discord.Member, lvl: int):        
        try:
            db.get_user(member.id)
            db.update_user(member.id, level=lvl)
        except UserNotFound:
            db.add_user(member.id)


def setup(bot):
    bot.add_cog(LevelSystemCog(bot))
