# Клавиатуры
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


test_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton('тест', callback_data='test')]
])

def guest_keyboard():
    """
    Основная клавиатура для гостя (слушателя)
    Содержит основные функции доступные гостю:
    - Просмотр программы мероприятий
    - Просмотр предстоящих мероприятий
    - Просмотр своего профиля
    """
    keyboard = [
        [
            InlineKeyboardButton('Программа мероприятий', callback_data='program'),
            InlineKeyboardButton('Предстоящие мероприятия', callback_data='upcoming')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)