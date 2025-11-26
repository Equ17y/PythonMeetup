# Клавиатуры
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


test_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton('тест', callback_data='test')]
])
