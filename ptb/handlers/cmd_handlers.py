# Обработчик команд вида /команда
from ptb.keyboards import keyboard
from . import states_bot


async def start(update, context):
    await update.message.reply_text(
        text='Приветствую тебя пользователь!',
        reply_markup=keyboard.test_menu,
    )

    return states_bot.TEST
