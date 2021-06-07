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

import alphashape
from PyQt5.QtGui import QColor, QPen, QCursor, QPolygonF, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPolygonItem
from PyQt5.QtCore import Qt, QPointF
from pyIMD.ui.poscorrection.polygonVertex import PolygonVertex
from pyIMD.ui.poscorrection.circle import Circle


class Polygon(QGraphicsPolygonItem):
    def __init__(self, composite, parent=None):
        super(Polygon, self).__init__(parent)
        self._composite = composite
        self.polygon_vertices = []
        self.setZValue(10)
        self.setPen(QPen(QColor(0, 255, 0, 90), 0.5))
        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.polygon_vertex_items = []
        self.center_of_mass_item = []

        self._centerOfMass = None
        self._area = None

    def number_of_points(self):
        return len(self.polygon_vertex_items)

    def add_vertex(self, p):
        self.polygon_vertices.append(p)
        self.setPolygon(QPolygonF(self.polygon_vertices))
        item = PolygonVertex(p.x(), p.y(), 2, len(self.polygon_vertices) - 1, self, self._composite)
        self.scene().addItem(item)
        self.polygon_vertex_items.append(item)
        item.setPos(p)
        # if len(self.polygon_vertex_items) == 1:
        #     item = Circle(p.x(), p.y(), 7, 'CoM', self._composite)
        #     self.scene().addItem(item)
        #     self.center_of_mass_item.append(item)
        #     item.setPos(p)
        self.updateCenterOfMass()

    def remove_last_vertex(self):
        if self.polygon_vertices:
            self.polygon_vertices.pop()
            self.setPolygon(QPolygonF(self.polygon_vertices))
            it = self.polygon_vertex_items.pop()
            self.scene().removeItem(it)
            del it
            self.updateCenterOfMass()

    def move_vertex(self, i, p):
        if 0 <= i < len(self.polygon_vertices):
            self.polygon_vertices[i] = self.mapFromScene(p)
            self.setPolygon(QPolygonF(self.polygon_vertices))

    def move_vertex_item(self, index, pos):
        if 0 <= index < len(self.polygon_vertex_items):
            item = self.polygon_vertex_items[index]
            item.setEnabled(False)
            item.setPos(pos)
            item.setEnabled(True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for i, point in enumerate(self.polygon_vertices):
                self.move_vertex_item(i, self.mapToScene(point))
        return super(Polygon, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor(255, 0, 0, 100))
        super(Polygon, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.NoBrush))
        super(Polygon, self).hoverLeaveEvent(event)

    def updateCenterOfMass(self):
        if len(self.polygon_vertex_items) == 0:
            return None

        sum_x = 0.0
        sum_y = 0.0
        for item in self.polygon_vertex_items:
            sum_x += item.x()
            sum_y += item.y()
        x = sum_x / len(self.polygon_vertex_items)
        y = sum_y / len(self.polygon_vertex_items)
        self._centerOfMass = QPointF(x, y)

        # Move the center of mass item on the scene
        # item = self.center_of_mass_item[0]
        # item.setEnabled(False)
        # item.setPos(self.mapFromScene(self._centerOfMass))
        # item.setEnabled(True)
        return self._centerOfMass

    def updateArea(self):
        coordinates = []
        for item in self.polygon_vertices:
            coordinates.append((item.x(), item.y()))
        alpha_shape = alphashape.alphashape(coordinates)
        self._area = alpha_shape.area

    def vertices_to_dict(self):
        x = []
        y = []
        for item in self.polygon_vertices:
            x.append(item.x())
            y.append(item.y())
        vertices = {'x': x, 'y': y}
        return vertices
