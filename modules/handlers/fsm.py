from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from modules.messageTemplates import Template
from modules.types.common import StateMachine


async def fsm_search_start(message: types.Message, state: FSMContext):
    await message.answer(Template.FSM_SEARCH_START)
    await state.set_state(StateMachine.search_input)


def setup(dp: Dispatcher):
    dp.message.register(
        fsm_search_start, F.text == Template.SEARCH_BUTTON, StateMachine.main_menu
    )
