from aiogram import Dispatcher

from .db import DbMiddleware
from .throttling import ThrottlingMiddleware

def setup(dp: Dispatcher, db):
    dp.setup_middleware(DbMiddleware(db))
    dp.setup_middleware(ThrottlingMiddleware())