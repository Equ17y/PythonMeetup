# Контроль состояний
from telegram.ext import(
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from . import cmd_handlers, states_bot
from .callback_handlers import main_menu_handler, events_list_handler

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', cmd_handlers.start)
    ],
    states={
        states_bot.MAIN_MENU: [
            CallbackQueryHandler(main_menu_handler),
        ],
        states_bot.EVENTS_LIST: [
            CallbackQueryHandler(events_list_handler),
        ],
        states_bot.EVENT_PROGRAM: [
            CallbackQueryHandler(events_list_handler),
        ],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.start)]
)