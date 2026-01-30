# run_desktop.py (Windows) - run Streamlit in-process (prevents process storm)
from __future__ import annotations

import os
import socket
import sys
import time
import webbrowser
from pathlib import Path

APP_NAME = "CVBuilder"


def _user_data_dir() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    p = Path(base) / APP_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))  # type: ignore[attr-defined]
    return os.path.join(base, rel_path)


def pick_free_port(preferred: int = 8501) -> int:
    for port in [preferred, 8502, 8503, 0]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return s.getsockname()[1]
            except OSError:
                continue
    return 8501


def open_browser_once(url: str) -> None:
    lock = _user_data_dir() / "browser_opened.lock"
    if lock.exists():
        return
    try:
        lock.write_text(str(time.time()), encoding="utf-8")
    except Exception:
        pass
    webbrowser.open_new_tab(url)


def main() -> None:
    # Hard-disable dev/watch modes that cause loops in frozen builds
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_GLOBAL_DEVELOPMENT_MODE", "false")
    os.environ.setdefault("STREAMLIT_SERVER_RUN_ON_SAVE", "false")
    os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")
    os.environ.setdefault("PYTHONUTF8", "1")

    app_path = resource_path("app.py")

    port_env = os.environ.get("CVBUILDER_PORT", "").strip()
    preferred_port = int(port_env) if port_env.isdigit() else 8501
    port = pick_free_port(preferred=preferred_port)

    url = f"http://127.0.0.1:{port}"

    # Open browser once
    time.sleep(0.8)
    open_browser_once(url)

    # Run Streamlit IN-PROCESS (no subprocess recursion)
    from streamlit.web import cli as stcli  # noqa

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.address",
        "127.0.0.1",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--server.runOnSave",
        "false",
        "--server.fileWatcherType",
        "none",
        "--browser.gatherUsageStats",
        "false",
    ]

    stcli.main()


if __name__ == "__main__":
    main()
