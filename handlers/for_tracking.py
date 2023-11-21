from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.for_keyboard import wallet_keyboard, main_keyboard, inc_exp_keyboard
from wallet_db import insert_data, startdb, select_data
from tabulate import tabulate


routerwallet = Router()

class Wallet(StatesGroup):
    date = State()
    description = State()
    amount = State()
    typeexpinc = State()

# Handler for Wallet button
@routerwallet.message(lambda message: message.text in ['Wallet'])
async def wallet_button(msg: Message):
    try:
        await msg.answer(text=f'''
Now you are entered to spending journal.
''', reply_markup= await wallet_keyboard())
    except Exception as ex:
        await msg.answer(str(ex))

@routerwallet.message(lambda message: message.text in ['Back'])
async def exchange(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text='You are entered at the main menu.', reply_markup=await main_keyboard())

@routerwallet.message(lambda message: message.text in ['List of data'])
async def wallet_button(msg: Message):
    try:
        dbpool = await startdb()
        if dbpool:
            user_id = msg.from_user.id
            data = await select_data(dbpool, user_id)
            table = tabulate(data, headers="keys", tablefmt="pretty", colalign=('left', 'center', 'center', 'center'))
            await msg.answer(text=f'{table}', reply_markup=await wallet_keyboard())
    except Exception as ex:
        await msg.answer(str(ex))

@routerwallet.message(lambda message: message.text in ['Enter your data'])
async def wallet_func(msg: Message, state: FSMContext):
    try:
        await state.set_state(Wallet.date)
        await msg.answer(text=f'''
Please enter the date in the format YYYY-MM-DD:
''', reply_markup= ReplyKeyboardRemove())
    except Exception as ex:
        await msg.answer(str(ex))

@routerwallet.message(Wallet.date)
async def data_func(msg: Message, state: FSMContext):
    try:
        date = msg.text
        await state.update_data(date=date)
        await msg.answer(text=f'''
Please enter the description:
''')
        await state.set_state(Wallet.description)
    except Exception as ex:
        await msg.answer(str(ex))

@routerwallet.message(Wallet.description)
async def get_desc(msg: Message, state: FSMContext):
    try:
        description = msg.text.capitalize()
        await state.update_data(description=description)
        await msg.answer(text=f'''
Please enter amount:
''')
        await state.set_state(Wallet.amount)
    except Exception as ex:
        await msg.answer(str(ex))

@routerwallet.message(Wallet.amount)
async def get_amount(msg: Message, state: FSMContext):
    try:
        amount = msg.text
        await state.update_data(amount=amount)
        await msg.answer(text=f'''Please enter a type of operation(income/expense):''')
        await state.set_state(Wallet.typeexpinc)
    except Exception as ex:
        await msg.answer(str(ex))
    
@routerwallet.message(Wallet.typeexpinc)
async def get_type(msg: Message, state: FSMContext):
    try:
        typeexpinc = msg.text.lower()
        user_id = msg.from_user.id
        await state.update_data(typeexpinc=typeexpinc)
        if typeexpinc in ('income', 'expense'):
            dbpool = await startdb()
            if dbpool:
                data = await state.get_data()
                date = data.get('date')
                description = data.get('description')
                amount = data.get('amount')
                if amount.isdigit():
                    typeexpinc = data.get('typeexpinc')
                    await insert_data(dbpool, date, description, amount, typeexpinc, user_id)
                    await msg.answer(text=f'''
You successfully added:
Date: {date}
Description: {description}
Amount: {amount}
Type: {typeexpinc}''', reply_markup=await wallet_keyboard())
                else:
                    await msg.answer(text=f'Please check again amount.', reply_markup=await wallet_keyboard())
            else:
                await msg.answer(text=f'''Error creating database connection. Please check again all your data.''')
        else:
            await msg.answer(text=f'''Make sure you have entered income or expense. Enter again.''')
    except Exception as ex:
        await msg.answer(str(ex))
    
