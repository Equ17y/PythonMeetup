# Клавиатуры
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def guest_keyboard():
    """
    Клавиатура для гостя (слушателя)
    """
    keyboard = [
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='program'),
            InlineKeyboardButton('Предстоящие мероприятия', callback_data='upcoming')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def speaker_keyboard():
    """
    Клавиатура для спикера
    """
    keyboard = [
        [
            InlineKeyboardButton('Завершить свое выступление', callback_data='finish_speech'),
        ],
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='program'),
            InlineKeyboardButton('Предстоящие мероприятия', callback_data='upcoming')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def organizer_keyboard():
    """
    Клавиатура для организатора
    """
    keyboard = [
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='program'),
            InlineKeyboardButton('Рассылка', callback_data='broadcast')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)