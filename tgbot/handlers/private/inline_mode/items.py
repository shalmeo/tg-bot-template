from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from tgbot.services.database.models import Items


async def show_items(query: types.InlineQuery, session: AsyncSession):
    result = await session.execute(select(Items))
    items = result.scalars().all()
    results = list()
    for item in items:
        results.append(types.InlineQueryResultArticle(
            id=item.id,
            title=item.title,
            description=f'{item.price}₽',
            input_message_content=types.InputTextMessageContent(f'<b>Название:</b> <i>{item.title}</i>\n\n'
                                                                f'<b>Описание:</b>\n<i>{item.description}</i>\n\n'
                                                                f'<b>Цена:</b> <i>{item.price}₽</i>'),
            thumb_url=item.photo_url,
            hide_url=True,
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[[types.InlineKeyboardButton(text='🔮 Показать товар', 
                                                             url=f't.me/finshalm_bot?start=buy_{item.id}')]]
            )
        ))
        
    await query.answer(results=sorted(results, key=lambda item: item.title), cache_time=10)


def setup(dp: Dispatcher):
    dp.register_inline_handler(show_items)