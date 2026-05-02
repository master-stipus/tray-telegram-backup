import logging
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from functools import partial
from pathlib import Path
from threading import Thread

import requests
from dotenv import load_dotenv
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

# Log file in the OS temp folder
LOG_FILE = Path(tempfile.gettempdir()) / f"{str(Path(__file__).parent.name)}.log"
log = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()


def send_document(filepath):
    url = f"https://api.telegram.org/bot{os.getenv('TOKEN')}/sendDocument"
    data = {"chat_id": os.getenv("CHAT_ID")}

    with open(filepath, "rb") as f:
        files = {"document": f}
        r = requests.post(url, data=data, files=files)

    return r


def backup(script):
    """
    Create 7-Zip archive in a temp folder by running backup script and send it
    to Telegram via bot.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Archive name in format scriptname-19840224-205612.7z
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_filename = f"{script.stem}-{timestamp}.7z"
        archive_path = Path(tmpdir) / archive_filename
        log.info("Path to the archive file: %s", archive_path)

        # Absolute path to script file
        script_path = script.resolve()

        try:
            # Random observation: subprocess.run() work with non-string paths?
            subprocess.run(
                [script_path, archive_path], check=True, capture_output=True, text=True
            )
            log.info("Archive created")
        except Exception as e:
            log.error("Error while creating archive: %s", e)

        try:
            r = send_document(archive_path)
            r.raise_for_status()
            log.info("Archive sent with %s HTTP code", r.status_code)
        except Exception as e:
            log.error("Error while sending archive: %s", e)


def view_logs():
    subprocess.run(["kitty", "lnav", LOG_FILE], capture_output=True)


def run_view_logs():
    Thread(target=view_logs).start()


def main():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    app = QApplication(sys.argv)
    menu = QMenu()

    for script in Path("backup_scripts").iterdir():
        # .stem return final component of path without extension
        menu.addAction(script.stem.title(), partial(backup, script))

    menu.addAction("View logs", run_view_logs)  # View logs in separate thread
    menu.addAction("Quit", app.quit)

    tray = QSystemTrayIcon(QIcon("icon.png"))
    tray.setContextMenu(menu)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
