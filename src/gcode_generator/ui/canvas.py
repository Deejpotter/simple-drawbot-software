# Basic UI elements (QWidget base class).
from PySide6.QtWidgets import QWidget
# Fundamental classes (Qt namespace for constants, QPoint for coordinates).
from PySide6.QtCore import Qt, QPoint
# Classes for graphics (painting, colors, paths).
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath
# Type hints for better code clarity.
from typing import List, Optional


class DrawingCanvas(QWidget):
    """
    A custom widget for freehand drawing with grid support.
    Inherits from QWidget to create a paintable canvas area.
    Reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Drawing state variables.
        self.drawing = False  # True when user is actively drawing.
        self.last_point = None  # Stores the last mouse position.
        # Path being currently drawn. The Optional type allows None as a valid value if no path exists.
        self.current_path: Optional[QPainterPath] = None
        self.paths: List[QPainterPath] = []  # List of completed paths.

        # Grid configuration
        self.grid_size = 20  # Size of grid squares in pixels.
        self.show_grid = True  # Toggle for grid visibility.

        # Set white background for the canvas.
        # setAutoFillBackground must be True for background color to work.
        self.setAutoFillBackground(True)
        # When you assign a new palette to a widget, the color roles from this palette are combined with the widget’s default palette to form the widget’s final palette.
        # Reference: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html#PySide6.QtWidgets.QWidget.palette
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(palette)

        # Enable mouse tracking to receive mouse move events even when no button is pressed.
        self.setMouseTracking(True)

    def paintEvent(self, event):
        """
        Qt override: Called whenever the widget needs to be repainted.
        Handles drawing of grid and all paths.
        Reference: https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPaintEvent.html
        """
        painter = QPainter(self)
        # Enable antialiasing for smoother lines
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw grid if enabled
        if self.show_grid:
            self.draw_grid(painter)

        # Draw all completed paths
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        for path in self.paths:
            painter.drawPath(path)

        # Draw the path currently being created
        if self.current_path:
            painter.drawPath(self.current_path)

    def draw_grid(self, painter: QPainter):
        """
        Draws the background grid using the specified grid size.
        Uses light grey color for grid lines.
        Reference: https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html
        """
        # Set up the pen for grid lines.
        pen = QPen(QColor(200, 200, 200), 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # Draw vertical grid lines.
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())

        # Draw horizontal grid lines.
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)

    def mousePressEvent(self, event):
        """
        Qt override: Handles mouse press events.
        Starts a new path when left button is pressed.
        See: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.pos())
            self.update()  # Schedule a repaint

    def mouseMoveEvent(self, event):
        """
        Qt override: Handles mouse move events.
        Adds points to current path while drawing.
        See: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        """
        if self.drawing and self.last_point:
            self.current_path.lineTo(event.pos())
            self.last_point = event.pos()
            self.update()  # Schedule a repaint

    def mouseReleaseEvent(self, event):
        """
        Qt override: Handles mouse release events.
        Completes the current path and adds it to the paths list.
        See: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        """
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            if self.current_path:
                self.paths.append(self.current_path)
                self.current_path = None
            self.update()  # Schedule a repaint

    def clear(self):
        """Clear all drawings from the canvas"""
        self.paths.clear()
        self.current_path = None
        self.update()  # Schedule a repaint

    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.update()  # Schedule a repaint

    def set_grid_size(self, size: int):
        """
        Set grid size with a minimum value of 5 pixels
        Args:
            size: The desired grid size in pixels
        """
        self.grid_size = max(5, size)  # Ensure minimum grid size
        self.update()  # Schedule a repaint
