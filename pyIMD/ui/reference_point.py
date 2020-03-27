from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QColor, QCursor, QPolygonF, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QLineF


class ReferencePoint(QGraphicsPathItem):

    def __init__(self, annotation_item, image_index):
        super(ReferencePoint, self).__init__()

        square = QPainterPath()
        square.addRect(0,0, 10, 10)

        self.image_index = image_index
        self.m_annotation_item = annotation_item

        self.setPath(square)
        self.setPen(QPen(QColor("green"), 1))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        print('HOVER')
        self.setPath(ReferencePoint.square)
        self.setPen(QPen(QColor("red"), 1))
        super(ReferencePoint, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPath(ReferencePoint.square)
        self.setPen(QPen(QColor("green"), 1))
        super(ReferencePoint, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(ReferencePoint, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            print('before')
            # self.m_annotation_item.move_vertex(self.id, value)
            print('executed that')
        return super(ReferencePoint, self).itemChange(change, value)


class CenterOfMassPoint(QGraphicsPathItem):

    def __init__(self, image_index, x, y):
        super(CenterOfMassPoint, self).__init__()

        point = QPainterPath()
        point.addEllipse(QRectF(x-5, y-5, 10, 10))
        self.image_index = image_index
        self.vertices = []
        self.vertices_items = []


        self.setPath(point)
        #self.setBrush(QColor("green"))
        self.setPen(QPen(QColor("green"), 1))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def add_vertex(self, p):
        print('here')
        self.vertices = p
        print('a')
        print(p.x())
        item = ReferencePoint(self, 0)
        print('there')
        # self.scene().addItem(item)
        self.vertices_items = item
        print('Add vertex at position:', p)
        item.setPos(p)

    # def hoverEnterEvent(self, event):
    #     self.setPen(QPen(QColor("red"), 1))
    #     super(ReferencePoint, self).hoverEnterEvent(event)
    #
    # def hoverLeaveEvent(self, event):
    #     self.setPen(QPen(QColor("green"), 1))
    #     super(ReferencePoint, self).hoverLeaveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     self.setSelected(False)
    #     super(ReferencePoint, self).mouseReleaseEvent(event)
    #
    # def itemChange(self, change, value):
    #     if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
    #         #self.m_annotation_item.move_vertex(self.m_index, value)
    #         print('executed that')
    #     return super(ReferencePoint, self).itemChange(change, value)

from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem, QGraphicsLineItem
from PyQt5.QtGui import QPen, QColor, QCursor, QPolygonF, QBrush
from PyQt5.QtCore import Qt, QPoint


class ReferenceLine(QGraphicsLineItem):
    def __init__(self, image_index, parent=None):
        super(ReferenceLine, self).__init__(parent)
        self.vertices = []
        self.cell_outline_items = []
        self.image_index = image_index

        self.setZValue(5)
        self.setPen(QPen(QColor("green"), 1))
        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        #self.setLine(0,0,100,100)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def number_of_vertices(self):
        return len(self.cell_outline_items)

    def add_vertex(self, p):
        self.vertices.append(p)
        print('ok')
        #self.setLine(QPolygonF(self.vertices))
        print('ok')
        cell_outline_item = ReferencePoint(self.image_index, len(self.vertices) - 1, p, self)
        print('d')
        self.scene().addItem(cell_outline_item)
        print('d')
        self.cell_outline_items.append(cell_outline_item)
        print('d3')
        cell_outline_item.setPos(p)
        print('end add', self.vertices)

        # self.determine_center_of_mass()

    def delete_last_vertex(self):
        if self.vertices:
            self.vertices.pop()
            # self.setLine(QPolygonF(self.vertices))
            it = self.cell_outline_items.pop()
            self.scene().removeItem(it)
            del it

    def set_new_pos(self, i, p):
        if 0 <= i < len(self.vertices):
            self.vertices[i] = self.mapToScene(p)
            # self.setLine(QPolygonF(self.vertices))

    def move_vertex(self, i, p):
        print(i,p)
        if 0 <= i < len(self.vertices):
            self.vertices[i] = self.mapFromScene(p)
            print('Scene mapping', self.mapFromScene(p))
            print(self.vertices[i].x())
            print(p)
            print(self.mapFromScene(p))
            print(self.mapToScene(p))
            # try:
            self.setLine(QLineF(self.vertices[0].x(), self.vertices[0].y(), self.vertices[i].x(), self.vertices[i].y()))
            # except Exception as e:
            #     print(e)

    def set_now_line(self):
        print('trying to set line', self.vertices[0].x(), self.vertices[0].y(), self.vertices[1].x(), self.vertices[1].y())
        if len(self.vertices) > 1:
            self.setLine(self.vertices[0].x(), self.vertices[0].y(), self.vertices[1].x(), self.vertices[1].y())

    def move_object(self, index, pos):
        if 0 <= index < len(self.cell_outline_items):
            cell_outline_item = self.cell_outline_items[index]
            cell_outline_item.setEnabled(False)
            cell_outline_item.setPos(pos)
            cell_outline_item.setEnabled(True)
            self.move_vertex(index, pos)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            print('bla')
            for i, point in enumerate(self.vertices):
                self.move_object(i, self.mapToScene(point))
        return super(ReferenceLine, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        super(ReferenceLine, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        super(ReferenceLine, self).hoverLeaveEvent(event)