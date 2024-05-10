import logging

from aiogram.dispatcher import FSMContext

from keyboards.inline.buttons import InlineButton
from loader import dp
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from states.quiz import QuizState
from utils.db_api.db import QuestionCategory
from handlers.users.algorithm import Queue
from utils.db_api.db import Answer
from keyboards.default.buttons import DefaultButton

def_btn = DefaultButton()
answer = Answer()
in_btn = InlineButton()

# def questions():
questions = Queue()


# return my_questions


def subjects():
    categories = QuestionCategory()
    subjects_all = categories.objects_all()
    my_subjects = [category[0].lower() for category in subjects_all]
    return my_subjects


@dp.callback_query_handler(text=subjects().append('next'), state=QuizState.quiz)
async def question_math(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'next':
        await call.message.answer("Savollar: ", reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:
        obj = data.get('quiz').dequeue()

    if obj:
        question = obj[1]  # Savol
        explanation = obj[2]  # Javobni tushuntirish
        correct_id = answer.get(question_id=obj[0])[-1]  # to'g'ri javob
        options = [option for option in answer.get(question_id=obj[0])][2:5]  # variantlar

        await call.message.answer_poll(question=question,
                                       options=options,
                                       correct_option_id=correct_id,
                                       explanation=explanation,
                                       type="quiz", reply_markup=in_btn.next_btn)  # savol yuborish
        logging.info(call.message)
        await QuizState.quiz.set()
    else:
        await call.message.answer("Savollar tugadi", reply_markup=def_btn.menu)  # savollar tugadi.
        await state.finish()
    await call.answer(cache_time=60)


