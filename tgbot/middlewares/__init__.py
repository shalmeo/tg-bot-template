from aiogram import Dispatcher

from .config import ConfigMiddleware
from .db import DbSessionMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, config, db_pool):
    dp.setup_middleware(ConfigMiddleware(config))
    dp.setup_middleware(DbSessionMiddleware(db_pool))
    dp.setup_middleware(ThrottlingMiddleware())