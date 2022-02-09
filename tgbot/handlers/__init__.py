from aiogram import Dispatcher

from .private import start
from .admin import admin


def setup(dp: Dispatcher):
    for module in (start, admin):
        module.setup(dp)