from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class DefaultButton:

    @property
    def menu(self):
        btn = ReplyKeyboardMarkup(resize_keyboard=True)
        menu_btn = KeyboardButton('Savollar')
        btn.add(menu_btn)
        return btn
