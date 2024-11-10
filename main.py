import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.types import AddToFavoritesMarkup, RemoveFromFavoritesMarkup

import logging
import os

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=os.getenv("FILM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
api = MovieAPI(os.getenv("TMDB_ACCESS_TOKEN"))
db = FavoritesDB()


@dp.message(Command("start"))
async def start(message: types.Message):
    try:
        db.new_user(message.from_user.id)
        await message.answer(
            f"Вас вітає Flagrate Movie Bot! Введіть /search [назва фільму] для пошуку фільму."
        )
    except Exception as e:
        await message.answer(
            "💔 Щось пішло не так. Спробуйте команду /start ще раз пізніше\nФункціонал улюблених фільмів тимчасово недоступний"
        )


@dp.message(Command("search"))
async def search(message: types.Message, command: CommandObject):
    if command.args:
        search_result = api.search(query=command.args)

        if not search_result:
            await message.answer(
                "💔 Нічого не знайдено. Спробуйте інший пошуковий запит або англійську мову"
            )
            return

        markup = AddToFavoritesMarkup(search_result.movie_id)

        await message.answer_photo(
            photo=search_result.poster_path,
            caption=search_result.text,
            reply_markup=markup,
        )
    else:
        await message.answer(
            "💔 Неправильне використання команди, введіть параметри пошуку."
        )


@dp.callback_query(F.data.startswith("favorites"))
async def update_favorites(callback: types.CallbackQuery):
    command = callback.data.removeprefix("favorites_")
    
    movie_id = int(command.split(":")[1])
    action = command.split(":")[0]

    db.update_movies_in_user(callback.from_user.id, action, movie_id)

    if action == "add":
        await callback.answer("✅ Фільм додано до улюблених")
        markup = RemoveFromFavoritesMarkup(movie_id)
    elif action == "remove":
        await callback.answer("❌ Фільм видалено з улюблених")
        markup = AddToFavoritesMarkup(movie_id)

    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.message(Command("all"))
async def all(message: types.Message):
    await message.answer(str(db.get_all()))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
