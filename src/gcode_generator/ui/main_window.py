# Import required Qt widgets for building our main window
# QMainWindow: The main application window
# QWidget: Base class for all UI objects
# QVBoxLayout: Vertical layout manager
# Other imports: Various UI elements we need (menus, toolbars, buttons)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMenuBar,
    QStatusBar,
    QToolBar,
    QSpinBox,
    QPushButton
)

# Qt.ToolBarArea helps position the toolbar.
from PySide6.QtCore import Qt

# QAction represents an abstract user interface action.
# These are used for menu items and toolbar buttons.
from PySide6.QtGui import QAction

# Import the custom canvas widget that handles the drawing.
from .canvas import DrawingCanvas


class MainWindow(QMainWindow):
    """
    This is the main application window that holds all other widgets.
    I'm using QMainWindow as the base class because it provides a lot of built-in functionality.
    Reference: https://doc.qt.io/qt-6/qmainwindow.html#public-functions
    """
    def __init__(self):
        super().__init__()
        self.statusBar = QStatusBar()
        self.setWindowTitle("G-Code Generator")
        # Create the drawing canvas first so we can reference it later.
        self.canvas = DrawingCanvas()
        self.setup_ui()

    def setup_ui(self):
        # QMainWindow needs a central widget to hold everything.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Use QVBoxLayout to arrange widgets vertically.
        layout = QVBoxLayout(central_widget)

        # Set up the main UI components.
        self.create_menu_bar()
        self.create_tool_bar()

        # Add the drawing canvas to the layout.
        layout.addWidget(self.canvas)

        # Set the status bar to the initialized QStatusBar.
        self.setStatusBar(self.statusBar)

        # Set a reasonable default window size.
        self.resize(800, 600)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Create the main menu items
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()  # Add a line.
        file_menu.addAction("Exit")

        # Edit menu with canvas clearing functionality
        edit_menu = menubar.addMenu("Edit")

        # Connect the clear action to the canvas's clear method.
        clear_action = QAction("Clear Canvas", self)
        clear_action.triggered.connect(self.canvas.clear)
        edit_menu.addAction(clear_action)

        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # View menu with grid toggle functionality
        view_menu = menubar.addMenu("View")
        toggle_grid_action = QAction("Toggle Grid", self)
        toggle_grid_action.triggered.connect(self.canvas.toggle_grid)
        view_menu.addAction(toggle_grid_action)

        # Tools menu for application settings
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings")

    def create_tool_bar(self):
        # Create a toolbar and add it to the left side of the window
        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)

        # Add a spacer widget to position controls
        toolbar.addWidget(QWidget())

        # Add a spin box for controlling grid size.
        # Reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSpinBox.html
        # A spin box allows users to select a value from a predefined range for use as parameters in the application (e.g. brush size, grid size).
        grid_size_spin = QSpinBox()
        grid_size_spin.setRange(5, 100)
        grid_size_spin.setValue(20)
        grid_size_spin.setSingleStep(5)
        grid_size_spin.valueChanged.connect(self.canvas.set_grid_size)
        toolbar.addWidget(grid_size_spin)

        # Add a clear button to the toolbar and connect it to the canvas's clear method.
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.canvas.clear)
        toolbar.addWidget(clear_btn)
