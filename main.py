import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB

from modules.handlers.general import setup as setup_general
from modules.handlers.commands import setup as setup_commands
from modules.handlers.callbacks import setup as setup_callbacks
from modules.handlers.fsm import setup as setup_fsm

import config
import logging
import os


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    movie_api = MovieAPI(config.TMDB_ACCESS_TOKEN)
    db = FavoritesDB(config.DB_PATH)

    dp = Dispatcher(db=db, movie_api=movie_api)
    setup_general(dp)
    setup_commands(dp)
    setup_callbacks(dp)
    setup_fsm(dp)
    

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
