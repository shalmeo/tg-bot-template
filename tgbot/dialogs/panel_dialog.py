from aiogram_dialog import Dialog, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.admin.add_items import go_back, to_panel, to_view
from tgbot.states.add_item import AddItem


add_item_dialog = Dialog(
    Window(
        Const('🛠 Административная панель\n'
              'Добавление сслыки\n\n'
              '"<b>http://example.com</b>"'),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=to_panel)),
       state=AddItem.link
    ),    
    
    Window(
        Const('🛠 Административная панель\n'
              'Добавление названия и цены\n\n'
              '"<b>title 25</b>"'),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=go_back)),
        state=AddItem.title_price
    ),
    
    Window(
        Const(
              '🛠 Административная панель\n'
              'Добавление описания\n\n'
              '"Lorem ipsum..."'),
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        state=AddItem.description
    ),
    
    Window(
        Const(
            '🛠 Административная панель\n'
            'Просмотр результата'),
        Button(Const('🔮 Просмотр'), id='back', on_click=to_view),
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        state=AddItem.view
    )
)


def setup(registry: DialogRegistry):
    registry.register(add_item_dialog)