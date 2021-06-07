# /********************************************************************************
# * Copyright © 2018-2020, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the GNU Public License v3.0
# * which accompanies this distribution, and is available at
# * http://www.gnu.org/licenses/gpl
# *
# * Contributors:
# *     Aaron Ponti - initial API
# *     Andreas P. Cuny - initial API and final implementation
# *******************************************************************************/

from PyQt5.QtGui import QColor, QPen, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsLineItem
from PyQt5.QtCore import Qt


class Line(QGraphicsLineItem):
    """A line."""

    def __init__(self, x0, y0, x, y, name, composite):
        """Constructor."""

        self._name = name
        self._composite = composite

        width = x - x0
        height = y - y0

        # Call parent constructor
        super(Line, self).__init__(0, 0, width, height, parent=None)

        # Now place it at the correct position in the scene
        self.setPos(x0, y0)

        self.setPen(QPen(QColor(148, 85, 141), 0.5))
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def name(self):
        return self._name

    def mousePressEvent(self, event):
        self._composite.setSelectedItemAndOrigin(self, event.scenePos())
        super(Line, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self._composite.itemMovedTo(self, event.scenePos())
        super(Line, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._composite.setSelectedItemAndOrigin(None, None)
        super(Line, self).mouseReleaseEvent(event)