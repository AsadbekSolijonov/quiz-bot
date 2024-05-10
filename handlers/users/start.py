from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.buttons import DefaultButton
def_btn = DefaultButton()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer_photo(
        photo=open('images/bot_logo.jpeg', 'rb'),
        caption=f"Salom, {message.from_user.full_name}!\n\n"
                f"Men Fanlar bo'yicha <b>🤖 QUIZ BOT</b> man.\n", reply_markup=def_btn.menu)
