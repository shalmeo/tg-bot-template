import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from tgbot.config import load_config
from tgbot.misc.set_bot_commands import set_dafault_commands
from tgbot.database.utils import make_connection_string
from tgbot import middlewares, filters, handlers


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    
    # Creating DB engine for PostgreSQL
    engine = create_async_engine(
        make_connection_string(config.db),
        future=True,
        echo=False
    )

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Creating bot and dispatcher
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    
    # setup
    middlewares.setup(dp, config, db_pool)
    filters.setup(dp)
    handlers.setup(dp)

    await set_dafault_commands(dp)

    # start
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")