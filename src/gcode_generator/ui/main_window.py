from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMenuBar,
    QStatusBar
)


class MainWindow(QMainWindow):
    """
    Main window of the application.
    The main window contains the menu bar, status bar, and the central widget.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("G-Code Generator")
        self.setup_ui()

    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        layout = QVBoxLayout(central_widget)

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Set window size
        self.resize(800, 600)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit")

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings")
