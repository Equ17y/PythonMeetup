# Основные обработчики
from . import states_bot
from ptb.keyboards import keyboard
from asgiref.sync import sync_to_async

async def guest_handler_main_menu(update, context):
    """
    Обработчик callback'ов для гостя
    Обрабатывает нажатия на кнопки клавиатуры гостя
    """
    from meetup_core.models.Guest import Guest

    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data == 'program':
        await query.edit_message_text(
            "Программа мероприятий",
            reply_markup=keyboard.guest_keyboard()
        )

    elif callback_data == 'upcoming':
        await query.edit_message_text(
            "Предстоящие мероприятия",
            reply_markup=keyboard.guest_keyboard()

        )

    return states_bot.TEST

