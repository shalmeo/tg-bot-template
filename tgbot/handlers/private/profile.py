from aiogram import Dispatcher, types
from aiogram_dialog import DialogManager, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.states.profile_dialog import ProfileSG


async def show_profile(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfileSG.profile, mode=StartMode.RESET_STACK)
    

async def referal(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().switch_to(ProfileSG.referal)
    

async def feedback(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().switch_to(ProfileSG.feedback) 
    

async def go_back(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().switch_to(ProfileSG.profile) 


def setup(dp: Dispatcher):
    dp.register_message_handler(show_profile, text='🏠 Профиль', is_user=True)