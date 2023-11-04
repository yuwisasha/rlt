import asyncio
import logging
import sys
import json
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold

from aggregation import aggregate_payments

load_dotenv()

TOKEN = getenv("TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hi, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    group_info: dict = json.loads(message.text)
    payments = await aggregate_payments(*group_info.values())
    await message.answer(json.dumps(payments))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
