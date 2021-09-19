# OpenCodeBlock an open-source tool for modular visual programing in python
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Module for the OCB Scene """

import math

from PyQt5.QtCore import QLine, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene


class OCBScene(QGraphicsScene):

    """ Scene for the OCB Window. """

    def __init__(self, parent=None,
            background_color:str="#393939",
            grid_color:str="#292929", grid_light_color:str="#2f2f2f",
            width:int=64000, height:int=64000,
            grid_size:int=20, grid_squares:int=5):
        super().__init__(parent=parent)

        self._background_color = QColor(background_color)
        self._grid_color = QColor(grid_color)
        self._grid_light_color = QColor(grid_light_color)
        self.grid_size = grid_size
        self.grid_squares = grid_squares

        self.width, self.height = width, height
        self.setSceneRect(-self.width//2, -self.height//2, self.width, self.height)
        self.setBackgroundBrush(self._background_color)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        """ Draw the Scene background """
        super().drawBackground(painter, rect)
        self.drawGrid(painter, rect)

    def drawGrid(self, painter: QPainter, rect: QRectF):
        """ Draw the background grid """
        left = int(math.floor(rect.left()))
        top = int(math.floor(rect.top()))
        right = int(math.ceil(rect.right()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # Compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # Draw the lines using the painter
        pen = QPen(self._grid_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLines(*lines_dark)

        pen = QPen(self._grid_light_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLines(*lines_light)