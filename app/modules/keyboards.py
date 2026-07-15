from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

BUTTONS = {
    "pc_control": {"en": "PC control", "ru": "Контроль ПК"},
    "find": {"en": "Find", "ru": "Найти"},
    "chat": {"en": "Chat", "ru": "Чат"},
    "settings": {"en": "Settings", "ru": "Настройки"},
    "files": {"en": "Files", "ru": "Файлы"},
    "launch_app": {"en": "Launch app", "ru": "Запустить приложение"},
    "shutdown": {"en": "Shut down", "ru": "Выключить"},
    "back": {"en": "⬅️ Back", "ru": "⬅️ Назад"},
    "change_nickname": {"en": "Change nickname", "ru": "Изменить имя"},
    "change_role": {"en": "Change AI role", "ru": "Изменить роль ИИ"},
    "history": {"en": "History", "ru": "История"},
    "clear_history": {"en": "Clear history", "ru": "Очистить историю"},
    "check_keys": {"en": "Check API keys", "ru": "Проверить API-ключи"},
}


def button_texts(key: str) -> list[str]:
    return list(BUTTONS[key].values())


def label(key: str, language: str) -> str:
    return BUTTONS[key].get(language, BUTTONS[key]["en"])


LANGUAGE_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en"),
        ]
    ]
)


def main_menu(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=label("pc_control", language)), KeyboardButton(text=label("find", language))],
            [KeyboardButton(text=label("chat", language)), KeyboardButton(text=label("settings", language))],
        ],
        resize_keyboard=True,
    )


def pc_control_menu(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=label("files", language)), KeyboardButton(text=label("launch_app", language))],
            [KeyboardButton(text=label("shutdown", language)), KeyboardButton(text=label("back", language))],
        ],
        resize_keyboard=True,
    )


def settings_menu(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=label("change_role", language), callback_data="settings:role"),
                InlineKeyboardButton(text=label("change_nickname", language), callback_data="settings:nickname"),
            ],
            [
                InlineKeyboardButton(text=label("history", language), callback_data="settings:history"),
                InlineKeyboardButton(text=label("clear_history", language), callback_data="settings:clear_history"),
            ],
            [InlineKeyboardButton(text=label("check_keys", language), callback_data="settings:check_keys")],
        ]
    )


def back_menu(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=label("back", language))]], resize_keyboard=True)
