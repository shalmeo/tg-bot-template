from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from tgbot.handlers.admin.add_items import set_link
from tgbot.handlers.admin.admin import admin_panel, go_back
from tgbot.misc.custom_button import SwitchCurrentChat
from tgbot.services.database.models import User
from tgbot.states.admin_dialog import AdminSG


async def info_getter(dialog_manager: DialogManager, **kwargs):
    user: User = dialog_manager.data.get('user')
    
    return {
        "tg_id": user.user_id,
    }
    

admin_dialog = Dialog(
    Window(
        Format('<b>Ваш ID:</b> <code>{tg_id}</code>\n'
               '<b>Администратор</b>'),
        SwitchCurrentChat(Const('🛒 Каталог'), id='shop'),
        Button(Const('🛠 Админ панель'), id='panel', on_click=admin_panel),
        state=AdminSG.main,
        getter=info_getter,
    ),
    
    Window(
        Const('🛠 Административная панель'),
        Button(Const('➕ Добавить товар'), id='add', on_click=set_link),
        Button(Const('📣 Рассылка'), id='distribution', on_click=''),
        Button(Const('⬅️ Назад'), id='back2', on_click=go_back),
        state=AdminSG.panel
    )
)


def setup(registry: DialogRegistry):
    registry.register(admin_dialog)