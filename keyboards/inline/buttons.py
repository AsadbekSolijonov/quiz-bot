from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.db import QuestionCategory

categories = QuestionCategory()


class InlineButton:
    @property
    def show_categories(self):
        my_btn = InlineKeyboardMarkup(row_width=2)
        categories_button = categories.objects_all()
        buttons = list()

        if categories_button:
            for category in categories_button:
                btn = InlineKeyboardButton(category[0], callback_data=category[0].lower())
                buttons.append(btn)
        else:
            btn = InlineKeyboardButton("Savollar mavjud emas")
            buttons.append(btn)

        my_btn.add(*buttons)

        return my_btn

    @property
    def next_btn(self):
        my_btn = InlineKeyboardMarkup()
        next_btn = InlineKeyboardButton("Next", callback_data="next")
        my_btn.add(next_btn)
        return my_btn
