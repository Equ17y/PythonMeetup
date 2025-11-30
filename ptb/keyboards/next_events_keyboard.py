# Клавиатуры для подписки на следующие мероприятия
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def next_events_list_keyboard(events):
    """
    Клавиатура со списком следующих мероприятий
    """
    keyboard = []

    for event in events:
        button_text = f"{event['name']}"

        callback_data = f"event_{event['id']}"

        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    # Кнопка назад
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])

    return InlineKeyboardMarkup(keyboard)


def next_event_program_keyboard(event_id, subscribed=False):
    """
    Клавиатура для программы мероприятия
    """
    keyboard = [
        [
            InlineKeyboardButton("🔙 Назад к мероприятиям", callback_data="back_to_events")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
