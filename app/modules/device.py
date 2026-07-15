import platform
import subprocess


def schedule_shutdown(delay_seconds: int = 60) -> str:
    system = platform.system()
    if system == "Windows":
        subprocess.run(["shutdown", "/s", "/t", str(delay_seconds)], check=True)
    elif system in ("Linux", "Darwin"):
        subprocess.run(["shutdown", "-h", f"+{max(delay_seconds // 60, 1)}"], check=True)
    else:
        raise OSError(f"Unsupported platform: {system}")
    return f"Shutdown scheduled in {delay_seconds} seconds."


def cancel_shutdown() -> str:
    system = platform.system()
    if system == "Windows":
        subprocess.run(["shutdown", "/a"], check=True)
    elif system in ("Linux", "Darwin"):
        subprocess.run(["shutdown", "-c"], check=True)
    else:
        raise OSError(f"Unsupported platform: {system}")
    return "Shutdown cancelled."


def launch_app(path: str) -> str:
    subprocess.Popen([path], shell=False)
    return f"Launched: {path}"
