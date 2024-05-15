from aiogram.dispatcher.filters.state import StatesGroup, State


class QuizState(StatesGroup):
    subjects = State()
    quiz = State()
