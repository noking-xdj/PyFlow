# Pyflow an open-source tool for modular visual programing in python
# Copyright (C) 2021-2022 Mathïs FEDERICO <https://www.gnu.org/licenses/>
# pylint:disable=wrong-import-position

""" Pyflow main module. """

import os
import sys
import asyncio

if os.name == "nt":  # If on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from PyQt5.QtWidgets import QApplication
from pyflow.graphics.window import Window


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    wnd = Window()
    if len(sys.argv) > 1:
        wnd.createNewMdiChild(sys.argv[1])

    wnd.setWindowTitle("Pyflow Beta v0.1")
    wnd.show()
    sys.exit(app.exec_())