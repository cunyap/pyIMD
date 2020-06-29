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


class BookKeeper:

    def __init__(self):
        """
        Constructor.
        """

        self.timepoint = 0
        self.image_paths = [
            resource_path('ui/icons/pyIMD_logo.png')]
        self.initBookkeeper()

    def addImagePath(self, image_path):
        self.image_paths = image_path
        self.initBookkeeper()

    def initBookkeeper(self):
        self.num_timepoints = len(self.image_paths)
        self.images = self.num_timepoints * [None]
        self.compositeLines = self.num_timepoints * [None]
        self.compositePolygons = self.num_timepoints * [None]
        print(self.image_paths)

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
        print(compositeLine)
        self.compositeLines[self.timepoint] = compositeLine

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

    def getCurrentImagePath(self):
        """
        Return current image for display.
        """
        return self.image_paths[self.timepoint]
