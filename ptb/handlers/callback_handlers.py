# Основные обработчики
from . import states_bot
from ptb.keyboards import keyboard


async def handler_main_menu(update, context):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text='Главное меню',
        reply_markup=keyboard.test_menu,
    )
    return states_bot.TEST
