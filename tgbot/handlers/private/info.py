from aiogram import Dispatcher, types

from tgbot.keyboards.inline import info_kb


async def show_info(message: types.Message):
    await message.answer('1.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Velit sed ullamcorper morbi tincidunt ornare massa eget.\n'
                         '1.2 Massa tempor nec feugiat nisl pretium. Integer malesuada nunc vel risus. Dui id ornare arcu odio. Vitae congue eu consequat ac felis donec. Enim neque volutpat ac tincidunt vitae semper quis. Ultricies integer quis auctor elit sed vulputate mi sit amet.\n\n'
                         '2.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Aliquam ultrices sagittis orci a scelerisque purus semper eget. At quis risus sed vulputate odio ut enim.\n'
                         '2.2 Enim eu turpis egestas pretium. Orci sagittis eu volutpat odio facilisis mauris. Commodo sed egestas egestas fringilla. Scelerisque purus semper eget duis at tellus at urna condimentum.',
                         reply_markup=info_kb())
    
   
async def close_info(call: types.CallbackQuery):
    await call.message.delete()    

    
def setup(dp: Dispatcher):
    dp.register_message_handler(show_info, text='📎 Информация')
    dp.register_callback_query_handler(close_info, text='close_info')