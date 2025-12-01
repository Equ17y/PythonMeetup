# Клавиатуры
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def guest_keyboard():
    """
    Клавиатура для гостя (слушателя)
    """
    keyboard = [
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='program'),
        ],
        [
            InlineKeyboardButton('Предстоящие мероприятия', callback_data='upcoming')
        ],
        [
            InlineKeyboardButton('Подписка', callback_data='quick_subscribe')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def speaker_keyboard():
    """
    Клавиатура для спикера
    """
    keyboard = [
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='program'),
        ],
        [
            InlineKeyboardButton('Предстоящие мероприятия', callback_data='upcoming')
        ],
        [
            InlineKeyboardButton('Подписка', callback_data='quick_subscribe')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def organizer_keyboard():
    """
    Клавиатура для организатора
    """
    keyboard = [
        [
            InlineKeyboardButton('Программы мероприятий', callback_data='event_programs'),
        ],
        [
            InlineKeyboardButton('Рассылка', callback_data='broadcast')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def broadcast_confirmation_keyboard():
    """
    Клавиатура подтверждения рассылки (Reply клавиатура)
    """
    keyboard = [
        ["Разослать", "Отменить"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)