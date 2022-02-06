import asyncio
import logging
import ssl

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram_dialog import DialogRegistry

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from glQiwiApi import QiwiWrapper

from tgbot.config import load_config
from tgbot.services.database.base import Base
from tgbot.misc.set_bot_commands import set_dafault_commands
from tgbot.services.database.utils import get_connection_string
from tgbot import dialogs, middlewares, filters, handlers


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
        get_connection_string(config.db),
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        future=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Creating
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    
    wallet = QiwiWrapper(secret_p2p=config.qiwi.p2p_token)
    registry = DialogRegistry(dp)  
    
    # setup
    middlewares.setup(dp, config, db_pool, wallet)
    filters.setup(dp)
    handlers.setup(dp)
    dialogs.setup(registry)

    # set commands
    await set_dafault_commands(bot)

    # webhook
    await bot.set_webhook(config.webhook.webhook_url, certificate=open(config.webhook.webhook_ssl_cert, 'rb'))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(config.webhook.webhook_ssl_cert, config.webhook.webhook_ssl_priv)
    app = get_new_configured_app(dispatcher=dp, path=config.webhook.webhook_url)
        
    # start
    try:
        await dp.skip_updates()
        web.run_app(app, host=config.webapp.webapp_host, port=config.webapp.webapp_port, ssl_context=context)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): 
        logger.error("Bot stopped!")