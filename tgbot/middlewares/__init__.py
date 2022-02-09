from aiogram import Dispatcher

from .config import ConfigMiddleware
from .db import DbSessionMiddleware
from .acl import ACLMiddleware

def setup(dp: Dispatcher, config, db_pool):
    dp.setup_middleware(DbSessionMiddleware(db_pool))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(ConfigMiddleware(config))