"""
main.py
Entry point aplikasi To-Do List berbasis PySide6.
Separation of Concerns: hanya menginisialisasi QApplication dan memuat stylesheet.
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from ui.main_window import MainWindow

# Pastikan import relatif bekerja dari direktori mana saja
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_stylesheet(app: QApplication) -> None:
    """Memuat file QSS eksternal dan menerapkannya ke seluruh aplikasi."""
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"[PERINGATAN] File stylesheet tidak ditemukan: {qss_path}")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("To-Do List")
    app.setOrganizationName("Mahasiswa PBO")

    # Font default
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Stylesheet eksternal
    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
