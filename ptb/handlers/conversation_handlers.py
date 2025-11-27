# Контроль состояний
from telegram.ext import(
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from . import cmd_handlers, states_bot
from .callback_handlers import main_menu_handler

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', cmd_handlers.start)
    ],
    states={
        states_bot.MAIN_MENU: [
            CallbackQueryHandler(main_menu_handler),
        ],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.start)]
)