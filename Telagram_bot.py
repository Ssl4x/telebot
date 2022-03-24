"""
This is a echo bot.
It echoes any incoming text messages.
"""

import 
import os
import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\n I'm EchoBot!\n Powered by aiogram.")

@dp.message_handler(commands=['gdz'])
async def get_dz_solution(message: types.Message):
    pass

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)