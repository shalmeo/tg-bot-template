from aiogram import Bot


async def send_admin(bot: Bot, user, admin, item):
    await bot.send_message(admin, f'Пользователь {user} совершил покупку\n\n'
                                  f'<b>{item.title} {item.price}</b>₽')