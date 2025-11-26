# Контроль состояний
from telegram.ext import(
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from . import cmd_handlers, states_bot

from .callback_handlers import guest_handler_main_menu

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', cmd_handlers.guest_start)],
    states={
        states_bot.TEST: [
            CallbackQueryHandler(guest_handler_main_menu),
        ],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.guest_start)]
)