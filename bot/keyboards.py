from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню с выбором режима"""

    buttons = [
        [KeyboardButton(text="Currency Tracker")],
        [KeyboardButton(text="Screener")],
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def currency_list_keyboard(coins: list) -> ReplyKeyboardMarkup:
    """Клавиатура со списком доступных криптовалют"""

    # разбивка на ряды по три кнопки
    rows = []

    for i in range(0, len(coins), 3):
        row = [KeyboardButton(text=coin) for coin in coins[i:i+3]]
        rows.append(row)

    rows.append([KeyboardButton(text="Back to menu ->")])

    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)