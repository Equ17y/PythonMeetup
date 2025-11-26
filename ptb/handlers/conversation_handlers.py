# Контроль состояний
from telegram.ext import(
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)
from . import callback_handlers, cmd_handlers, states_bot


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', cmd_handlers.start)],
    states={
        states_bot.TEST: [
            CallbackQueryHandler(callback_handlers.handler_main_menu)
        ],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.start)]
)