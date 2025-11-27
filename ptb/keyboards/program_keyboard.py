# Клавиатуры для программы мероприятий
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def events_list_keyboard(events):
    """
    Клавиатура со списком мероприятий
    """
    keyboard = []
    
    for event in events:
        # Форматируем время
        time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"
        
        # Добавляем статус "Идет сейчас"
        status = " 🟢" if event['is_active'] else ""
        
        button_text = f"{event['name']}{status}"
        
        callback_data = f"event_{event['id']}"
        
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # Кнопка назад
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])
    
    return InlineKeyboardMarkup(keyboard)

def event_program_keyboard(event_id):
    """
    Клавиатура для программы мероприятия (только кнопка назад)
    """
    keyboard = [
        [InlineKeyboardButton("🔙 Назад к мероприятиям", callback_data="back_to_events")]
    ]
    return InlineKeyboardMarkup(keyboard)