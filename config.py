from tools.database import Database
from itertools import cycle

import os


# Main project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Bot token
BOT_TOKEN = os.getenv('DISCORD-TOKEN')

# Database & db options
DB_USERNAME = os.getenv('DB-USERNAME')
DB_PASSWORD = os.getenv('DB-PASSWORD')
DB_NAME = os.getenv('DB-NAME')
DB_HOST = os.getenv('DB-HOST')
DB_PORT =os.getenv('DB-PORT')

DATABASE = Database()

# Bot statuses
DEFAULT_BOT_STATUS = 'Working...'
BOT_STATUSES = cycle(['Working', 'Working.', 'Working..', 'Working...'])

# NetCube guild id
NET_CUBE_GUILD_ID = 634026670579384330

# Important discord channels
NEW_USERS_CHANNEL_ID = 634026670579384332
LOG_CHANNEL_ID = 638312215031578644
REPORT_CHANNEL_ID = 646733819852095489
VOID_CHANNEL_ID = 634788586499080212

# Level system rewards
LEVEL_REWARDS = [
    [10, 'Bloger']
]
