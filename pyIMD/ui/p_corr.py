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
import os
import math
import pandas as pd
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import pyqtSignal, QRegExp, pyqtSlot, Qt, QPointF, QAbstractTableModel
from PyQt5.Qt import QValidator, QDoubleValidator, QRegExpValidator, QStyle, QDialog, QRadioButton, \
    QMainWindow, QApplication, QListWidgetItem, QPixmap, QListWidget, QListView, QGraphicsScene, QGraphicsPixmapItem,\
    QGroupBox, QLabel, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QVBoxLayout, QWidget, QSpacerItem, QPushButton, QSizePolicy, QTextDocumentFragment
from PyQt5.QtWidgets import QShortcut, QToolBar, QAction, QFileDialog, QProgressBar, QMessageBox
from pyIMD.configuration.defaults import *
from pyIMD.ui.resource_path import resource_path
# from pyIMD.ui.WellItemRect import WellItemRect
# from pyIMD.ui.custom_tree_item import WellItem, ReferencePointTreeItem
# from pyIMD.ui.graphics_scene import GraphicScene
# from pyIMD.ui.reference_point import CenterOfMassPoint
# from pyCAME.ui.well_table_model import WellTableModel
# from pyIMD.ui.WellItemRect import WellItemRect
# from pyIMD.ui.app_event_filter import AppEventFilter
from functools import partial
from enum import Enum
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
import pyqtgraph as pg
from pyIMD.ui.graphics_items import ReferenceLine, CellShapeOutline
# from pyIMD.ui.reference_point import ReferencePoint
from pyIMD.analysis.calculations import calculate_center_of_mass
from skimage import exposure
from skimage.morphology import disk
from skimage.filters import rank
from scipy import ndimage
#pg.setConfigOption('background', 'k')
#pg.setConfigOption('foreground', 'w')

__author__ = 'Andreas P. Cuny'


