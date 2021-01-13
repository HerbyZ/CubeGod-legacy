import postgresql.driver as pg_driver

import config as cfg


class Database:
    def __init__(self):
        self.db = pg_driver.connect(
            user=cfg.DB_USERNAME,
            password=cfg.DB_PASSWORD,
            host=cfg.DB_HOST,
            port=cfg.DB_PORT,
            database=cfg.DB_NAME
        )

    def add_user(self, discord_id: int):
        """Adds user to Users table."""
        try: # Checks that user's entry doesn't exists
            self.get_user(discord_id)
        except UserNotFound:
            query = f'INSERT INTO users (discord_id) VALUES ({discord_id})'
            self.db.execute(query)

    def update_user(self, discord_id: int, table: str='users', **kwargs):
        """Updates data from kwargs for entry with discord_id = discord_id."""
        if not kwargs:
            raise ValueError('No data about user.')

        items = ''
        for key, value in kwargs.items():
            if type(value) != str:
                items += f'{key}={value},'
            else:
                items += f'{key}=\'{value}\','

        # Checks that user already in db
        try:
            self.get_user(discord_id)
        except UserNotFound:
            raise

        query = f'UPDATE {table} SET {items[:-1]} WHERE discord_id = {discord_id}'
        self.db.execute(query)

    def ban_user(self, discord_id: int, reason=None):
        """Adds user's entry to banned_users table."""
        try: # Checks that user not in banned_users
            self.get_banned_user(discord_id)
        except UserNotFound:
            query = f'INSERT INTO banned_users (discord_id, ban_reason) VALUES ({discord_id}, \'{reason}\')'
            self.db.execute(query)

    def unban_user(self, discord_id: int):
        """Deletes user's entry from BannedUsers table."""
        try: # Checks that user's entry exists in BannedUsers
            self.get_banned_user(discord_id)
        except:
            raise

        query = f'DELETE FROM banned_users WHERE discord_id = {discord_id}'
        self.db.execute(query)

    def get_user(self, discord_id):
        """Returns entry with specified discord id."""
        query = f'SELECT * FROM users WHERE discord_id = {discord_id}'
        data = self.db.prepare(query)

        result = []
        for i in data:
            result.append(i)

        if len(result) == 0:
            raise UserNotFound(f'User with discord_id={discord_id} not found.')

        result = result[0]
        user = {
            'id': result[0],
            'discord_id': result[1],
            'join_date': result[2],
            'level': result[3],
            'experience': result[4]
        }

        return user

    def get_banned_user(self, discord_id):
        """Returns entry with specified discord id."""
        query = f'SELECT * FROM banned_users WHERE discord_id = {discord_id}'
        data = self.db.prepare(query)

        result = []
        for i in data:
            result.append(i)

        if len(result) == 0:
            raise UserNotFound(f'User with discord_id={discord_id} not found.')

        return result[0]

    def delete_user(self, discord_id):
        """Deletes entry with specified discord id."""

        # Checks that user already in db
        try:
            self.get_user(discord_id)
        except UserNotFound:
            raise

        # Delete's user's entry from db
        query = f'DELETE FROM users WHERE discord_id={discord_id}'
        self.db.execute(query)
        

class DatabaseException(Exception):
    """Base database exception class for the Database tool."""
    pass


class UserNotFound(DatabaseException):
    """Exception that's thrown when get_user cant find any entries in db."""
    pass


if __name__ == "__main__":
    db = Database()
    id = 319861774604304384
    db.ban_user(id)
    db.update_user(id, 'banned_users', ban_reason='hello, world!')
    user = db.get_banned_user(id)
    for i in user:
        print(i)
