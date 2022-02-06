from aiogram import Bot


async def check_subscription(user_id, channel='-1001714061689'):
    bot = Bot.get_current()
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.is_chat_member()