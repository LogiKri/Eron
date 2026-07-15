from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.modules import storage
from app.modules.keyboards import LANGUAGE_MENU, main_menu
from app.modules.texts import t

router = Router()


class Onboarding(StatesGroup):
    choosing_language = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Onboarding.choosing_language)
    await message.answer(t("en", "choose_language") + " / " + t("ru", "choose_language"), reply_markup=LANGUAGE_MENU)


@router.callback_query(StateFilter(Onboarding.choosing_language), F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    language = callback.data.split(":", 1)[1]

    profile = await storage.get_profile(callback.from_user.id)
    profile.language = language
    await storage.save_profile(callback.from_user.id, profile)

    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        t(language, "start"),
        reply_markup=main_menu(language),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await message.answer(t(profile.language, "help"), reply_markup=main_menu(profile.language))
