# We need this for sys.argv (command line arguments) and sys.exit()
import sys

# I'm using PySide6, which is the official binding for Qt for Python:
# https://doc.qt.io/qtforpython-6/
# QApplication manages the GUI application's control flow and main settings.
# There can only be ONE QApplication instance per application.
from PySide6.QtWidgets import QApplication

# Import the MainWindow
from gcode_generator.ui.main_window import MainWindow


def main():
    """
    The main function that starts our application.
    This is the entry point of our GUI program.
    """
    # sys.argv is passed to allow command line arguments to control the application.
    # For example: '--style fusion' could change the application's look.
    app = QApplication(sys.argv)

    # Create an instance of our main window.
    window = MainWindow()

    # Windows are hidden by default, so we need to show them explicitly.
    window.show()

    # app.exec() starts Qt's event loop.
    # sys.exit() ensures the Python script exits with the proper code when the app is closed.
    sys.exit(app.exec())


# If this file is run directly, call the main() function to start the application.
if __name__ == "__main__":
    main()
