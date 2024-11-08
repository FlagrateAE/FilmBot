import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from modules.movieAPI import MovieAPI

import logging
import os
logging.basicConfig(level=logging.INFO)


bot = Bot(
    token=os.getenv("FILM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
api = MovieAPI(os.getenv("TMDB_ACCESS_TOKEN"))


@dp.message(Command("start"))
async def start(message: types.Message):
    
    await message.reply("test")
    
    
@dp.message(Command("search"))
async def find(message: types.Message, command: CommandObject):    
    if command.args:
        search_result = api.search(query=command.args)
        await message.answer_photo(
            photo=search_result.poster_path,
            caption=search_result.text
        )
    else:
        await message.answer("💔 Неправильне використання команди, введіть параметри пошуку.")
    
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
