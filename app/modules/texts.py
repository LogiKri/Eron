TEXT = {
    "en": {
        "start": (
            "Hi! I am *Eron* and I'm here to help you with your problems\n\n"
            "1. You can ask me questions and I'll answer\n"
            "2. You can control your PC from this bot\n"
            "3. I can find files for you\n\n"
            "Try something :)"
        ),
        "help": "You can customize and extend the bot as you like.\nChange the language: /start\n*Eron*",
        "choose_language": "Choose your region and language",
        "pc_control_menu": (
            "*PC control menu*\n"
            "Here you can control the device this bot is running on:\n"
            "1. Send files\n"
            "2. Launch applications\n"
            "3. Shut down the PC\n"
        ),
        "chat_intro": "You're chatting with Eron now. Send /stop to leave the chat.",
        "chat_stopped": "Chat closed.",
        "chat_not_configured": "AI chat is not configured. Add GROQ_TOKEN to your .env file.",
        "ask_file_path": "Send the full path to a file to grab it directly, or just its name (or part of it) to search for it.",
        "file_not_found": "No files matching '{value}' were found.",
        "file_too_large": "This file is larger than Telegram's 50 MB limit.",
        "file_candidates_found": "Found {count} matching file(s). Pick one:",
        "too_many_matches": "Showing the first {count} matches — send a more specific name if yours isn't listed.",
        "file_selection_cancelled": "Selection cancelled.",
        "cancel": "❌ Cancel",
        "ask_app_path": "Send the full path to the application you want to launch.",
        "app_launch_error": "Could not launch the application: {error}",
        "shutdown_confirm": "This will shut down the PC in 60 seconds. Send /confirm to proceed or /cancel to abort.",
        "shutdown_scheduled": "Shutdown scheduled. Send /cancel_shutdown any time before it happens.",
        "shutdown_cancelled": "Shutdown cancelled.",
        "ask_nickname": "Send the nickname you'd like me to use for you.",
        "nickname_saved": "Got it, I'll call you {nickname} from now on.",
        "ask_role": "Send the role or personality you want the assistant to take on.",
        "role_saved": "Role updated.",
        "history_cleared": "Chat history cleared.",
        "history_empty": "No chat history yet.",
        "checking_keys": "Checking configured API keys, one moment…",
        "no_keys_configured": "No API keys are set in .env (GROQ_TOKEN / OPEN_AI_TOKEN / CLAUDE_TOKEN).",
        "back": "⬅️ Back",
    },
    "ru": {
        "start": (
            "Привет! Меня зовут *Eron*, и я здесь, чтобы помочь тебе с твоими задачами\n\n"
            "1. Ты можешь задать мне вопросы, и я отвечу\n"
            "2. Ты можешь управлять своим компьютером через этого бота\n"
            "3. Я могу находить для тебя файлы\n\n"
            "Попробуй что-нибудь :)"
        ),
        "help": "Ты можешь настроить и доработать бота как тебе удобно.\nПоменять язык: /start\n*Eron*",
        "choose_language": "Выбери регион и язык",
        "pc_control_menu": (
            "*Меню контроля ПК*\n"
            "Здесь ты можешь управлять устройством, на котором запущен бот:\n"
            "1. Отправлять файлы\n"
            "2. Запускать приложения\n"
            "3. Выключать ПК\n"
        ),
        "chat_intro": "Ты общаешься с Eron. Отправь /stop, чтобы выйти из чата.",
        "chat_stopped": "Чат завершён.",
        "chat_not_configured": "ИИ-чат не настроен. Добавь GROQ_TOKEN в .env файл.",
        "ask_file_path": "Отправь полный путь к файлу, чтобы получить его сразу, или просто имя (или часть имени) для поиска.",
        "file_not_found": "Файлы по запросу '{value}' не найдены.",
        "file_too_large": "Файл превышает лимит Telegram в 50 МБ.",
        "file_candidates_found": "Найдено {count} совпадений. Выбери файл:",
        "too_many_matches": "Показаны первые {count} совпадений — пришли более точное имя, если нужного файла здесь нет.",
        "file_selection_cancelled": "Выбор отменён.",
        "cancel": "❌ Отмена",
        "ask_app_path": "Отправь полный путь к приложению, которое нужно запустить.",
        "app_launch_error": "Не удалось запустить приложение: {error}",
        "shutdown_confirm": "ПК выключится через 60 секунд. Отправь /confirm для подтверждения или /cancel для отмены.",
        "shutdown_scheduled": "Выключение запланировано. Отправь /cancel_shutdown, чтобы отменить.",
        "shutdown_cancelled": "Выключение отменено.",
        "ask_nickname": "Отправь имя, по которому мне тебя называть.",
        "nickname_saved": "Хорошо, теперь буду звать тебя {nickname}.",
        "ask_role": "Отправь роль или характер, который должен принять ассистент.",
        "role_saved": "Роль обновлена.",
        "history_cleared": "История чата очищена.",
        "history_empty": "История чата пока пуста.",
        "checking_keys": "Проверяю добавленные API-ключи, секунду…",
        "no_keys_configured": "В .env не указано ни одного ключа (GROQ_TOKEN / OPEN_AI_TOKEN / CLAUDE_TOKEN).",
        "back": "⬅️ Назад",
    },
}


def t(language: str, key: str, **kwargs) -> str:
    template = TEXT.get(language, TEXT["en"]).get(key, TEXT["en"][key])
    return template.format(**kwargs) if kwargs else template
