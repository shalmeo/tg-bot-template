from aiogram import Dispatcher

from .admin import AdminFilter 
from .user import UserFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(UserFilter)