# src/main.py
import sys
from PySide6.QtWidgets import QApplication
from gcode_generator.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
