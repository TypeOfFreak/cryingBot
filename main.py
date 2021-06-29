import logging
import os
import random
import uuid
from src.services.joke_service import JokeService

from src import setup, models

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# load ENV and setup database
load_dotenv()
session = setup.connect()

# logging setup
logging.basicConfig(level=logging.ERROR, filename="data/app.log")

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

# generate Services
joke_service = JokeService(session)


@dp.message_handler(content_types=['photo'])
async def save_joke_with_photo(message: types.Message):
    if "caption" in message and message.caption.startswith("/save"):
        text = message.caption.split("/add")[1:]
        path = 'data/downloads/' + str(uuid.uuid4()) + ".jpg"
        await message.photo[-1].download(path)
        joke_service.save_joke("".join(text).strip(), path)
        await message.reply("Шутка успешно сохранена вместе с картинкой")


@dp.message_handler(commands=['сохр'], commands_prefix='!/')
async def save_joke(message: types.Message):
    text = message.get_args()
    joke_service.save_joke(text)
    await message.reply("Шутка успешно сохранена")


@dp.message_handler(commands=['шутка'], commands_prefix='!/')
async def get_joke(message: types.Message):
    try:
        joke = random.choice(joke_service.get_jokes())
        if joke.image is not None:
            with open(joke.image, "rb") as photo:
                await message.reply_photo(photo, caption=joke.text)
            return
        await message.reply(joke.text)

    except Exception as e:
        await message.reply(str(e))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
