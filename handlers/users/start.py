import logging

from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.buttons import DefaultButton
from states.quiz import QuizState

def_btn = DefaultButton()


@dp.message_handler(CommandStart())
@dp.message_handler(CommandStart(), state=QuizState.quiz)
async def bot_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state:
        await state.finish()
        logging.info('Finished state %s for user %s', current_state, message.chat.id)

    await message.answer_photo(
        photo=open('images/bot_logo.jpeg', 'rb'),
        caption=f"Salom, {message.from_user.full_name}!\n\n"
                f"Men Fanlar bo'yicha <b>🤖 QUIZ BOT</b> man.\n", reply_markup=def_btn.menu)
