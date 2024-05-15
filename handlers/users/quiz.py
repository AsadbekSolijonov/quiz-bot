import logging

from aiogram.dispatcher import FSMContext

from keyboards.inline.buttons import InlineButton
from loader import dp
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from states.quiz import QuizState
from utils.db_api.db import QuestionCategory, Question
from handlers.users.algorithm import Queue
from utils.db_api.db import Answer
from keyboards.default.buttons import DefaultButton

def_btn = DefaultButton()
answer = Answer()
in_btn = InlineButton()


def subjects():
    categories = QuestionCategory()
    subjects_all = categories.objects_all()
    my_subjects = [category[0].lower() for category in subjects_all]
    return my_subjects


@dp.callback_query_handler(text=subjects(), state=QuizState.subjects)
async def quiz_subjects(call: types.CallbackQuery, state: FSMContext):
    category_name = call.data
    category_id = QuestionCategory().get_category_id(category_name)

    questions = Queue(category_id=category_id)
    async with state.proxy() as data:
        data["quiz"] = questions

    if not questions.dequeue():
        await call.message.answer("Savollar tez orada qo'shiladi")
        await state.finish()
    else:
        await call.message.answer(f"{call.data} savollar: ", reply_markup=ReplyKeyboardRemove())
        async with state.proxy() as data:
            obj = data.get('quiz').dequeue()

        if obj:
            question = obj[1]  # Savol
            explanation = obj[2]  # Javobni tushuntirish
            correct_id = answer.get(question_id=obj[0])[-1]  # to'g'ri javob
            options = [option for option in answer.get(question_id=obj[0])][2:5]  # variantlar a, b, c

            await call.message.answer_poll(question=question,
                                           options=options,
                                           correct_option_id=correct_id,
                                           explanation=explanation,
                                           type="quiz", reply_markup=in_btn.next_btn)  # savol yuborish
        await QuizState.quiz.set()
    await call.answer(cache_time=60)


@dp.callback_query_handler(state=QuizState.quiz)
@dp.callback_query_handler(text=['next'], state=QuizState.quiz)
async def question_math(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'next':
        await call.message.delete()

    async with state.proxy() as data:
        obj = data.get('quiz').dequeue()

    if obj:
        question = obj[1]  # Savol
        explanation = obj[2]  # Javobni tushuntirish
        correct_id = answer.get(question_id=obj[0])[-1]  # to'g'ri javob
        options = [option for option in answer.get(question_id=obj[0])][2:5]  # variantlar a, b, c

        await call.message.answer_poll(question=question,
                                       options=options,
                                       correct_option_id=correct_id,
                                       explanation=explanation,
                                       type="quiz", reply_markup=in_btn.next_btn)  # savol yuborish
        logging.info(call.message)
        await QuizState.quiz.set()
    else:
        await call.message.answer("Tez orada qolgan savollar qo'shiladi!",
                                  reply_markup=def_btn.menu)  # savollar tugadi.
        await state.finish()
    await call.answer(cache_time=60)
