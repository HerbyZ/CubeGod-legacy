import datetime

import config as cfg


# TODO:  Complete the log system and add it to all commands that need it.
async def log(bot, message: str):
    current_time = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
    log_channel = bot.get_channel(cfg.LOG_CHANNEL_ID)

    await log_channel.send(f'[{current_time}]: {message}')

    print(message)
