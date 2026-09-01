"""
omira_app.py — turns Omira into a real desktop application.

Instead of running `python new_omira.py` in a terminal every time, this
gives you a system-tray icon: right-click it for Start/Stop/Quit, and
Omira's listening loop runs in a background thread. This file becomes the
entry point PyInstaller packages into an .exe (see build_app.md).

Setup:
    pip install PyQt5   # already in requirements.txt
Put this file next to new_omira.py.
"""

import sys
import threading

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal

import new_omira  # your existing assistant module — unchanged


class OmiraController(QObject):
    status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._thread = None
        self._running = False

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_omira, daemon=True)
        self._thread.start()
        self.status_changed.emit("running")

    def _run_omira(self):
        try:
            new_omira.main()
        except Exception as exc:
            print(f"[omira_app] Omira stopped unexpectedly: {exc}")
        finally:
            self._running = False
            self.status_changed.emit("stopped")

    def stop(self):
        new_omira.RUNNING = False
        self._running = False
        self.status_changed.emit("stopped")


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    controller = OmiraController()

    tray = QSystemTrayIcon(QIcon.fromTheme("audio-input-microphone"))
    tray.setToolTip("Omira")

    menu = QMenu()
    start_action = QAction("Start listening")
    stop_action = QAction("Stop listening")
    quit_action = QAction("Quit")

    start_action.triggered.connect(controller.start)
    stop_action.triggered.connect(controller.stop)
    quit_action.triggered.connect(app.quit)

    menu.addAction(start_action)
    menu.addAction(stop_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()

    controller.start()  # auto-start on launch; remove this line if you'd rather click Start

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
