import sqlite3
import os

import config as cfg


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(cfg.BASE_DIR, 'db.sqlite3'))
        self.cursor = self.connection.cursor()

    def add_user(self, discord_id: int):
        """Adds user to Users table"""
        query = f'INSERT INTO Users (DiscordId) VALUES ({discord_id})'
        self.cursor.execute(query)
        self.connection.commit()

    def update_user(self, discord_id: int, **kwargs):
        """Updates data in kwargs for entry with DiscordId = discord_id"""
        if not kwargs:
            raise ValueError('No data about user.')

        items = ''
        for key, value in kwargs.items():
            items += f'{key}="{value}",'

        query = f'UPDATE Users SET {items[:-1]} WHERE DiscordId = {discord_id}'
        self.cursor.execute(query)

        self.connection.commit()

    def ban_user(self, discord_id: int, reason=None):
        """Adds user to BannedUsers table."""
        query = f'INSERT INTO BannedUsers (DiscordId, BanReason) VALUES (\'{discord_id}\', \'{reason}\')'
        self.cursor.execute(query)
        self.connection.commit()

    def unban_user(self, discord_id: int):
        query = f'DELETE FROM Users WHERE DiscordId = {discord_id}'
        self.cursor.execute(query)
        self.connection.commit()

    def get_users(self, **kwargs):
        """Returns all db entries with specified arguments."""
        if not kwargs:
            raise ValueError('No data about user.')

        items = ''
        for key, value in kwargs.items():
            items += f'{key}="{value}" AND '

        query = f'SELECT * FROM Users WHERE {items[:-5]}'
        self.cursor.execute(query)

        data = self.cursor.fetchall()

        if len(data) == 0:
            raise UserNotFound(f'Users with specified arguments not found. Query: "{query}"')

        return data

    def get_user(self, discord_id):
        """Returns entry with specified discord id."""
        query = f'SELECT * FROM Users WHERE DiscordId={discord_id}'
        self.cursor.execute(query)

        data = self.cursor.fetchall()
        if len(data) == 0:
            raise UserNotFound(f'User with discord id {discord_id} not found. Query: "{query}"')

        return data[0]

    def delete_user(self, discord_id):
        """Deletes entry with specified discord id."""
        user = self.get_user(discord_id)
        delete_query = f'DELETE FROM Users WHERE DiscordId={discord_id}'
        self.cursor.execute(delete_query)
        

class DatabaseException(Exception):
    """Base database exception class for the Database tool."""
    pass


class UserNotFound(DatabaseException):
    """Exception that's thrown when get_user cant find any entries in db."""
    pass
