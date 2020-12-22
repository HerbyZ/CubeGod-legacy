import config as cfg


async def log(bot, message: str):
    log_channel = bot.get_channel(cfg.LOG_CHANNEL_ID)
    await log_channel.send(message)
    print(message)
