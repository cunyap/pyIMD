from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem
from PyQt5.QtGui import QPen, QColor, QCursor, QPolygonF, QBrush
from PyQt5.QtCore import Qt
from pyIMD.ui.reference_point import CenterOfMassPoint
from pyIMD.analysis.calculations import calculate_center_of_mass


class ReferenceLineVertex(QGraphicsPathItem):
    circle = QPainterPath()
    circle.addEllipse(QRectF(-10, -10, 20, 20))
    square = QPainterPath()
    square.addRect(QRectF(-15, -15, 30, 30))

    def __init__(self, reference_line_item, index):
        super(ReferenceLineVertex, self).__init__()
        self.reference_line_item = reference_line_item
        self.vertex_index = index

        self.setPath(ReferenceLineVertex.circle)
        self.setBrush(QColor("green"))
        self.setPen(QPen(QColor("green"), 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(11)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        self.setPath(ReferenceLineVertex.square)
        self.setBrush(QColor("red"))
        super(ReferenceLineVertex, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPath(ReferenceLineVertex.circle)
        self.setBrush(QColor("green"))
        super(ReferenceLineVertex, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(ReferenceLineVertex, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
            self.reference_line_item.move_vertex(self.vertex_index, value)
        return super(ReferenceLineVertex, self).itemChange(change, value)


class ReferenceLine(QGraphicsPolygonItem):
    def __init__(self, image_index, parent=None):
        super(ReferenceLine, self).__init__(parent)
        self.vertices = []
        self.vertices_items = []
        self.image_index = image_index
        self.setZValue(10)
        self.setPen(QPen(QColor("green"), 2))
        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def number_of_vertices(self):
        return len(self.vertices_items)

    def add_vertex(self, p):
        if self.number_of_vertices() < 2:
            self.vertices.append(p)
            self.setPolygon(QPolygonF(self.vertices))
            item = ReferenceLineVertex(self, len(self.vertices) - 1)
            # self.scene().addItem(item)
            self.vertices_items.append(item)
            print('Add vertex at position:', p)
            item.setPos(p)

    def delete_last_vertex(self):
        if self.vertices:
            self.vertices.pop()
            self.setPolygon(QPolygonF(self.vertices))
            it = self.vertices_items.pop()
            self.scene().clear()
            self.scene().removeItem(it)
            del it

    def move_vertex(self, i, p):
        if 0 <= i < len(self.vertices):
            self.vertices[i] = self.mapFromScene(p)
            self.setPolygon(QPolygonF(self.vertices))

    def move_vertices_item(self, index, pos):
        if 0 <= index < len(self.vertices_items):
            vertex_item = self.vertices_items[index]
            vertex_item.setEnabled(False)
            vertex_item.setPos(pos)
            vertex_item.setEnabled(True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for i, point in enumerate(self.vertices):
                self.move_vertices_item(i, self.mapToScene(point))
        return super(ReferenceLine, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor(255, 0, 0, 100))
        super(ReferenceLine, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.NoBrush))
        super(ReferenceLine, self).hoverLeaveEvent(event)


class CellShapeOutline(QGraphicsPolygonItem):
    def __init__(self, image_index, parent=None):
        super(CellShapeOutline, self).__init__(parent)
        self.vertices = []
        self.vertices_in_scene = []
        self.vertices_items = []
        self.image_index = image_index
        self.center_of_mass = []
        self.center_of_mass_item = []
        self.center_of_mass_item2 = []

        self.setZValue(5)
        self.setPen(QPen(QColor("green"), 2))
        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def number_of_vertices(self):
        return len(self.vertices_items)

    def add_vertex(self, p):
        self.vertices.append(p)
        self.vertices_in_scene.append(p)
        self.setPolygon(QPolygonF(self.vertices))
        vertex_item = CellShapeOutlineVertex(self, len(self.vertices) - 1, self.image_index)
        #self.scene().addItem(vertex_item)
        self.vertices_items.append(vertex_item)
        vertex_item.setPos(p)

    def delete_last_vertex(self):
        if self.vertices:
            self.vertices.pop()
            self.setPolygon(QPolygonF(self.vertices))
            it = self.vertices_items.pop()
            # self.scene().removeItem(it)
            return it
            del it

    # def set_new_pos(self, i, p):
    #     if 0 <= i < len(self.vertices):
    #         self.vertices[i] = self.mapToScene(p)
    #         self.setPolygon(QPolygonF(self.vertices))

    def move_vertex(self, i, p):
        if 0 <= i < len(self.vertices):
            self.vertices[i] = p
            #self.vertices[i] = p
            self.setPolygon(QPolygonF(self.vertices))

    def move_vertex2(self, i, p):
        if 0 <= i < len(self.vertices):
            self.vertices[i] = self.mapFromScene(p)
            #self.vertices[i] = p
            self.setPolygon(QPolygonF(self.vertices))

    def move_vertices_in_scene(self, i, p):
        if i == 0:
            print(self.mapFromParent(p))
        self.vertices_in_scene[i] = p

    #def on_drag_vertex_finished(self):
    #     for i in range(0,len(self.vertices)):
    #         #self.vertices[i] = self.mapFromScene(p)
    #         self.vertices[i] = self.mapToScene(p)
    #         print('m pos', p)
    #         self.setPolygon(QPolygonF(self.vertices))

    def move_vertices_item(self, index, pos):
        if 0 <= index < len(self.vertices_items):
            vertex_item = self.vertices_items[index]
            vertex_item.setEnabled(False)
            #print(self.mapToScene(pos))
            vertex_item.setPos(self.mapToScene(pos))
            vertex_item.setEnabled(True)
            self.move_vertex(index, pos)

    def move_center_of_mass(self, index, pos):
        if self.center_of_mass_item:
            #self.determine_center_of_mass()
            center_of_mass_item = self.center_of_mass_item
            try:
                center_of_mass_item.setEnabled(False)
                center_of_mass_item.setPos(self.mapToScene(pos))
                center_of_mass_item.setEnabled(True)
            except Exception as e:
                print(e)

    def determine_center_of_mass(self):
        if len(self.vertices) > 3:
            vertices = []
            for i in range(len(self.vertices)):
                # print('vertex pos', self.mapToScene(QPointF(self.vertices[i].x(), self.vertices[i].y())))
                vertices.append([self.vertices[i].x(), self.vertices[i].y()])
            self.center_of_mass = calculate_center_of_mass(vertices)
            # print('Center of Mass', self.center_of_mass)
            # print('Center of Mass', QPointF(self.center_of_mass[0], self.center_of_mass[1]))
            # print('Center of Mass', self.mapFromScene(QPointF(self.center_of_mass[0], self.center_of_mass[1])))
            # print(self.center_of_mass_item)
            if not self.center_of_mass_item:
                # print('a')
                # c_o_m = CenterOfMassPoint(self.image_index, self.center_of_mass[0],  self.center_of_mass[1])
                # c_o_m.add_vertex(QPointF(self.center_of_mass[0],  self.center_of_mass[1]))
                # self.center_of_mass_item = c_o_m
                rp = ReferencePoint(self, 0, self.image_index)
                self.center_of_mass_item = rp
                rp.setPos(QPointF(self.center_of_mass[0],  self.center_of_mass[1]))
            # else:
            #     print(self.center_of_mass_item.pos())
            #     #self.center_of_mass_item.setPos(self.mapFromScene(QPointF(self.center_of_mass[0],  self.center_of_mass[1])))
            #     print(self.center_of_mass_item.pos())
            # #self.scene().addItem(c_o_m)
            # print(self.center_of_mass_item.x(), self.center_of_mass_item.y())
            # print(self.vertices)
            # print('done')
            # self.cell_outline_items = 1 # Add center of mass here.

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for i, point in enumerate(self.vertices):
            #     self.move_vertices_item(i, self.mapToScene(point))
            # self.determine_center_of_mass()
            # self.move_center_of_mass(1, self.mapToScene(QPointF(self.center_of_mass[0], self.center_of_mass[1])))
                #print('pos', self.pos())
                print(self.mapToScene(self.vertices[0]))
                self.move_vertices_item(i, point)
                self.move_vertices_in_scene(i, point)
                self.determine_center_of_mass()
                self.move_center_of_mass(1, (QPointF(self.center_of_mass[0], self.center_of_mass[1])))
        return super(CellShapeOutline, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor(255, 0, 0, 100))
        super(CellShapeOutline, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.NoBrush))
        super(CellShapeOutline, self).hoverLeaveEvent(event)


class CellShapeOutlineVertex(QGraphicsPathItem):
    circle = QPainterPath()
    circle.addEllipse(QRectF(-5, -5, 10, 10))
    square = QPainterPath()
    square.addRect(QRectF(-5, -5, 10, 10))

    def __init__(self, cell_shape_outline_item, index, image_index):
        super(CellShapeOutlineVertex, self).__init__()
        self.cell_shape_outline_item = cell_shape_outline_item
        self.vertex_index = index
        self.image_index = image_index

        self.setPath(CellShapeOutlineVertex.circle)
        self.setBrush(QColor("green"))
        self.setPen(QPen(QColor("green"), 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        self.setPath(CellShapeOutlineVertex.square)
        self.setBrush(QColor("red"))
        super(CellShapeOutlineVertex, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPath(CellShapeOutlineVertex.circle)
        self.setBrush(QColor("green"))
        super(CellShapeOutlineVertex, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(CellShapeOutlineVertex, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.cell_shape_outline_item.move_vertex(self.vertex_index, value)
            self.cell_shape_outline_item.move_vertex2(self.vertex_index, value)
            self.cell_shape_outline_item.determine_center_of_mass()
            try:
                self.cell_shape_outline_item.move_center_of_mass(1, (QPointF(
                    self.cell_shape_outline_item.center_of_mass[0], self.cell_shape_outline_item.center_of_mass[1])))
            except Exception as e:
                print(e)
        return super(CellShapeOutlineVertex, self).itemChange(change, value)


class ReferencePoint(QGraphicsPathItem):

    square = QPainterPath()
    square.addRect(QRectF(-5, -5, 10, 10))

    def __init__(self, annotation_item, index, image_index):
        super(ReferencePoint, self).__init__()

        self.image_index = image_index
        self.index = index
        self.m_annotation_item = annotation_item

        self.setPath(ReferencePoint.square)
        self.setPen(QPen(QColor(148, 85, 141), 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        self.setPath(ReferencePoint.square)
        self.setPen(QPen(QColor("red"), 2))
        super(ReferencePoint, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPath(ReferencePoint.square)
        self.setPen(QPen(QColor(148, 85, 141), 2))
        super(ReferencePoint, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(ReferencePoint, self).mouseReleaseEvent(event)
