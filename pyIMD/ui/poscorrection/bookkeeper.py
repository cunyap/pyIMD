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

from pyIMD.ui.resource_path import resource_path
from pyIMD.ui.poscorrection.compositeLine import CompositeLine
from pyIMD.ui.poscorrection.compositePolygon import CompositePolygon
from pathlib import Path


class BookKeeper:

    def __init__(self):
        """
        Constructor.
        """

        self.timepoint = 0
        self.image_paths = [
            resource_path(str(Path('ui', 'icons', 'pyIMD_logo.png')))]
        self.initBookkeeper()

    def addImagePath(self, image_path):
        self.image_paths = image_path
        self.initBookkeeper()

    def initBookkeeper(self):
        self.num_timepoints = len(self.image_paths)
        self.images = self.num_timepoints * [None]
        self.compositeLines = self.num_timepoints * [None]
        self.compositePolygons = self.num_timepoints * [None]

    def getCurrentTimepoint(self):
        """
          Get the current timepoint.
        """
        return self.timepoint

    def getCurrentCompositeLine(self):
        """
        Get CompositeLine for current timepoint (or None if it does not exist).
        """
        return self.compositeLines[self.timepoint]

    def getAllCompositeLine(self):
        """
        Get AllCompositeLine for all timepoints (or None if it does not exist).
        """
        return self.compositeLines

    def addCompositeLine(self, compositeLine):
        """
        Add a CompositeLine at current timepoint.
        """
        self.compositeLines[self.timepoint] = compositeLine

    def removeCompositeLine(self):
        """
        Removes the CompositeLine from the bookKeeper.
        """
        self.compositeLines[self.timepoint] = None

    def getCurrentCompositePolygon(self):
        """
        Get CompositePolygon for current timepoint (or None if it does not exist).
        """
        return self.compositePolygons[self.timepoint]

    def getAllCompositePolygon(self):
        """
        Get AllCompositePolygon for all timepoints (or None if it does not exist).
        """
        return self.compositePolygons

    def addCompositePolygon(self, compositePolygon):
        """
        Add a CompositePolygon at current timepoint.
        """
        self.compositePolygons[self.timepoint] = compositePolygon

    def copyPreviousCompositePolygon(self, scene):
        """
        copy previous CompositePolygon and CompositeLine at current timepoint.
        """

        if self.timepoint >= 1:

            previous_polygon = self.compositePolygons[self.timepoint - 1]
            previous_line = self.compositeLines[self.timepoint - 1]

            # Create a new CompositePolygon instance
            new_composite_polygon = CompositePolygon()
            new_composite_polygon.addToScene(scene)

            # Copy the vertices from current polygon
            items = previous_polygon._polygon_item.polygon_vertex_items
            for item in items:
                new_composite_polygon._polygon_item.add_vertex(item.pos())

            # Create a new CompositePolygon instance
            new_composite_line = CompositeLine(previous_line.pos)
            # Copy the vertices from current line
            new_composite_line._line.setLine(previous_line._line.line().p1().x(), previous_line._line.line().p1().y(),
                                             previous_line._line.line().p2().x(), previous_line._line.line().p2().y())
            new_composite_line._vertexA.setPos(previous_line._vertexA.scenePos())
            new_composite_line._vertexB.setPos(previous_line._vertexB.scenePos())

            # Copy previous polygon
            self.compositePolygons[self.timepoint] = new_composite_polygon
            # Copy previous line
            self.compositeLines[self.timepoint] = new_composite_line

    def addCompositePolygonAllTime(self, scene):
        """
        add current CompositePolygon and CompositeLine at all timepoint.
        """

        current_polygon = self.compositePolygons[self.timepoint]
        current_line = self.compositeLines[self.timepoint]

        for ix, item in enumerate(self.compositePolygons):
            # Create a new CompositePolygon instance
            new_composite_polygon = CompositePolygon()
            new_composite_polygon.addToScene(scene)

            # Copy the vertices from current polygon
            items = current_polygon._polygon_item.polygon_vertex_items
            for item in items:
                new_composite_polygon._polygon_item.add_vertex(item.pos())

            # Create a new CompositePolygon instance
            new_composite_line = CompositeLine(current_line.pos)
            # Copy the vertices from current line
            new_composite_line._line.setLine(current_line._line.line().p1().x(), current_line._line.line().p1().y(),
                                             current_line._line.line().p2().x(), current_line._line.line().p2().y())
            new_composite_line._vertexA.setPos(current_line._vertexA.scenePos())
            new_composite_line._vertexB.setPos(current_line._vertexB.scenePos())

            # Add the new polygon to the list
            self.compositePolygons[ix] = new_composite_polygon
            self.compositeLines[ix] = new_composite_line

    def removeCompositePolygon(self):
        """
        Removes the compositePolygons from the bookKeeper.
        """
        self.compositePolygons[self.timepoint] = None

    def getCurrentImagePath(self):
        """
        Return current image for display.
        """
        return self.image_paths[self.timepoint]
