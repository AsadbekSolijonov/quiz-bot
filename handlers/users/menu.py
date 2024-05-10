import logging

from handlers.users.algorithm import Queue
from loader import dp
from aiogram import types
from states.quiz import QuizState
from aiogram.dispatcher import FSMContext
from keyboards.inline.buttons import InlineButton

in_btn = InlineButton()


@dp.message_handler(text='Savollar')
async def show_menu(message: types.Message, state: FSMContext):
    await message.answer("Bo'limlardan birini tanlang:", reply_markup=in_btn.show_categories)
    async with state.proxy() as data_file:
        data_file['quiz'] = Queue()
    await QuizState.quiz.set()

