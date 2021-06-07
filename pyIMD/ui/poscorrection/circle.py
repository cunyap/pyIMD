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

from PyQt5.QtWidgets import QGraphicsEllipseItem


class Circle(QGraphicsEllipseItem):
    """A vertex."""

    def __init__(self, x, y, radius=2, name="", composite=None):
        """Constructor."""

        self._diameter = 2 * radius
        self._radius = radius
        self._name = name
        self._composite = composite

        # Call the parent constructor
        super(Circle, self).__init__(0, 0, self._diameter, self._diameter, parent=None)
