# Утилиты для работы с меню
from ptb.roles import get_user_role
from ptb.keyboards import keyboard
from ptb.greeting_messages import get_welcome_message
from asgiref.sync import sync_to_async


async def get_main_menu_message(user_id, user_name):
    """
    Возвращает сообщение и клавиатуру для главного меню
    """
    role = await sync_to_async(get_user_role)(user_id)
    welcome_message = get_welcome_message(role, user_name)

    if role == "speaker":
        reply_markup = keyboard.speaker_keyboard()
    elif role == "organizer":
        reply_markup = keyboard.organizer_keyboard()
    else:
        reply_markup = keyboard.guest_keyboard()

    return welcome_message, reply_markup
