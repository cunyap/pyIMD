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

from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
import pyqtgraph as pg
from pyIMD.ui.poscorrection.vertex import Vertex
from pyIMD.ui.poscorrection.line import Line
from pyIMD.ui.poscorrection.polygon import Polygon
from pyIMD.ui.poscorrection.polygonVertex import PolygonVertex
from pyIMD.ui.poscorrection.circle import Circle
from pyIMD.ui.poscorrection.image_filter import filter_image
from pyIMD.ui.poscorrection.compositeLine import CompositeLine
from skimage.io import imread
from skimage.color import rgb2gray, rgba2rgb
from scipy import ndimage


class Scene(QGraphicsScene):
    """
    The main Scene.
    """

    signal_add_object_at_position = \
        pyqtSignal(float, float, name='signal_add_object_at_position')

    def __init__(self, image, x=0, y=0, width=500, height=500, parent=None):
        super().__init__(x, y, width, height, parent)
        self.setSceneRect(0, 0, width, height)

        self.image = image

    def display_image(self, image_path=None, image_filter=None):
        """
        Stores and displays an image
        :param image_path: full path to the image to display
        :param image_filter: If not none an image filter as specified in a dict will be used to filter the image
        :return: void
        """

        # Open the image
        if image_path is not None:
            # image = imageio.imread(image_path).T
            img = imread(image_path)
            if img.shape[2] == 4:
                gray = rgb2gray(rgba2rgb(img))
            else:
                gray = rgb2gray(imread(image_path))

            image = ndimage.rotate(gray, -90)

            if image_filter is not None:
                image = filter_image(image, image_filter)

            if not image.dtype == 'uint8':
                image = image / 256
                image.astype('uint8')
            self.image = pg.ImageItem(image)

        if self.image is None:
            return

        # Show the image (and store it)
        self.image.render()
        self.pixMap = QPixmap.fromImage(self.image.qimage)

        # If needed, remove last QPixMap from the scene
        for item in self.items():
            if type(item) is QGraphicsPixmapItem:
                self.removeItem(item)
                del item

        item = self.addPixmap(self.pixMap)
        self.update()
        item.setTransformOriginPoint(item.boundingRect().center())

        # Reset the scene size
        self.setSceneRect(0, 0, self.image.width(), self.image.height())

    def paintEvent(self, event):
        if not self.pixMap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.pixMap)

    def resizeEvent(self, event):
        if not self.pixMap.pixmap().isNull():
            self.fitInView(self.pixMap, Qt.KeepAspectRatio)
        super(QGraphicsScene, self).resizeEvent(event)

    def removeCompositeLine(self):
        """
        Remove CompositeLine if it exists from the scene, but does not
        delete the object.
        """
        for item in self.items():
            if type(item) is CompositeLine or \
                    type(item) is Line or \
                    type(item) is Vertex:
                self.removeItem(item)

    def removeCompositePolygon(self):
        """
        Remove CompositePolygon if it exists from the scene, but does not
        delete the object.
        """
        for item in self.items():
            if type(item) is Polygon or \
                type(item) is PolygonVertex or \
                    type(item) is Circle:
                self.removeItem(item)

    def mousePressEvent(self, event):
        """
        Process a mouse press event on the scene.
        :param event: A mouse press event.
        :return:
        """
        if event.buttons() == Qt.LeftButton:
            x = event.scenePos().x()
            y = event.scenePos().y()
            self.signal_add_object_at_position.emit(x, y)

        else:
            pass

        super().mousePressEvent(event)

