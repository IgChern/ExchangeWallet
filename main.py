import asyncio
import sys, os
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from handlers import for_currency_change, for_tracking
from dotenv import load_dotenv
from wallet_db import startdb

load_dotenv()
TELETOKEN = os.getenv('TELETOKEN')
dp = Dispatcher()
router = Router()
dp.include_routers(for_currency_change.router, for_tracking.routerwallet)

async def start(loop: asyncio.AbstractEventLoop) -> None:
    bot = Bot(token=TELETOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
    await Bot.set_my_commands(self=bot, commands=[
        types.BotCommand(command="start", description="Start bot"),
        types.BotCommand(command="help", description="Help info"),
        types.BotCommand(command="currencies", description="List of supported currencies")
    ])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    dbpool = loop.run_until_complete(startdb())

    try:
        loop.run_until_complete(start(loop))
    except KeyboardInterrupt:
        pass
    finally:
        if dbpool:
            loop.run_until_complete(dbpool.close())
            print('Connect closed')