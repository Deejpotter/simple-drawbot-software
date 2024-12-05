from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath
from typing import List, Optional


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Drawing settings
        self.drawing = False
        self.last_point = None
        self.current_path: Optional[QPainterPath] = None
        self.paths: List[QPainterPath] = []

        # Canvas settings
        self.grid_size = 20
        self.show_grid = True

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)

        # Enable mouse tracking
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw grid
        if self.show_grid:
            self.draw_grid(painter)

        # Draw all paths
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        for path in self.paths:
            painter.drawPath(path)

        # Draw current path
        if self.current_path:
            painter.drawPath(self.current_path)

    def draw_grid(self, painter: QPainter):
        pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        painter.setPen(pen)

        # Draw vertical lines
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())

        # Draw horizontal lines
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.pos())
            self.update()

    def mouseMoveEvent(self, event):
        if self.drawing and self.last_point:
            self.current_path.lineTo(event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            if self.current_path:
                self.paths.append(self.current_path)
                self.current_path = None
            self.update()

    def clear(self):
        """Clear all drawings from the canvas"""
        self.paths.clear()
        self.current_path = None
        self.update()

    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.update()

    def set_grid_size(self, size: int):
        """Set grid size"""
        self.grid_size = max(5, size)  # Minimum grid size of 5
        self.update()
