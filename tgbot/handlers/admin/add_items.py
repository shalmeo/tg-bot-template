from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram_dialog import DialogManager
from aiogram.dispatcher.filters.state import State
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.inline import item_finish_kb, item_kb, item_cb
from tgbot.services.database.quick_commands import merge_item
from tgbot.states.add_item import AddItem
from tgbot.states.admin_dialog import AdminSG


async def set_link(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AddItem.link)
    

async def set_title_price(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().switch_to(AddItem.title_price)
    

async def set_description(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().switch_to(AddItem.description)
    

async def go_back(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().back()
    
    
async def to_panel(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.panel)
    

async def to_view(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.message.delete()
    
    state: FSMContext = dialog_manager.data.get('state')
    data = await state.get_data()
    
    photo_url = data.get('photo_url')
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
        
    await call.message.answer_photo(photo=photo_url, 
                                    caption=f'📌 <b>Название:</b> {title}\n'
                                            f'📝 <b>Описание:</b>\n{description}\n\n'
                                            f'💵 <b>Цена:</b> {price}₽',
                                            reply_markup=item_kb())
    
    
async def add_item(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    
    photo_url = data.get('photo_url')
    title = data.get('title')
    description = data.get('description')
    price = int(data.get('price'))
    
    merge = await merge_item(session, title=title, description=description, price=price, photo_url=photo_url)
    
    if merge:
        await call.message.edit_caption('🎉 Товар был успешно добавлен', reply_markup=item_finish_kb())
        await state.reset_data()
    else:
        await call.answer('😔 Что-то пошло не так', show_alert=False)
    
        
async def add_more(call: types.CallbackQuery, dialog_manager: DialogManager):
    await call.message.delete()
    await dialog_manager.start(AddItem.link) 
        

async def cancel(call: types.CallbackQuery, dialog_manager: DialogManager):
    await call.message.delete()
    await dialog_manager.start(AdminSG.panel)
        
    
async def handler(message: types.Message, dialog_manager: DialogManager, state: FSMContext):
    context = dialog_manager.current_context()
    current_state: State = context.state.state
    
    if current_state == 'AddItem:link':
        await state.update_data(photo_url=message.text)
        await dialog_manager.start(AddItem.title_price, data=context.dialog_data)
    
    elif current_state == 'AddItem:title_price':
        *title, price = message.text.split()
        await state.update_data(title=' '.join(title), price=price)
        await dialog_manager.start(AddItem.description, data=context.dialog_data)
    
    elif current_state == 'AddItem:description':
        await state.update_data(description=message.text)
        await dialog_manager.start(AddItem.view, data=context.dialog_data)
    
    
def setup(dp: Dispatcher):
    dp.register_message_handler(handler, is_admin=True)
    dp.register_callback_query_handler(add_item, item_cb.filter(action='add'))
    dp.register_callback_query_handler(add_more, item_cb.filter(action='add_more'))
    dp.register_callback_query_handler(cancel, item_cb.filter(action='cancel'))
    