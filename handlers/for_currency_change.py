from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from exchange_req import convert
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.for_keyboard import main_keyboard, conv_calc_keyboard

import json

router = Router()

class Exchange(StatesGroup):
    convertationpair1 = State()
    convertationpair2 = State()
    convertation_step = State()


# Handler for /help
@router.message(Command('help'))
async def command_help(msg: Message):
    await msg.answer(text=f'''
Here is some information on using this bot:
1) Press the Exchange button to check currency exchange rates. You can also view the list of supported currencies using /currencies.
2) If you wish to start keeping a spending journal, press the Wallet button.
''', reply_markup=await main_keyboard())

# Handler for /currencies
@router.message(Command('currencies'))
async def command_currencies(msg: Message):
    data_cur = 'currencies.json'
    with open(data_cur, 'r') as file:
        currencies = json.load(file)
    
    lines = []
    for curren, name, country in zip(currencies.keys(), (name['name'] for name in currencies.values()), (country['country'] for country in currencies.values())):
        lines.append(f'{curren} - {name} - {country}')
        
    line1 = '\n'.join(lines[:120])
    line2 = '\n'.join(lines[120:])
    await msg.answer(text=f'{line1}')
    await msg.answer(text=f'{line2}')

# Handler for /start
@router.message(Command('start'))
async def command_start(msg: Message):
    await msg.answer(text=f'''Welcome! It is a <b>FinancialBot</b>.
Please use /help to read the instructions.''', parse_mode='HTML')
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='GitHub',
        url='https://github.com/IgChern'
    ))
    builder.row(InlineKeyboardButton(
        text='Telegram',
        url='https://t.me/igareokay'
    ))
    await msg.answer(text="Here is developer's info", reply_markup=builder.as_markup())
    await msg.answer(text= 'Please use keyboard buttons to make a choise', reply_markup=await main_keyboard())

# If button Exchange
@router.message(lambda message: message.text in ['Exchange'])
async def exchange(msg: Message):
    await msg.answer(text='Now you are entered to exchange, please push Convert', reply_markup=await conv_calc_keyboard())

# If button Back
@router.message(lambda message: message.text in ['Back'])
async def exchange(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text='You are entered at the main menu', reply_markup=await main_keyboard())

# If button Convert
@router.message(lambda message: message.text in ['Convert'])
async def convertation(msg: Message, state: FSMContext):
    try:
        await state.set_state(Exchange.convertationpair1)
        await msg.answer(text='Please enter the first currency code for conversion: ', reply_markup=ReplyKeyboardRemove())
    except Exception as ex:
        await msg.answer(str(ex))

# Get first currency
@router.message(Exchange.convertationpair1)
async def get_pair1(msg: Message, state: FSMContext):
    try:
        pair1 = msg.text.upper()
        await state.update_data(pair1=pair1)
        await msg.answer(text='You are entered the first currency. Please enter the second currency code for conversion: ')
        await state.set_state(Exchange.convertationpair2)
    except Exception as ex:
        await msg.answer(str(ex))

# Get second currency
@router.message(Exchange.convertationpair2)
async def get_pair2(msg: Message, state: FSMContext):
    try:
        pair2=msg.text.upper()
        await state.update_data(pair2=pair2)
        await convertation_step(msg, state)
    except Exception as ex:
        await msg.answer(str(ex))

# Give response cur1/cur2
@router.message(Exchange.convertation_step)
async def convertation_step(msg: Message, state: FSMContext):
    try:
        await msg.answer(text='Here is your rates: ')
        data = await state.get_data()
        pair1 = data.get('pair1')
        pair2 = data.get('pair2')
        response = convert(pair1, pair2)
        await msg.answer(text=f'{response}', reply_markup=await conv_calc_keyboard())
    except Exception as ex:
        await msg.answer(str(ex))

