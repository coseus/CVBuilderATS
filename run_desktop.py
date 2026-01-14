import os
import sys
import time
import webbrowser
import subprocess


def resource_path(rel_path: str) -> str:
    """
    Works for PyInstaller onefile/onedir.
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


def main():
    # Ensure Streamlit finds your app.py
    app_path = resource_path("app.py")

    # Prefer localhost fixed port
    port = os.environ.get("CVBUILDER_PORT", "8501")
    url = f"http://localhost:{port}"

    # Start streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]

    # Windows: hide console spam
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW  # type: ignore

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)

    # give it a moment then open browser
    time.sleep(1.2)
    webbrowser.open(url)

    # Wait until streamlit exits
    try:
        p.wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
