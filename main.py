import asyncio
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB

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
async def find(message: types.Message, command: CommandObject):
    if command.args:
        search_result = api.search(query=command.args)

        if not search_result:
            await message.answer(
                "💔 Нічого не знайдено. Спробуйте інший пошуковий запит або англійську мову"
            )
            return

        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="⭐ Додати до улюблених",
                        callback_data=f"add_to_favorites:{search_result.movie_id}",
                    )
                ]
            ]
        )

        await message.answer_photo(
            photo=search_result.poster_path,
            caption=search_result.text,
            reply_markup=markup,
        )
    else:
        await message.answer(
            "💔 Неправильне використання команди, введіть параметри пошуку."
        )


@dp.callback_query()
async def callback_query_handler(callback: types.CallbackQuery):
    callback_data = callback.data.split(":")

    match callback_data[0]:
        case "add_to_favorites":
            db.add_movie_to_user(
                user_id=callback.from_user.id,
                movie_id=int(int(callback_data[1])),
            )
            await callback.answer(
                text=str(db.get_all()),
                show_alert=True
            )


@dp.message(Command("all"))
async def all(message: types.Message):
    await message.answer(str(db.get_all()))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