class PositionCorrectionUI(QMainWindow):
    """
    Position Correction user interface implementation.

    """

    save_to_main_signal = pyqtSignal(object, int, int, int, bool, name='save_to_main_signal')
    """
    pyqtSignal sends the data to the main window

    Returns:
        data (`object`):                           Data to be sent to the main window.
    """

    def __init__(self):
        """
        Settings user interface (UI) constructor.

        Returns:
            QDialog (`obj`):     Settings ui object
        """
        super(PositionCorrectionUI, self).__init__()

        uic.loadUi(resource_path(os.path.join('positioncorrectionui\\positioncorrectionui.ui')), self)
        # uic.loadUi(resource_path(os.path.join('ui\\positioncorrectionui.ui')), self)

        self.setWindowTitle('pyIMD :: Position Correction')
        self.draw_reference_line_action = QAction(QIcon(resource_path('scratch_space\\Icons-01.png')), 'Draw new cantilever tip reference line', self)
        self.draw_cell_outline_action = QAction(QIcon(resource_path('scratch_space\\Icons-02.png')), 'Draw new cell outline', self)

        self.draw_item = None
        self.image_file_names = []
        self.reference_line_list = []
        self.cells_list = []
        self.center_of_mass_list = []
        self.tip_offset_list = []
        self.data = []
        self.data_results = []

        self.graphicsView = pg.ImageView()
        self.graphicsView.ui.menuBtn.hide()
        self.graphicsView.ui.roiBtn.hide()
        self.graphicsView.view.setMenuEnabled(False)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.sigTimeChanged.connect(self.on_time_change)
        self.graphicsView.view.sigStateChanged.connect(self.on_view_box_state_change)
        self.graphicsView.setCurrentIndex = self.setCurrentIndex
        self.gridLayout.addWidget(self.graphicsView, 0, 1)
        his = self.graphicsView.getHistogramWidget()
        self.gridLayout.addWidget(his, 0, 2)
        self.graphicsView.view.setBackgroundColor((100, 10, 34))

        files = []
        for file in os.listdir(
                "C:\\Users\\localadmin\\ownCloud\\SoftwareDev\\Python\\pyIMD\\pyIMD\\scratch_space"):
            if file.endswith(".tif"):
                files.append(os.path.join(
                    "C:\\Users\\localadmin\\ownCloud\\SoftwareDev\\Python\\pyIMD\\pyIMD\\scratch_space",
                    file))
        self.image_file_names = files
        image = ndimage.rotate(imread(files[0]), -90)

        arrays = [np.random.normal(size=(417, 417)) for i in range(5)]
        image_stack = np.stack(arrays, axis=0)
        image_stack = image_stack + image
        self.start_time_spin_box.setValue(1)
        self.start_time_spin_box.setRange(1, len(image_stack))
        self.end_time_spin_box.setValue(len(image_stack))
        self.end_time_spin_box.setRange(1, len(image_stack))
        self.measurements_spin_box.setRange(1, 100000000)
        self.initialize_item_lists(len(arrays))
        self.initialize_offset_dataframe(len(arrays))
        # Set image stack
        self.graphicsView.setImage(image_stack, xvals=np.linspace(1., image_stack.shape[0], image_stack.shape[0]),
                                   autoRange=False)
        self.graphicsView.view.setLimits(xMin=0, xMax=image_stack.shape[1], yMin=0, yMax=image_stack.shape[2])
        self.mainToolBar.addAction(self.draw_reference_line_action)
        self.mainToolBar.addAction(self.draw_cell_outline_action)

        self.imageDirEdit.setReadOnly(True)

        self.loadImagesBtn.clicked.connect(self.on_open_image_dir)
        self.loadOffsetsBtn.clicked.connect(self.on_open_position_correction_file)
        self.calcOffsetBtn.clicked.connect(self.calculate_tip_offset)
        self.draw_reference_line_action.triggered.connect(self.on_new_reference_line)
        self.draw_cell_outline_action.triggered.connect(self.on_new_cell_shape)
        self.export_results_btn.pressed.connect(self.on_export_results)
        self.save_btn.pressed.connect(self.on_save)

        self.filter_box = FilterBox()
        self.tabWidget.setTabText(1, '2. Apply image filter')
        self.tabWidget.setTabText(3, '4. Save results')
        self.verticalLayout.addWidget(self.filter_box)
        add_filter_btn = self.filter_box.findChild(QPushButton)
        add_filter_btn.clicked.connect(self.on_add_filter)

        self.statusBar.showMessage('Ready')
        self.progressBar = QProgressBar()

        self.statusBar.addPermanentWidget(self.progressBar)

        self.infoTextEdit.setStyleSheet("background-color: rgb(230, 230, 230); border-radius: 5px;")
        self.infoTextEdit.setReadOnly(True)
        tick_icon = QTextDocumentFragment.fromHtml(r"<img src='../scratch_space/Icons-02.png'>")

        self.infoTextEdit.insertPlainText("Welcome to the position correction editor:\n\n")
        self.infoTextEdit.insertPlainText("1. Load a series of images depicting a cell attached to a cantilever.\n")
        self.infoTextEdit.insertPlainText("2. Filter the image stack to increase the contrast for identification of the"
                                          "cellular shape.\n")
        self.infoTextEdit.insertPlainText("3. To compute the position correction (offset from the tip of the cantilever"
                                          ", draw a reference line on the tip of the cantilever first. Press the line "
                                          " button in the toolbar or hit the key R. Then click into the image. Drag the"
                                          " dots such that the line aligns well with the cantilever tip. Then hit the "
                                          " polygon tool or key C and click around the cell until the polygon "
                                          " surrounds the cell well. Hit key ESC to leave the editing mode. Now you can"
                                          " fine tune the shape. Repeat this procedure on several images in the stack."
                                          " The images you leave out will be interpolated.\n"
                                          " interpolated.\n 4. Indicate the measured data index which corresponds to "
                                          "the first image frame (0 if data recording and imaging were startet "
                                          "simultaneously. Set the last image frame until which the correction should "
                                          "be computed (Note: can not be higher than the last image frame but lower. "
                                          "Indicated the number of measurement points per image interval. Compute the "
                                          "offsets (offset can be loaded from a csv file if determined otherwise). \n"
                                          "5. Export the result to a csv file or save and close the dialog. Note: if "
                                          "the pyIMD project is saved all the work done in the position correction "
                                          "editor is saved in the xml file and can be reloaded.")
        self.infoTextEdit.textCursor().insertFragment(tick_icon)
        self.tabWidget.setCurrentIndex(0)
        self.export_results_btn.setEnabled(False)
        self.save_btn.setEnabled(False)

        self.graphicsView.scene.sigMouseMoved.connect(self.onMouseMoved)
        self.last_position = []

    def on_add_filter(self):
        if self.filter_box.isApplyFilter:
            self.load_image_files()

    def onMouseMoved(self, point):
        p = self.graphicsView.view.mapSceneToView(point)
        self.last_position = p
        # print(point)
        # print("{}-{}".format(p.x(), p.y()))

    def initialize_item_lists(self, length):
        self.reference_line_list = [None] * length
        self.cells_list = [None] * length
        self.tip_offset_list = [None] * length

    def initialize_offset_table(self, table_dataframe):
        tm = TableModel(table_dataframe)
        self.data_results = table_dataframe
        self.tableView.setModel(tm)

    def initialize_offset_dataframe(self, length):
        self.data = []
        for i in range(length):
            self.data.append([i+1] + [np.nan] * 7)

    def on_open_image_dir(self):

        self.image_file_names, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                                "All Files (*);; Image Files (*.tif)")

        if self.image_file_names:
            self.statusBar.showMessage('Start importing the files')
            self.load_image_files()

    def on_export_results(self):

        self.export_name, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                                "Comma separated file (*.csv);;")
        if self.export_name:
            self.statusBar.showMessage('Exported results')
            self.export_results()

    def on_save(self):
        try:
            data_to_send = self.data_results
            data_to_send['Image frames'] = self.image_file_names
            print('VAL', self.start_time_spin_box.value(), type(self.start_time_spin_box.value()))
            self.send_data(data_to_send, self.start_time_spin_box.value(), self.end_time_spin_box.value(),
                           self.measurements_spin_box.value(), self.is_zero_outside_box.isChecked())
            self.close()
        except Exception as e:
            self.statusBar.showMessage("Error: {}".format(e))

    def load_project(self, image_files, data, image_start_index, position_correction_end_frame,
                     number_of_data_per_frame, is_zero_outside_correction_range):
        self.image_file_names = image_files
        self.load_image_files()
        self.initialize_offset_table(data)
        self.export_results_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.start_time_spin_box.setValue(image_start_index)
        self.end_time_spin_box.setValue(position_correction_end_frame)
        self.measurements_spin_box.setValue(number_of_data_per_frame)
        self.is_zero_outside_box.setChecked(is_zero_outside_correction_range)
        self.statusBar.showMessage('Ready!')

    def load_image_files(self):
        image_list = [None] * len(self.image_file_names)
        try:
            for f in range(len(self.image_file_names)):
                # Set progressbar
                if len(self.image_file_names) == 1:
                    self.progressBar.setValue(f / (len(self.image_file_names)) * 100)
                else:
                    self.progressBar.setValue(f / (len(self.image_file_names) - 1) * 100)

                # Load images and apply filter if needed
                if self.filter_box.isApplyFilter:
                    if self.filter_box.filter_widget.filter_name == 'Gamma Correction':
                        self.statusBar.showMessage('Applying {} filter on images'.format(
                            self.filter_box.filter_widget.filter_name))
                        gain = self.filter_box.filter_widget.gain.value()
                        gamma = self.filter_box.filter_widget.gamma.value()
                        image_list[f] = exposure.adjust_gamma(ndimage.rotate(rgb2gray(imread(self.image_file_names[f])),
                                                                             -90), gamma, gain)
                    elif self.filter_box.filter_widget.filter_name == 'Global Histogram Equalization':
                        self.statusBar.showMessage(
                            'Applying {} filter on images'.format(self.filter_box.filter_widget.filter_name))
                        n_bins = self.filter_box.filter_widget.n_bins.value()
                        image_list[f] = exposure.equalize_hist(ndimage.rotate(rgb2gray(imread(
                            self.image_file_names[f])), -90), n_bins)
                    elif self.filter_box.filter_widget.filter_name == 'Local Histogram Equalization':
                        self.statusBar.showMessage(
                            'Applying {} filter on images'.format(self.filter_box.filter_widget.filter_name))
                        disk_val = self.filter_box.filter_widget.disk.value()
                        image_list[f] = rank.equalize(ndimage.rotate(rgb2gray(imread(self.image_file_names[f])), -90),
                                                      selem=disk(disk_val))
                    elif self.filter_box.filter_widget.filter_name == 'Adaptive Histogram Equalization':
                        kernel_size = self.filter_box.filter_widget.kernel_size.value()
                        if kernel_size == 0:
                            kernel_size = None
                        clip_limit = self.filter_box.filter_widget.clip_limit.value()
                        n_bins = self.filter_box.filter_widget.n_bins.value()
                        image_list[f] = exposure.equalize_adapthist(ndimage.rotate(rgb2gray(imread(
                            self.image_file_names[f])), -90), kernel_size=kernel_size, clip_limit=clip_limit,
                            nbins=n_bins)
                    elif self.filter_box.filter_widget.filter_name == 'Logarithmic Correction':
                        inv = self.filter_box.filter_widget.inv.value()
                        if inv == 0:
                            inv = False
                        else:
                            inv = True
                        gain = self.filter_box.filter_widget.gain.value()
                        image_list[f] = exposure.adjust_log(ndimage.rotate(rgb2gray(imread(self.image_file_names[f])),
                                                                           -90), gain=gain, inv=inv)
                    elif self.filter_box.filter_widget.filter_name == 'None':
                        image_list[f] = ndimage.rotate(rgb2gray(imread(self.image_file_names[f])), -90)
                else:
                    image_list[f] = ndimage.rotate(rgb2gray(imread(self.image_file_names[f])), -90)
            # arrays = [rgb2gray(imread(files[f])) for f in range(len(files))]
            image_stack = np.stack(image_list, axis=0)
            self.start_time_spin_box.setValue(1)
            self.start_time_spin_box.setRange(1, len(image_stack))
            self.end_time_spin_box.setValue(len(image_stack))
            self.end_time_spin_box.setRange(1, len(image_stack))
            self.graphicsView.setImage(image_stack, xvals=np.linspace(1., image_stack.shape[0], image_stack.shape[0]),
                                       autoRange=False)
            self.graphicsView.view.setLimits(xMin=0, xMax=image_stack.shape[1], yMin=0, yMax=image_stack.shape[2])

            self.graphicsView.view.setBackgroundColor((100, 10, 34))
            self.imageDirEdit.setText(os.path.dirname(self.image_file_names[0]))
            self.initialize_item_lists(len(image_list))
            self.initialize_offset_dataframe(len(image_list))
            self.statusBar.showMessage('Ready')
        except Exception as e:
            self.statusBar.showMessage("Error: {}".format(e))
        self.initialize_item_lists(len(self.image_file_names))

    def on_open_position_correction_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "",
                                              "All Files (*);; Position correction file (*.csv)")
        df = pd.read_csv(file, delimiter=',', names={'Image frame', 'Tip offset'})
        self.initialize_offset_table(df)

    def on_new_reference_line(self):
        reference_line = ReferenceLine(self.graphicsView.currentIndex)
        self.reference_line_list[self.graphicsView.currentIndex] = reference_line
        self.draw_item = 0

    def on_new_cell_shape(self):
        cell_item = CellShapeOutline(self.graphicsView.currentIndex)
        self.cells_list[self.graphicsView.currentIndex] = cell_item
        self.draw_item = 1

    def on_time_change(self):
        self.display_poly_items()

    def on_view_box_state_change(self):
        self.display_poly_items()

    def display_poly_items(self):
        self.remove_poly_item()
        for item in self.reference_line_list:
            # if item.image_index == self.imv.currentIndex:
            if isinstance(item, ReferenceLine):
                if item.image_index == self.graphicsView.currentIndex:
                    # self.graphicsView.getView().addItem(item)
                    self.graphicsView.scene.addItem(item)
                    if item.vertices_items:
                        for vertex in item.vertices_items:
                            self.graphicsView.scene.addItem(vertex)
                            # self.graphicsView.getView().addItem(vertex)
        for item in self.cells_list:
            if isinstance(item, CellShapeOutline):
                if item.image_index == self.graphicsView.currentIndex:
                    # self.imv.getView().scene().addItem(item)
                    self.graphicsView.scene.addItem(item)

                    item.determine_center_of_mass()
                    # if item.center_of_mass_item:
                    #     print('a', item.center_of_mass_item)
                    #     self.graphicsView.scene.addItem(item.center_of_mass_item)
                    if item.center_of_mass_item:
                        print('start adding')
                        try:
                            self.graphicsView.scene.addItem(item.center_of_mass_item)
                        except Exception as e:
                            print(e)
                    if item.vertices_items:
                        for vertex in item.vertices_items:
                            # self.imv.view.scene().addItem(vertex)
                            self.graphicsView.scene.addItem(vertex)

    def remove_poly_item(self):
        for item in self.graphicsView.scene.items():
            if isinstance(item, CellShapeOutline) or isinstance(item, ReferenceLine):
                # self.imv.getView().scene().removeItem(item)
                self.graphicsView.scene.removeItem(item)
                if hasattr(item, 'center_of_mass_item'):
                    # if item.center_of_mass_item:
                    #     print('del from scene', item.center_of_mass_item)
                    #     self.graphicsView.scene.removeItem(item.center_of_mass_item)
                    if item.center_of_mass_item:
                        self.graphicsView.scene.removeItem(item.center_of_mass_item)
                if item.vertices_items:
                    for vertex in item.vertices_items:
                        # self.imv.view.scene().removeItem(vertex)
                        self.graphicsView.scene.removeItem(vertex)

    def mousePressEvent(self, event):
        # print('Scene Pos', event.type())
        # print(self.graphicsView.getImageItem().mapFromView(event.pos()))
        # print(event.pos())
        # print('pos',  event.pos())
        # print(self.graphicsView.getView())
        # print(self.graphicsView.mapFromParent(event.pos()))
        # print(self.graphicsView.getView().mapViewToScene(event.pos()))
        # print('pos mapped scene to view', self.graphicsView.view.mapSceneToView(event.pos()))
        # print('pos mapped from view', self.graphicsView.view.mapFromView(event.pos()))
        # print('pos mapped to view', self.graphicsView.view.mapToView(event.pos()))
        # print('pos mapped view to scene', self.graphicsView.view.mapViewToScene(event.pos()))
        # print('view', self.graphicsView.view.viewPixelSize())
        # print(self.graphicsView.view.viewRange())
        # print(self.graphicsView.view.viewRect())
        print('last position', self.last_position)
        print('event pos', event.pos())
        print(self.graphicsView.view.mapViewToScene(event.pos()))
        print(self.graphicsView.view.mapSceneToView(event.pos()))
        if self.draw_item == 0:
            self.remove_poly_item()
            if self.reference_line_list[self.graphicsView.currentIndex]:
                # print('pos mapped scene to view', self.graphicsView.view.mapSceneToView(event.pos()))
                # print('pos mapped from view', self.graphicsView.view.mapFromView(event.pos()))
                # print('pos mapped to view', self.graphicsView.view.mapFromView(event.pos()))
                # print('pos mapped view to scene', self.graphicsView.view.mapViewToScene(event.pos()))
                # print('view', self.graphicsView.view.viewPixelSize())
                # First point
                self.reference_line_list[self.graphicsView.currentIndex].add_vertex(self.graphicsView.view.mapViewToScene(self.last_position))
                # Second point
                self.reference_line_list[self.graphicsView.currentIndex].add_vertex(self.graphicsView.view.mapViewToScene(self.last_position))
                self.draw_item = None
        elif self.draw_item == 1:
            if self.cells_list[self.graphicsView.currentIndex]:
                item_to_delete = self.cells_list[self.graphicsView.currentIndex].delete_last_vertex()
                self.graphicsView.view.scene().removeItem(item_to_delete)
                self.cells_list[self.graphicsView.currentIndex].add_vertex(self.graphicsView.view.mapViewToScene(self.last_position))
                # Second point
                self.cells_list[self.graphicsView.currentIndex].add_vertex(self.graphicsView.view.mapViewToScene(self.last_position))
        self.display_poly_items()

    def keyPressEvent(self, event):
        self.remove_poly_item()
        if event.key() == Qt.Key_Escape:
            self.draw_item = None
        elif event.key() == Qt.Key_R:
            self.on_new_reference_line()
        elif event.key() == Qt.Key_C:
            self.on_new_cell_shape()
        elif event.key() == Qt.Key_O:
            self.on_open_image_dir()
        self.display_poly_items()

    def setCurrentIndex(self, ind):
        """ Override of pg.ImageView.setCurrentIndex to emit the signal sigTimeChanged for proper refreshing of
        GraphicsItems.

        Set the currently displayed frame index.
        """
        self.graphicsView.currentIndex = np.clip(ind, 0, self.graphicsView.getProcessedImage().shape[
            self.graphicsView.axes['t']] - 1)
        self.graphicsView.updateImage()
        self.graphicsView.ignoreTimeLine = True
        self.graphicsView.timeLine.setValue(self.graphicsView.tVals[self.graphicsView.currentIndex])
        self.graphicsView.ignoreTimeLine = False
        self.graphicsView.sigTimeChanged.emit(self.graphicsView.currentIndex, self.graphicsView.currentIndex)

    @staticmethod
    def calculate_norm_cell_to_reference(p1, p2, centroid):
        try:
            print(p1, p2, centroid)
            denominator = abs((p2.y() - p1.y()) * centroid.x() - (p2.x() - p1.x()) * centroid.y() + p2.x() * p1.y() - p2.y() * p1.x())
            print(denominator)
            numerator = math.sqrt((p2.y() - p1.y()) ** 2 + (p2.x() - p1.x()) ** 2)
            print(numerator)
            distance = denominator/numerator
            print(distance)
            return distance
        except Exception as e:
            print(e)

    def calculate_tip_offset(self):

        try:
            res = self.show_popup()

            if res == 0:
                for i in range(len(self.cells_list)):
                    # If we have a pair of a reference line and a cell outline on a particular image we compute its
                    # offset
                    # @todo: Implement functionality if a pyIMD xml project is loaded such that one can continue
                    # working in the editor.
                    # Idea: load center of mass into center of mass list, load offsets from table or do nothing.
                    # Have priority if a shape is drawn overwrite table!
                    # @todo Implement positioning of cell center and reference line if project is loaded.
                    # Check how line can be drawn programatically.
                    if self.reference_line_list[i] and self.cells_list[i]:
                        vertices = []
                        vertices2 = []
                        for j in range(len(self.cells_list[i].vertices)):
                            vertices.append([self.graphicsView.view.mapSceneToView(self.cells_list[i].vertices[j]).x(),
                                             self.graphicsView.view.mapSceneToView(self.cells_list[i].vertices[j]).y()])
                            vertices2.append([self.graphicsView.view.mapViewToScene(self.cells_list[i].vertices_in_scene[j]).x(),
                                             self.graphicsView.view.mapViewToScene(self.cells_list[i].vertices_in_scene[j]).y()])

                        center_of_mass = calculate_center_of_mass(vertices)
                        center_of_mass2 = calculate_center_of_mass(vertices2)
                        print('CENTER OF MASS', center_of_mass)
                        print('CENTER OF MASS2', center_of_mass2)

                        print(self.cells_list[i].center_of_mass)
                        # print('bb')
                        self.tip_offset_list[i] = self.calculate_norm_cell_to_reference(
                            self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[0]),
                            self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[1]),
                            QPointF(center_of_mass[0], center_of_mass[1]))
                        # print('aa')
                        self.data[i] = [i + 1, self.tip_offset_list[i], center_of_mass[0], center_of_mass[1],
                                        self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[0]).x(),
                                        self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[0]).y(),
                                        self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[1]).x(),
                                        self.graphicsView.view.mapSceneToView(self.reference_line_list[i].vertices[1]).y()]

                # Interpolate missing values for image frames in between if not for all image frame a reference and cell
                # outline was drawn. Note at least on the first and last frame the reference and cell outline has to be
                #  present.
                # print(self.tip_offset_list)
                if self.tip_offset_list:
                    # print('data', self.data)
                    df = pd.DataFrame(self.data, columns=['Image frame', 'Tip offset', 'Centroid x', 'Centroid y',
                                                          'Ref point1 x', 'Ref point1 y', 'Ref point2 x',
                                                          'Ref point2 y'])

                    # print('vaaaaaal', self.start_time_spin_box.value())
                    x_values = np.linspace(self.start_time_spin_box.value(), self.end_time_spin_box.value(), (
                            self.end_time_spin_box.value()-self.start_time_spin_box.value())+1)
                    # print('len data', len(self.data))
                    # print('xvalues', x_values)
                    ddf = df.dropna()
                    # print(len(ddf))
                    if len(ddf) >= 1:
                        interp = np.interp(x_values, ddf.iloc[:, 0], ddf.iloc[:, 1])
                        # print(interp)
                        # print(len(df))
                        # print((self.start_time_spin_box.value()), self.end_time_spin_box.value())
                        indicies = [int(x_values[i]-1) for i in range(len(x_values))]
                        # print(indicies)
                        # print(indicies[0], indicies[-1])
                        # print(indicies)
                        df.iloc[indicies, 1] = interp  # Note be very careful where to insert as depending on the interp range we do not
                        #  evaluate the whole data.
                        self.initialize_offset_table(df)
                        # Do interpolation of the values.
                        # The interpolated values have then to be matched and re interpolated to the length of the measurement data.
                        # Image frequency has to be know or at least how many measurements one had between the first image and next
                        # one.
                        self.export_results_btn.setEnabled(True)
                        self.save_btn.setEnabled(True)
                        self.statusBar.showMessage('Done!')
                    else:
                        self.statusBar.showMessage('Error: Check if all items are drawn correctly.')
                        # print('Interpolating')

        except Exception as e:
            print('Exception:', e)
            self.statusBar.showMessage('Error:', e)

    def export_results(self):
        try:
            model = self.tableView.model()
            if model:
                data = model.get_data()
                if self.export_name.endswith('.csv'):
                    data.to_csv(self.export_name, sep=',', index=False, header=True)
                else:
                    data.to_csv(self.export_name + '.csv', sep=',', index=False, header=True)
                self.statusBar.showMessage('Done exporting')
        except Exception as e:
            self.statusBar.showMessage('Error:', e)

    def send_data(self, data, start_idx, end_idx, interval, condition):

        """
        Sends the data to the main window

        Args:
            data (`PandasDataframe`):                   Data to be sent to the console.
            start_idx (`int`):                          Measured data index which corresponds to first image frame.
            end_idx (`int`):                            Image frame until which the position should be computed.
            interval (`int`):                           Number of measurement points between two image frames.
            condition (`bool`):                         Bool determining if data will be set to zero outside of position
                                                        corrected range

        Returns:
            data (`PandasDataframe`):                   Data to be sent to the console
            start_idx (`int`):                          Measured data index which corresponds to first image frame.
            end_idx (`int`):                            Image frame until which the position should be computed.
            interval (`int`):                           Number of measurement points between two image frames.
            condition (`bool`):                         Bool determining if data will be set to zero outside of position
                                                        corrected range
        """
        self.save_to_main_signal.emit(data, start_idx, end_idx, interval, condition)

    def show_popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("pyIMD :: Position Correction :: Message")
        msgBox.setStandardButtons(QMessageBox.Cancel)

        # Set text depending on ui state:
        empty_cells_idx = [i for i in range(len(self.cells_list)) if self.cells_list[i] == None]
        filled_cells_idx = [i for i in range(len(self.cells_list)) if self.cells_list[i] != None]
        empty_reference_line_idx = [i for i in range(len(self.reference_line_list)) if self.reference_line_list[i] == None]
        filled_reference_line_idx = [i for i in range(len(self.reference_line_list)) if self.reference_line_list[i] != None]
        # @todo compare lengths of empty indices. The shorter one neets to be corrected i.e add new item. if equal check
        # if first elemnt is filled out if not ask user to do so. if last is not len(list) notify if he wants to
        # interpolate only until there. note that rest data will be set to zero. if accept we calc otherwise we let correct before interpolating
        # @todo if results are loaded display center of mass with point and draw lines programmatically. find out how.
        # (check if image stack equals length of list, then draw, otherwise just display table)
        # @todo implement save button.
        # @todo implement use offset in main pyimd
        # @ todo dowload first from git and do merge before commiting anything
        # print('filled cell idx', filled_cells_idx)
        # print('filled ref idx', filled_reference_line_idx)
        # print('length cells', len(filled_cells_idx), 'length ref', len(filled_reference_line_idx))
        print('___________________________')
        print('Empty Cells', empty_cells_idx)
        print('Empty ref', empty_reference_line_idx)
        print('filled Cells', filled_cells_idx)
        print('filled ref', filled_reference_line_idx)
        print(len(self.cells_list) )
        if not filled_cells_idx and not filled_reference_line_idx:
            msgBox.setText("Please draw at least a cell outline and reference line.")
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msgBox.exec()
        elif 0 in empty_cells_idx:
            msgBox.setText("Cell outline on the first frame is missing. Please add it to continue.")
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msgBox.exec()
        elif 0 in empty_reference_line_idx:
            msgBox.setText("Reference line on the first frame is missing. Please add it to continue.")
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msgBox.exec()
        elif set(filled_cells_idx) != set(filled_reference_line_idx):
            not_in_reference = set(filled_cells_idx) - set(filled_reference_line_idx)
            not_in_cells = set(filled_reference_line_idx) - set(filled_cells_idx)
            msgBox.setText("Some items are missing. Please correct before you continue:\n Reference item(s) "
                           "missing on frame(s) {}.\n Cell item(s) missing on frame(s) {}.".format(
                            [i + 1 for i in list(not_in_reference)], [i + 1 for i in list(not_in_cells)]))
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
            return_value = msgBox.exec()
        elif len(self.cells_list) - 1 in empty_cells_idx:
            msgBox.setText("Cell outline on the last frame is missing. If this is intentional note that the data will "
                           "only be corrected until your last marked frame ({}) and the rest will be set to zero. "
                           "Otherwise please add a cell outline on the last image frame as well.".format(
                max(filled_cells_idx) + 1))
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok | QMessageBox.Cancel)
            return_value = msgBox.exec()
        elif len(self.reference_line_list) - 1 in empty_reference_line_idx:
            msgBox.setText("Reference line on the last frame is missing. If this is intentional note that the data will"
                           "only be corrected until your last marked frame ({}) and the rest will be set to zero. "
                           "Otherwise please add a reference line on the last image frame as well.".format(
                max(filled_reference_line_idx) + 1))
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok | QMessageBox.Cancel)
            return_value = msgBox.exec()
        else:
            msgBox.setText("All good.")
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok | QMessageBox.Cancel)
            return_value = QMessageBox.Ok
            msgBox.done(0)

        if return_value == QMessageBox.Ok:
            return 0
        elif return_value == QMessageBox.Retry:
            return 2
        elif return_value == QMessageBox.Cancel:
            return 1
        else:
            return 1


