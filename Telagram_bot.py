import os
import logging

import parsers
from url import Url
parser = parsers.Parser()

from aiogram import Bot, Dispatcher, executor, types

# подгружает токен бота из переменной окружения
API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['ping'])
async def ping_pong(message: types.Message):
    """для проверки работоспособности"""
    await message.reply("pong!")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Вызывается при запуске бота. """
    await message.reply("По башке себе постучи! Козел... \n Сделал Прядкин Максим")

@dp.message_handler(commands=['gdz'])
async def get_dz_solution(message: types.Message):
    """вытаскивает картинку решения задачи с сайта gdz.ru"""

    
    print(message.text)
    # превращает запрос из строки в список строк и отрезает команду /gdz
    text = message.text.lower().split()[1:]

    # запраштвает у парсера ссылку с сайта. если запрос неправильный то парсер вернет сообщение, 
    # если правильный, то обьект класса Url
    imgs_urls: list[Url] = parser.make_url_from_words(text)

    # проверяет является значение, отправленное парсером ссылкой
    if type(imgs_urls) != list:
        # т.к. значение не является ссылкой возвращает сообщение, переданное парсером
        await message.answer(imgs_urls)
    # если сообщение ссылка возвращает кртинку
    else:
        for img in imgs_urls:
            await message.answer_photo(img)

def start():
    """запуск бота"""
    executor.start_polling(dp, skip_updates=True)
