from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.modules import storage
from app.modules.keyboards import back_menu, button_texts, main_menu
from app.modules.llm import LLMNotConfigured, chat_completion
from app.modules.texts import t

router = Router()


class Chatting(StatesGroup):
    active = State()


@router.message(F.text.in_(button_texts("chat")))
async def enter_chat(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(Chatting.active)
    await message.answer(t(profile.language, "chat_intro"), reply_markup=back_menu(profile.language))


@router.message(StateFilter(Chatting.active), F.text.in_(button_texts("back")))
@router.message(StateFilter(Chatting.active), Command("stop"))
async def leave_chat(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.clear()
    await message.answer(t(profile.language, "chat_stopped"), reply_markup=main_menu(profile.language))


@router.message(StateFilter(Chatting.active))
async def handle_chat_message(message: Message) -> None:
    profile = await storage.get_profile(message.from_user.id)

    try:
        profile = await storage.append_history(message.from_user.id, "user", message.text)
        reply = await chat_completion(profile.ai_role, profile.history)
        await storage.append_history(message.from_user.id, "assistant", reply)
        await message.answer(reply)
    except LLMNotConfigured:
        await message.answer(t(profile.language, "chat_not_configured"))
