# Контроль состояний
from telegram.ext import(
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from . import cmd_handlers, states_bot
from .callback_handlers import main_menu_handler, events_list_handler
from .broadcast_handlers import receive_broadcast_text, confirm_broadcast

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
        states_bot.BROADCAST_TEXT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receive_broadcast_text
            )
        ],
        states_bot.BROADCAST_CONFIRM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                confirm_broadcast
            )
        ],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.start)]
)