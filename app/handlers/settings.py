from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.config import config
from app.modules import storage
from app.modules.key_checker import APIProvider, check_configured_keys
from app.modules.keyboards import button_texts, main_menu, settings_menu
from app.modules.texts import t

router = Router()


class Settings(StatesGroup):
    awaiting_nickname = State()
    awaiting_role = State()


@router.message(F.text.in_(button_texts("settings")))
async def open_settings(message: Message) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await message.answer("⚙️", reply_markup=settings_menu(profile.language))


@router.callback_query(F.data == "settings:nickname")
async def ask_nickname(callback: CallbackQuery, state: FSMContext) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    await state.set_state(Settings.awaiting_nickname)
    await callback.answer()
    await callback.message.answer(t(profile.language, "ask_nickname"))


@router.message(StateFilter(Settings.awaiting_nickname))
async def save_nickname(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    profile.nickname = message.text.strip()
    await storage.save_profile(message.from_user.id, profile)
    await state.clear()
    await message.answer(
        t(profile.language, "nickname_saved", nickname=profile.nickname),
        reply_markup=main_menu(profile.language),
    )


@router.callback_query(F.data == "settings:role")
async def ask_role(callback: CallbackQuery, state: FSMContext) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    await state.set_state(Settings.awaiting_role)
    await callback.answer()
    await callback.message.answer(t(profile.language, "ask_role"))


@router.message(StateFilter(Settings.awaiting_role))
async def save_role(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    profile.ai_role = message.text.strip()
    await storage.save_profile(message.from_user.id, profile)
    await state.clear()
    await message.answer(t(profile.language, "role_saved"), reply_markup=main_menu(profile.language))


@router.callback_query(F.data == "settings:history")
async def show_history(callback: CallbackQuery) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    await callback.answer()

    if not profile.history:
        await callback.message.answer(t(profile.language, "history_empty"))
        return

    lines = [f"*{item['role']}:* {item['content']}" for item in profile.history]
    await callback.message.answer("\n\n".join(lines))


@router.callback_query(F.data == "settings:clear_history")
async def clear_history(callback: CallbackQuery) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    await storage.clear_history(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(t(profile.language, "history_cleared"))


@router.callback_query(F.data == "settings:check_keys")
async def check_api_keys(callback: CallbackQuery) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(t(profile.language, "checking_keys"))

    keys = {
        APIProvider.GROQ: config.groq_token,
        APIProvider.OPENAI: config.openai_token,
        APIProvider.ANTHROPIC: config.claude_token,
    }
    results = await check_configured_keys(keys)

    if not results:
        await callback.message.answer(t(profile.language, "no_keys_configured"))
        return

    lines = [f"*{provider.value}:* {message}" for provider, (_, message) in results.items()]
    await callback.message.answer("\n".join(lines))
