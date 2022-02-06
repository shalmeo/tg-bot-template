from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import User
from tgbot.states.enter_referal import EnterReferal
from tgbot.keyboards.reply import cancel_kb, confirm_kb
from tgbot.misc.allow_acc import allow_acces
from tgbot.misc.referal import add_referal
from tgbot.services.database.quick_commands import fetch_user


@allow_acces()
async def enter_referal(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Введите ID пригласившего вас пользователя пользователя ✏️\n\n'
                                 'Вы сможете получить доступ к боту, после того как введете ID.')
    await state.set_state(EnterReferal.enter)
    

@allow_acces()
async def confirm_referal(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        referal = await fetch_user(session, int(message.text))
        if referal:
            await message.answer(f'Вы ввели <b>{message.text}</b>\n\n'
                                 'Чтобы подтвердить нажмите ✅ Да\n'
                                 'Чтобы отменить нажмите ❌ Нет', reply_markup=confirm_kb())
            
            await state.update_data(referal=referal)
            await state.set_state(EnterReferal.confirm)
        else:
            await message.answer('К сожалению нам не удалось найти такого пользователя 😔\n'
                                 'Попытайтесь ввести ID еще раз.\n\n'
                                 'Чтобы выйти нажмите "Отменить"', reply_markup=cancel_kb())
    except ValueError:
        await message.answer('Похоже вы ввели не число 😔\n'
                             'Попытайтесь ввести ID еще раз.\n\n'
                             'Чтобы выйти нажмите "Отменить"', reply_markup=cancel_kb())


@allow_acces()
async def confirm(message: types.Message, state: FSMContext, session: AsyncSession, user: User):
    await message.answer('Нажмите /start, чтобы посмотреть информацию о доступе.', 
                         reply_markup=types.ReplyKeyboardRemove())
    
    data = await state.get_data()
    referal = data.get('referal')
    
    if message.text == '✅ Да':
        await add_referal(session, referal, user)
        
    await state.finish()
    
    
@allow_acces()
async def cancel(message: types.Message, state: FSMContext):
    await message.answer('Нажмите /start, чтобы посмотреть информацию о доступе.',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(enter_referal, text='enter_referal')
    dp.register_message_handler(cancel, text='Отменить', state=EnterReferal.enter)
    dp.register_message_handler(confirm_referal, state=EnterReferal.enter)
    dp.register_message_handler(confirm, state=EnterReferal.confirm)