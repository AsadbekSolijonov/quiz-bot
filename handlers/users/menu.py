from loader import dp
from aiogram import types
from states.quiz import QuizState
from keyboards.inline.buttons import InlineButton

in_btn = InlineButton()


@dp.message_handler(text='Savollar')
async def show_menu(message: types.Message):
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=in_btn.show_categories)
    await QuizState.subjects.set()
