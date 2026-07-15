from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.config import config
from app.modules import storage
from app.modules.device import cancel_shutdown, launch_app, schedule_shutdown
from app.modules.files import MAX_SEARCH_RESULTS, is_too_large, resolve_path, search_files
from app.modules.keyboards import back_menu, button_texts, label, main_menu, pc_control_menu
from app.modules.texts import t

router = Router()


class PCControl(StatesGroup):
    menu = State()
    awaiting_file = State()
    choosing_file = State()
    awaiting_app = State()
    awaiting_shutdown_confirm = State()


@router.message(F.text.in_(button_texts("pc_control")))
async def enter_pc_control(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(PCControl.menu)
    await message.answer(t(profile.language, "pc_control_menu"), reply_markup=pc_control_menu(profile.language))


@router.message(StateFilter(PCControl), F.text.in_(button_texts("back")))
async def leave_pc_control(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.clear()
    await message.answer(t(profile.language, "start"), reply_markup=main_menu(profile.language))


@router.message(StateFilter(PCControl.menu), F.text.in_(button_texts("files")))
async def ask_file_path(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(PCControl.awaiting_file)
    await message.answer(t(profile.language, "ask_file_path"), reply_markup=back_menu(profile.language))


def _candidates_keyboard(count: int, language: str) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=str(i + 1), callback_data=f"pickfile:{i}")] for i in range(count)]
    buttons.append([InlineKeyboardButton(text=label("cancel", language), callback_data="pickfile:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def _deliver_file(message: Message, language: str, path: Path) -> None:
    if is_too_large(path):
        await message.answer(t(language, "file_too_large"))
        return
    await message.answer_document(FSInputFile(path))


@router.message(StateFilter(PCControl.awaiting_file))
async def send_requested_file(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    value = message.text.strip()

    direct_path = resolve_path(value)
    if direct_path is not None:
        await _deliver_file(message, profile.language, direct_path)
        await state.set_state(PCControl.menu)
        await message.answer(t(profile.language, "pc_control_menu"), reply_markup=pc_control_menu(profile.language))
        return

    candidates = search_files(value, config.search_roots)
    if not candidates:
        await message.answer(t(profile.language, "file_not_found", value=value))
        return

    await state.update_data(file_candidates=[str(path) for path in candidates])
    await state.set_state(PCControl.choosing_file)

    lines = [f"{i + 1}. {path.name}\n   📁 {path.parent}" for i, path in enumerate(candidates)]
    intro = t(profile.language, "file_candidates_found", count=len(candidates))
    if len(candidates) == MAX_SEARCH_RESULTS:
        intro += "\n" + t(profile.language, "too_many_matches", count=len(candidates))

    await message.answer(
        intro + "\n\n" + "\n".join(lines),
        reply_markup=_candidates_keyboard(len(candidates), profile.language),
    )


@router.callback_query(StateFilter(PCControl.choosing_file), F.data.startswith("pickfile:"))
async def choose_file_candidate(callback: CallbackQuery, state: FSMContext) -> None:
    profile = await storage.get_profile(callback.from_user.id)
    choice = callback.data.split(":", 1)[1]
    await callback.answer()

    if choice == "cancel":
        await state.set_state(PCControl.awaiting_file)
        await callback.message.answer(t(profile.language, "file_selection_cancelled"))
        return

    data = await state.get_data()
    candidates = data.get("file_candidates", [])
    index = int(choice)
    if index >= len(candidates):
        return

    await _deliver_file(callback.message, profile.language, Path(candidates[index]))
    await state.set_state(PCControl.menu)
    await callback.message.answer(t(profile.language, "pc_control_menu"), reply_markup=pc_control_menu(profile.language))


@router.message(StateFilter(PCControl.menu), F.text.in_(button_texts("launch_app")))
async def ask_app_path(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(PCControl.awaiting_app)
    await message.answer(t(profile.language, "ask_app_path"), reply_markup=back_menu(profile.language))


@router.message(StateFilter(PCControl.awaiting_app))
async def launch_requested_app(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    try:
        result = launch_app(message.text.strip())
        await message.answer(result)
    except OSError as exc:
        await message.answer(t(profile.language, "app_launch_error", error=exc))

    await state.set_state(PCControl.menu)
    await message.answer(t(profile.language, "pc_control_menu"), reply_markup=pc_control_menu(profile.language))


@router.message(StateFilter(PCControl.menu), F.text.in_(button_texts("shutdown")))
async def confirm_shutdown(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(PCControl.awaiting_shutdown_confirm)
    await message.answer(t(profile.language, "shutdown_confirm"))


@router.message(StateFilter(PCControl.awaiting_shutdown_confirm), Command("confirm"))
async def do_shutdown(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    schedule_shutdown()
    await state.set_state(PCControl.menu)
    await message.answer(t(profile.language, "shutdown_scheduled"), reply_markup=pc_control_menu(profile.language))


@router.message(StateFilter(PCControl.awaiting_shutdown_confirm), Command("cancel"))
async def abort_shutdown(message: Message, state: FSMContext) -> None:
    profile = await storage.get_profile(message.from_user.id)
    await state.set_state(PCControl.menu)
    await message.answer(t(profile.language, "shutdown_cancelled"), reply_markup=pc_control_menu(profile.language))


@router.message(Command("cancel_shutdown"))
async def cancel_scheduled_shutdown(message: Message) -> None:
    profile = await storage.get_profile(message.from_user.id)
    cancel_shutdown()
    await message.answer(t(profile.language, "shutdown_cancelled"))
