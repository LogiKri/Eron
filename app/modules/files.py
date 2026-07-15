import os
from pathlib import Path

MAX_TELEGRAM_FILE_SIZE = 50 * 1024 * 1024
MAX_SEARCH_RESULTS = 10

SKIP_DIR_NAMES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "$Recycle.Bin", "System Volume Information",
}


def resolve_path(raw_path: str) -> Path | None:
    path = Path(raw_path.strip().strip('"')).expanduser()
    return path if path.is_file() else None


def search_files(query: str, roots: list[str], max_results: int = MAX_SEARCH_RESULTS) -> list[Path]:
    needle = query.strip().lower()
    matches: list[Path] = []

    for root in roots:
        root_path = Path(root).expanduser()
        if not root_path.exists():
            continue

        for current_dir, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES and not d.startswith(".")]

            for filename in filenames:
                if needle in filename.lower():
                    matches.append(Path(current_dir) / filename)
                    if len(matches) >= max_results:
                        return matches

    return matches


def is_too_large(path: Path) -> bool:
    return path.stat().st_size > MAX_TELEGRAM_FILE_SIZE
