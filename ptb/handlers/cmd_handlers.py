# Обработчик команд вида /команда
from ptb.menu_utils import get_main_menu_message
from . import states_bot
from asgiref.sync import sync_to_async


async def start(update, context):
    """
    Обработчик команды /start для всех ролей
    """
    user = update.effective_user

    message_text, reply_markup = await get_main_menu_message(user.id, user.first_name)

    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return states_bot.MAIN_MENU