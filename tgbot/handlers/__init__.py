from aiogram import Dispatcher
from . import admin, user, echo

def setup(dp: Dispatcher):
    for module in (admin, user, echo):
        module.setup(dp)