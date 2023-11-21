from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Main menu keyb
async def main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Exchange")
    kb.button(text="Wallet")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Convert keyb
async def conv_calc_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Convert")
    kb.button(text='Back')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# Wallet keyb
async def wallet_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Enter your data")
    kb.button(text='List of data')
    kb.button(text='Back')
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)