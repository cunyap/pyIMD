# /********************************************************************************
# * Copyright © 2018-2019, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
# * All rights reserved. This program and the accompanying materials
# * are made available under the terms of the GNU Public License v3.0
# * which accompanies this distribution, and is available at
# * http://www.gnu.org/licenses/gpl
# *
# * Contributors:
# *     Andreas P. Cuny - initial API and implementation
# *******************************************************************************/

import sys
from pathlib import Path
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QApplication
from pyIMD.ui.main_ui import IMDWindow
from pyIMD.ui.resource_path import resource_path


def show_ui():
    app = QApplication(sys.argv)
    main = IMDWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path(str(Path("ui", "icons", "pyIMD_logo_icon.ico")))))
    main = IMDWindow()
    main.show()
    sys.exit(app.exec_())
