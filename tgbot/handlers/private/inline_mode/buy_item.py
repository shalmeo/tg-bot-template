from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from glQiwiApi import types as qiwi_types
from glQiwiApi.utils.exceptions import APIError

from tgbot.config import Config
from tgbot.services.database.models import User
from tgbot.states.profile_dialog import ProfileSG
from tgbot.keyboards.inline import buy_kb, check_paid, confirmation_kb, confirmation_cb, buy_cb, successful_payment_kb
from tgbot.misc.send_to_admin import send_admin
from tgbot.services.qiwi.payment import create_payment


async def confirmation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    item = data.get('item')
    action = callback_data.get('action')
    
    await call.message.edit_caption('Вы собираетесь приобрести данный товар?\n'
                                    f'{item.title}\n'
                                    f'Количество: 1 шт.\n\n'
                                    f'Цена {item.price}₽',
                                    reply_markup=confirmation_kb(action))


async def payment(call: types.CallbackQuery, state: FSMContext, wallet):
    data = await state.get_data()
    item = data.get("item")
    
    try:
        bill = await create_payment(amount=item.price, wallet=wallet)
        await state.update_data(bill=bill)
    except APIError:
        await call.answer('😔 К сожалению сервис временно не доступен', show_alert=False)
        return 
    
    await call.message.edit_caption(f"🔗 Вы можете оплатить счет по сслыке ниже:\n {bill.pay_url}", 
                                    reply_markup=check_paid())


async def successful_payment(call: types.CallbackQuery, state: FSMContext, user: User, 
                             session: AsyncSession, config: Config):
    data = await state.get_data()
    bill: qiwi_types.Bill = data.get("bill")
    item = data.get("item")
        
    status = await bill.check()
    
    if status:
        await call.message.edit_caption("🎉 Вы успешно оплатили покупку!\n"
                                        "В течении дня с вами свяжется админ",
                                        reply_markup=successful_payment_kb())        
        await send_admin(call.bot, 
                         call.from_user.get_mention(as_html=True), 
                         config.tg_bot.admin_ids[0], 
                         item)
        user.purchases += 1
        user.amount += item.price
        await session.commit()
        await state.reset_data()
    else:
        await call.answer("😔 Счет не был оплачен", show_alert=False)
        

async def payment_with_points(call: types.CallbackQuery, state: FSMContext, user: User, 
                              session: AsyncSession, config: Config):
    data = await state.get_data()
    item = data.get("item")
        
    if user.points >= item.price:
        await call.message.edit_caption("🎉 Вы успешно оплатили покупку!\n"
                                        "В течении дня с вами свяжется админ",
                                        reply_markup=successful_payment_kb())
        await send_admin(call.bot, 
                         call.from_user.get_mention(as_html=True), 
                         config.tg_bot.admin_ids[0], 
                         item)
        user.points -= item.price
        user.purchases += 1
        user.amount += item.price
        await session.commit()
        await state.reset_data()
    else:
        await call.answer("😔 Не хватает баллов", show_alert=False)
        

async def to_profile(call: types.CallbackQuery, dialog_manager: DialogManager):
    await call.message.delete()
    await dialog_manager.start(ProfileSG.profile, mode=StartMode.RESET_STACK)
    
    
async def cancel(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")
    
    await call.message.edit_caption(f'📌 <b>Артикль:</b> {item.id}\n'
                                    f'📝 <b>Описание:</b>\n{item.description}\n\n'
                                    f'💵 <b>Цена:</b> {item.price}₽', 
                                    reply_markup=buy_kb())
        
            
def setup(dp: Dispatcher):
    dp.register_callback_query_handler(confirmation, buy_cb.filter())
    dp.register_callback_query_handler(payment, confirmation_cb.filter(action='buy_item'))
    dp.register_callback_query_handler(successful_payment, confirmation_cb.filter(action='check_paid'))
    dp.register_callback_query_handler(payment_with_points, confirmation_cb.filter(action='buy_with_points'))
    dp.register_callback_query_handler(to_profile, confirmation_cb.filter(action='to_profile'))
    dp.register_callback_query_handler(cancel, confirmation_cb.filter(action='cancel'))