class TableModel(QAbstractTableModel):

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.index)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def get_data(self):
        return self._data

    def headerData(self, rowcol, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[rowcol]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[rowcol]
        return None

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        flags |= Qt.ItemIsDragEnabled
        flags |= Qt.ItemIsDropEnabled
        return flags

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)


class FilterBox(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        self.filter_widget = []
        self.isApplyFilter = False
        self.grid = QGridLayout(self)

        self.filter_select_box = QComboBox()
        self.filter_select_box.addItem('None')
        self.filter_select_box.addItem('Gamma Correction')
        self.filter_select_box.addItem('Logarithmic Correction')
        self.filter_select_box.addItem('Global Histogram Equalization')
        self.filter_select_box.addItem('Local Histogram Equalization')
        self.filter_select_box.addItem('Adaptive Histogram Equalization')

        self.apply_filter_btn = QPushButton("Apply filter", self)
        self.apply_filter_btn.clicked.connect(self.on_apply_filter)

        self.setLayout(self.grid)
        self.grid.addWidget(self.filter_select_box, 0, 0)
        self.grid.addWidget(self.apply_filter_btn, 4, 0)
        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(self.vertical_spacer)

        self.filter_select_box.currentIndexChanged.connect(self.add_filter_options)

    def on_apply_filter(self):

        if self.filter_widget:
            self.isApplyFilter = True
        else:
            self.isApplyFilter = False

    def add_filter_options(self):
        filter_name = self.filter_select_box.currentText()
        if self.filter_widget:
            for i in reversed(range(self.grid.count())):
                try:
                    self.grid.itemAt(i).widget().setParent(None)
                except Exception as e:
                    print(e)
            self.grid.addWidget(self.filter_select_box, 0, 0)
            self.grid.addWidget(self.apply_filter_btn, 4, 0)
        self.filter_widget = ImageFilterParameterFields(filter_name)
        self.grid.addWidget(self.filter_widget, 1, 0)
        self.grid.addItem(self.vertical_spacer)


class ImageFilterParameterFields(QWidget):
    def __init__( self, filter_name, parent=None):
        super(ImageFilterParameterFields, self).__init__(parent)
        self.gird_layout = QVBoxLayout()
        self.filter_name = filter_name
        self.initialize_widgets(filter_name)

    def initialize_widgets(self, filter_name):

        if filter_name == 'None':
            self.none = QLabel('')

        elif filter_name == 'Gamma Correction':
            self.gamma_label = QLabel('Gamma')
            self.gamma = QDoubleSpinBox()
            self.gamma.setToolTip('Non negative real number. Default value is 1.')
            self.gamma.setValue(1)
            self.gain_label = QLabel('Gain')
            self.gain = QDoubleSpinBox()
            self.gain.setToolTip('The constant multiplier. Default value is 1.')
            self.gain.setValue(1)
            self.gird_layout.addWidget(self.gamma_label)
            self.gird_layout.addWidget(self.gamma)
            self.gird_layout.addWidget(self.gain_label)
            self.gird_layout.addWidget(self.gain)

        elif filter_name == 'Global Histogram Equalization':
            self.n_bins_label = QLabel('Number of bins')
            self.n_bins = QSpinBox()
            self.n_bins.setRange(1, 1000000)
            self.n_bins.setValue(256)
            self.n_bins.setToolTip('Number of bins for image histogram. Note: this argument is ignored for integer '
                                   'images, for which each integer is its own bin.')
            self.gird_layout.addWidget(self.n_bins_label)
            self.gird_layout.addWidget(self.n_bins)

        elif filter_name == 'Local Histogram Equalization':
            self.disk_label = QLabel('Disk radius')
            self.disk = QSpinBox()
            self.disk.setRange(1, 1000000)
            self.disk.setValue(30)
            self.disk.setToolTip('The neighborhood expressed as a 2-D array of 1’s and 0’s.')
            self.gird_layout.addWidget(self.disk_label)
            self.gird_layout.addWidget(self.disk)
        elif filter_name == 'Adaptive Histogram Equalization':
            self.kernel_size_label = QLabel('Kernel size')
            self.kernel_size = QSpinBox()
            self.kernel_size.setValue(0)
            self.kernel_size.setToolTip('Defines the shape of contextual regions used in the algorithm. \n If iterable '
                                        ' is passed, it must have the same number of elements as image.ndim (without '
                                        ' color channel). \n If integer, it is broadcasted to each image dimension. \n '
                                        ' By default, kernel_size is 1/8 of image height by 1/8 of its width.')
            self.clip_limit_label = QLabel('Clipping limit')
            self.clip_limit = QDoubleSpinBox()
            self.clip_limit.setValue(0.01)
            self.clip_limit.setToolTip('Clipping limit, normalized between 0 and 1 (higher values give more contrast)')
            self.n_bins_label = QLabel('Number of bins')
            self.n_bins = QSpinBox()
            self.n_bins.setRange(1, 1000000)
            self.n_bins.setValue(256)
            self.n_bins.setToolTip('Number of gray bins for histogram (“data range”).')
            self.gird_layout.addWidget(self.kernel_size_label)
            self.gird_layout.addWidget(self.kernel_size)
            self.gird_layout.addWidget(self.clip_limit_label)
            self.gird_layout.addWidget(self.clip_limit)
            self.gird_layout.addWidget(self.n_bins_label)
            self.gird_layout.addWidget(self.n_bins)

        elif filter_name == 'Logarithmic Correction':
            self.gain_label = QLabel('Gain')
            self.gain = QDoubleSpinBox()
            self.gain.setValue(1)
            self.gain.setToolTip('The constant multiplier. Default value is 1.')
            self.inv_label = QLabel('Inv')
            self.inv = QSpinBox()
            self.inv.setRange(0, 1)
            self.inv.setValue(0)
            self.inv.setToolTip('If True, it performs inverse logarithmic correction, else correction will be '
                                'logarithmic. Defaults to False.')
            self.gird_layout.addWidget(self.gain_label)
            self.gird_layout.addWidget(self.gain)
            self.gird_layout.addWidget(self.inv_label)
            self.gird_layout.addWidget(self.inv)

        self.setLayout(self.gird_layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = PositionCorrectionUI()
    main.show()
    sys.exit(app.exec_())