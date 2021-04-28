# /********************************************************************************
# * Copyright © 2018-2020, ETH Zurich, D-BSSE, Andreas P. Cuny & Gotthold Fläschner
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
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QAbstractTableModel, pyqtSlot
from PyQt5.Qt import QMainWindow, QApplication,  QPushButton, QSizePolicy, QTextDocumentFragment, QPointF
from PyQt5.QtWidgets import QAction, QFileDialog, QProgressBar, QMessageBox, QSlider
from pyIMD.configuration.defaults import *
from pathlib import Path
from pyIMD.ui.resource_path import resource_path
from pyIMD.ui.poscorrection.bookkeeper import BookKeeper
from pyIMD.ui.poscorrection.scene import Scene
from pyIMD.ui.poscorrection.view import View
from pyIMD.ui.poscorrection.image_filter import FilterBox, get_image_filter
import numpy as np
import pyqtgraph as pg
from pgcolorbar.colorlegend import ColorLegendItem
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
from pyIMD.ui.poscorrection.compositeLine import CompositeLine
from pyIMD.ui.poscorrection.compositePolygon import CompositePolygon

__author__ = 'Andreas P. Cuny'


class PositionCorrectionUI(QMainWindow):
    """
    Position Correction user interface implementation.

    """

    save_to_main_signal = pyqtSignal(object, list, int, int, int, bool, name='save_to_main_signal')
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

        uic.loadUi(resource_path(str(Path('ui', 'positioncorrectionui.ui'))), self)
        self.setWindowTitle('pyIMD :: Position Correction')
        self.draw_reference_line_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-02.png')))),
                                                  'Draw new cantilever tip reference line', self)
        self.delete_reference_line_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-06.png')))),
                                                  'Delete current cantilever tip reference line', self)
        self.draw_cell_outline_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-01.png')))),
                                                'Draw new cell outline', self)
        self.copy_previous_cell_outline_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-03.png')))),
                                                'Copy cell outline and reference line from previous timepoint', self)
        self.copy_all_cell_outline_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-04.png')))),
                                                'Copy current cell outline  and reference line to all timepoints', self)
        self.delete_cell_outline_action = QAction(QIcon(resource_path(str(Path('ui', 'icons', 'Icons-05.png')))),
                                                'Delete current cell outline', self)
        self.draw_reference_line_action.triggered.connect(self.on_new_reference_line)
        self.delete_reference_line_action.triggered.connect(self.on_delete_reference_line)
        self.draw_cell_outline_action.triggered.connect(self.on_new_cell_shape)
        self.copy_previous_cell_outline_action.triggered.connect(self.on_copy_cell_shape)
        self.copy_all_cell_outline_action.triggered.connect(self.on_copy_all_cell_shapes)
        self.delete_cell_outline_action.triggered.connect(self.on_delete_cell_shape)

        self.draw_item = None
        self.image_file_names = []
        self.reference_line_list = []
        self.cells_list = []
        self.center_of_mass_list = []
        self.tip_offset_list = []
        self.data = []
        self.data_results = []
        self.correction_objects = []
        self.image = None
        self.image_filter_data = None

        # Instantiate a BookKeeper
        self.bookKeeper = BookKeeper()
        self.image_file_names = self.bookKeeper.image_paths
        self.scene = Scene(self.image, 0.0, 0.0, 500.0, 500.0)
        self.scene.signal_add_object_at_position.connect(
            self.handle_add_object_at_position)

        # Load and display the image
        self.scene.display_image(self.bookKeeper.getCurrentImagePath(), image_filter=self.image_filter_data)
        c_map_gray = pg.ColorMap(*zip(*Gradients["grey"]["ticks"]))
        lut = c_map_gray.getLookupTable()
        self.lut = lut.astype(np.uint8)
        self.scene.image.setLookupTable(self.lut)
        self.colorLegendItem = ColorLegendItem(
            imageItem=self.scene.image, showHistogram=True, label=False, histHeightPercentile=99.9)
        self.colorLegendItem.sigLevelsChanged.connect(self.on_histogram_changed)
        self.colorLegendItem.setLabel(None)
        self.graphicsLayoutWidget = pg.GraphicsLayoutWidget()
        self.graphicsLayoutWidget.addItem(self.colorLegendItem)
        self.graphicsLayoutWidget.setBackground((240, 240, 240))
        self.graphicsLayoutWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Ignored)
        self.graphicsLayoutWidget.setMinimumWidth(130)
        self.graphicsLayoutWidget.setMaximumWidth(130)

        # Attach a customized QGraphicsView to the QGraphicsScene
        self.view = View(self.scene)

        # Create an horizontal slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.bookKeeper.num_timepoints - 1)
        self.slider.valueChanged.connect(self.on_time_value_changed)

        self.gridLayout.addWidget(self.view, 0, 1)
        self.gridLayout.addWidget(self.slider, 1, 1)
        self.gridLayout.addWidget(self.graphicsLayoutWidget, 0, 2)

        self.start_time_spin_box.setValue(0)
        self.start_time_spin_box.setRange(0, 2147483647)
        self.end_time_spin_box.setValue(self.bookKeeper.num_timepoints)
        self.end_time_spin_box.setRange(1, self.bookKeeper.num_timepoints)
        self.measurements_spin_box.setRange(1, 2147483647)
        self.initialize_item_lists(self.bookKeeper.num_timepoints)
        self.initialize_offset_dataframe(self.bookKeeper.num_timepoints)
        self.graphicsView = self.view
        self.mainToolBar.addAction(self.draw_reference_line_action)
        self.mainToolBar.addAction(self.delete_reference_line_action)
        self.mainToolBar.addAction(self.draw_cell_outline_action)
        self.mainToolBar.addAction(self.copy_previous_cell_outline_action)
        self.mainToolBar.addAction(self.copy_all_cell_outline_action)
        self.mainToolBar.addAction(self.delete_cell_outline_action)

        self.imageDirEdit.setReadOnly(True)

        self.loadImagesBtn.clicked.connect(self.on_open_image_dir)
        self.loadOffsetsBtn.clicked.connect(self.on_open_position_correction_file)
        self.calcOffsetBtn.clicked.connect(self.calculate_tip_offset)
        self.export_results_btn.pressed.connect(self.on_export_results)
        self.save_btn.pressed.connect(self.on_save)

        self.filter_box = FilterBox()
        self.tabWidget.setTabText(1, '2. Apply image filter')
        self.tabWidget.setTabText(3, '4. Save results')
        self.verticalLayout.addWidget(self.filter_box)
        add_filter_btn = self.filter_box.findChild(QPushButton)
        add_filter_btn.clicked.connect(self.on_add_filter)
        self.tabWidget.setCurrentIndex(0)

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
        self.export_results_btn.setEnabled(False)
        self.save_btn.setEnabled(False)

        # self.graphicsView.scene.sigMouseMoved.connect(self.onMouseMoved)
        self.last_position = []

        # Show image
        self.redraw_scene()
        # self.scene.display_image()
        # self.colorLegendItem.resetColorLevels()
        # Set view size to image size
        # print(self.scene.pixMap.size())
        # width = self.scene.pixMap.size().width()
        # height = self.scene.pixMap.size().height()
        # self.graphicsView.setFixedSize(width, height)
        # self.graphicsView.setSceneRect(0, 0, width, height)
        # self.graphicsView.fitInView(0, 0, width, height, Qt.KeepAspectRatio)

    def redraw_scene(self):
        self.scene.display_image(self.bookKeeper.getCurrentImagePath(), image_filter=self.image_filter_data)
        self.colorLegendItem.setImageItem(self.scene.image)
        self.scene.image.setLookupTable(self.lut)
        self.colorLegendItem.autoScaleFromImage()  # note in version 1.0.0 its called resetColorLevels()
        self.refresh_items_on_scene()

    def on_histogram_changed(self):
        self.scene.display_image()
        self.refresh_items_on_scene()

    def on_time_value_changed(self, value):
        self.bookKeeper.timepoint = value
        self.redraw_scene()

    def refresh_items_on_scene(self):
        self.scene.removeCompositeLine()
        currentCompositeLine = self.bookKeeper.getCurrentCompositeLine()
        if currentCompositeLine is not None:
            currentCompositeLine.addToScene(self.scene)

        self.scene.removeCompositePolygon()
        currentCompositePolygon = self.bookKeeper.getCurrentCompositePolygon()
        if currentCompositePolygon is not None:
            currentCompositePolygon.addToScene(self.scene)

    def refresh_images(self):
        self.bookKeeper.addImagePath(self.image_file_names)
        self.slider.setMaximum(self.bookKeeper.num_timepoints - 1)
        self.redraw_scene()

    def on_add_filter(self):
        if self.filter_box.isApplyFilter:
            self.image_filter_data = get_image_filter(self.filter_box)
            self.statusBar.showMessage('Applying {} filter on images'.format(self.image_filter_data['filter_name']))
            self.redraw_scene()

    def onMouseMoved(self, point):
        p = self.graphicsView.view.mapSceneToView(point)
        self.last_position = p

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
            self.send_data(data_to_send, self.correction_objects, self.start_time_spin_box.value(),
                           self.end_time_spin_box.value(), self.measurements_spin_box.value(),
                           self.is_zero_outside_box.isChecked())
            self.close()
        except Exception as e:
            self.statusBar.showMessage("Error: {}".format(e))

    def load_project(self, image_files, data, correction_objects, image_start_index, position_correction_end_frame,
                     number_of_data_per_frame, is_zero_outside_correction_range):
        self.image_file_names = image_files
        self.load_image_files()
        self.load_objects(correction_objects)
        self.initialize_offset_table(data)
        self.export_results_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.start_time_spin_box.setValue(image_start_index)
        self.end_time_spin_box.setValue(position_correction_end_frame)
        self.measurements_spin_box.setValue(number_of_data_per_frame)
        self.is_zero_outside_box.setChecked(is_zero_outside_correction_range)
        self.statusBar.showMessage('Ready!')

    def load_image_files(self):

        try:
            image_list = [None] * len(self.image_file_names)
            self.refresh_images()

            self.start_time_spin_box.setValue(0)
            # self.start_time_spin_box.setRange(1, len(image_list))
            self.end_time_spin_box.setValue(len(image_list))
            self.end_time_spin_box.setRange(1, len(image_list))
            self.imageDirEdit.setText(os.path.dirname(self.image_file_names[0]))
            self.initialize_item_lists(len(image_list))
            self.initialize_offset_dataframe(len(image_list))
            self.statusBar.showMessage('Ready')
        except Exception as e:
            self.statusBar.showMessage("Error: {}".format(e))
        self.initialize_item_lists(len(self.image_file_names))

    def load_objects(self, correction_objects):

        self.correction_objects = correction_objects
        for el in self.correction_objects:
            self.bookKeeper.timepoint = el["image_frame"] - 1

            # Remove an already existing CompositeLine and Polygon object
            self.scene.removeCompositeLine()
            self.scene.removeCompositePolygon()

            # Create a CompositeLine (it manages three interdependent QGraphicsWidgets)
            compositeLine = CompositeLine(QPointF(32, 7))
            # Add the CompositeLine to the Scene. Note that the CompositeLine is
            # not a QGraphicsItem itself and cannot be added to the Scene directly.
            compositeLine.addToScene(self.scene)

            # Add the Line
            compositeLine._line.setLine(el["tip_reference_line"]['x'][0], el["tip_reference_line"]['y'][0],
                                        el["tip_reference_line"]['x'][1], el["tip_reference_line"]['y'][1])
            compositeLine._vertexA.setPos(el["tip_reference_line"]['x'][0], el["tip_reference_line"]['y'][0])
            compositeLine._vertexB.setPos(el["tip_reference_line"]['x'][1], el["tip_reference_line"]['y'][1])

            # Create a CompositePolygon
            currentCompositePolygon = CompositePolygon()
            # Add the CompositeLine to the Scene. Note that the CompositeLine is
            # not a QGraphicsItem itself and cannot be added to the Scene directly.
            currentCompositePolygon.addToScene(self.scene)
            # Add the vertices
            for v in range(0, len(el["object"]['x'])):
                currentCompositePolygon._polygon_item.add_vertex(QPointF(el["object"]['x'][v], el["object"]['y'][v]))

            # Store the objects
            self.bookKeeper.addCompositeLine(compositeLine)
            self.bookKeeper.addCompositePolygon(currentCompositePolygon)

    def on_open_position_correction_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "",
                                              "All Files (*);; Position correction file (*.csv)")
        df = pd.read_csv(file, delimiter=',', names={'Image frame', 'Tip offset'})
        self.initialize_offset_table(df)

    def on_new_reference_line(self):
        self.draw_item = 1

    def on_delete_reference_line(self):
        self.bookKeeper.removeCompositeLine()
        self.scene.removeCompositeLine()

    def on_new_cell_shape(self):
        self.draw_item = 2

    def on_copy_cell_shape(self):
        self.scene.removeCompositePolygon()
        self.scene.removeCompositeLine()
        self.bookKeeper.copyPreviousCompositePolygon(self.scene)
        self.redraw_scene()

    def on_copy_all_cell_shapes(self):
        self.bookKeeper.addCompositePolygonAllTime(self.scene)
        self.redraw_scene()

    def on_delete_cell_shape(self):
        self.bookKeeper.removeCompositePolygon()
        self.scene.removeCompositePolygon()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.draw_item = 0

    @pyqtSlot(float, float, name="handle_add_object_at_position")
    def handle_add_object_at_position(self, x, y):

        if QApplication.keyboardModifiers() == Qt.Key_Escape or QApplication.mouseButtons() == Qt.RightButton:
            self.draw_item = 0

        if QApplication.keyboardModifiers() == Qt.ControlModifier or self.draw_item == 1:

            # Remove an already existing CompositeLine object
            self.scene.removeCompositeLine()

            # Create a CompositeLine (it manages three interdependent QGraphicsWidgets)
            compositeLine = CompositeLine(QPointF(x, y))

            # Add the CompositeLine to the Scene. Note that the CompositeLine is
            # not a QGraphicsItem itself and cannot be added to the Scene directly.
            compositeLine.addToScene(self.scene)

            # Keep track of the object in the BookKeeper
            self.bookKeeper.addCompositeLine(compositeLine)
            self.draw_item = 0

        elif QApplication.keyboardModifiers() == Qt.ShiftModifier or self.draw_item == 2:

            currentCompositePolygon = self.bookKeeper.getCurrentCompositePolygon()
            if currentCompositePolygon is None:

                # Create a CompositePolygon
                currentCompositePolygon = CompositePolygon()

                # Add the CompositeLine to the Scene. Note that the CompositeLine is
                # not a QGraphicsItem itself and cannot be added to the Scene directly.
                currentCompositePolygon.addToScene(self.scene)

                # Store the polygon
                self.bookKeeper.addCompositePolygon(currentCompositePolygon)

            # Add the first vertex
            currentCompositePolygon._polygon_item.add_vertex(QPointF(x, y))

        elif QApplication.keyboardModifiers() == Qt.AltModifier:
            print("Implement me! i.e delete polygon item")
        else:
            pass

    @staticmethod
    def calculate_norm_cell_to_reference(p1, p2, centroid):
        try:
            denominator = abs((p2.y() - p1.y()) * centroid.x() - (p2.x() - p1.x()) * centroid.y() + p2.x() * p1.y() -
                              p2.y() * p1.x())
            numerator = math.sqrt((p2.y() - p1.y()) ** 2 + (p2.x() - p1.x()) ** 2)
            distance = denominator/numerator
            return distance
        except Exception as e:
            print(e)

    def calculate_tip_offset(self):
        try:
            res = self.show_popup()

            if res == 0:

                line_list = self.bookKeeper.getAllCompositeLine()
                polygon_list = self.bookKeeper.getAllCompositePolygon()
                # Reset list
                self.correction_objects = []

                for i in range(len(line_list)):
                    composite_object = {}

                    # If we have a pair of a reference line and a cell outline on a particular image we compute its
                    # offset
                    if line_list[i] and polygon_list[i]:

                        polygon_list[i].getCenterOfMass()
                        comP = polygon_list[i]._polygon_item._centerOfMass

                        p1 = line_list[i]._vertexA.pos()
                        p2 = line_list[i]._vertexB.pos()

                        polygon_list[i]._polygon_item.updateArea()
                        area = polygon_list[i]._polygon_item._area

                        self.tip_offset_list[i] = self.calculate_norm_cell_to_reference(p2, p1, comP)
                        self.data[i] = [i + 1, self.tip_offset_list[i], comP.x(), comP.y(), p2.x(), p2.y(), p1.x(),
                                        p1.y(), area]
                        # Collect the drawn objects per image frame into a list as dict.
                        composite_object.update({'image_frame': i + 1, 'tip_offset': self.tip_offset_list[i],
                                                 'object_area': area, 'object_center_of_mass': {'x': comP.x(),
                                                                                                'y': comP.y()},
                                                 'tip_reference_line': {'x': [p2.x(), p1.x()], 'y': [p2.y(), p1.y()]},
                                                 'object': polygon_list[i]._polygon_item.vertices_to_dict()})
                        self.correction_objects.append(composite_object)

                # Interpolate missing values for image frames in between if not for all image frame a reference and cell
                # outline was drawn. Note at least on the first and last frame the reference and cell outline has to be
                #  present.
                if self.tip_offset_list:
                    df = pd.DataFrame(self.data, columns=['Image frame', 'Tip offset', 'Centroid x', 'Centroid y',
                                                          'Ref point1 x', 'Ref point1 y', 'Ref point2 x',
                                                          'Ref point2 y', 'Area'])

                    x_values = np.linspace(self.start_time_spin_box.value(), self.end_time_spin_box.value(), (
                            self.end_time_spin_box.value()-self.start_time_spin_box.value())+1)
                    ddf = df.dropna()
                    if len(ddf) >= 1:
                        interp_offsets = np.interp(x_values, ddf.iloc[:, 0], ddf.iloc[:, 1])
                        interp_area = np.interp(x_values, ddf.iloc[:, 0], ddf.iloc[:, 8])
                        indicies = [int(x_values[i]-1) for i in range(len(x_values))]

                        df.iloc[indicies, 1] = interp_offsets  # Note be very careful where to insert as depending on
                        # the interp range we do not evaluate the whole data.
                        df.iloc[indicies, 8] = interp_area  # Note be very careful where to insert as depending on the
                        # interp range we do not evaluate the whole data.
                        self.initialize_offset_table(df)
                        # Do interpolation of the values.
                        # The interpolated values have then to be matched and re interpolated to the length of the
                        # measurement data.
                        # Image frequency has to be know or at least how many measurements one had between the first
                        # image and next
                        # one.
                        self.export_results_btn.setEnabled(True)
                        self.save_btn.setEnabled(True)
                        self.statusBar.showMessage('Done!')
                    else:
                        self.statusBar.showMessage('Error: Check if all items are drawn correctly.')

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

    def send_data(self, data, correction_objects, start_idx, end_idx, interval, condition):

        """
        Sends the data to the main window

        Args:
            data (`PandasDataframe`):                   Data to be sent to the mainwindow.
            correction_objects (`list`):                Position correction data to be sent to the mainwindow.
            start_idx (`int`):                          Measured data index which corresponds to first image frame.
            end_idx (`int`):                            Image frame until which the position should be computed.
            interval (`int`):                           Number of measurement points between two image frames.
            condition (`bool`):                         Bool determining if data will be set to zero outside of position
                                                        corrected range

        Returns:
            data (`PandasDataframe`):                   Data to be sent to the mainwindow
            correction_objects (`list`):                Position correction data to be sent to the mainwindow.
            start_idx (`int`):                          Measured data index which corresponds to first image frame.
            end_idx (`int`):                            Image frame until which the position should be computed.
            interval (`int`):                           Number of measurement points between two image frames.
            condition (`bool`):                         Bool determining if data will be set to zero outside of position
                                                        corrected range
        """
        self.save_to_main_signal.emit(data, correction_objects, start_idx, end_idx, interval, condition)

    def show_popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("pyIMD :: Position Correction :: Message")
        msgBox.setStandardButtons(QMessageBox.Cancel)

        # Set text depending on ui state:
        polygons = self.bookKeeper.getAllCompositePolygon()
        lines = self.bookKeeper.getAllCompositeLine()
        empty_cells_idx = [i for i in range(len(polygons)) if polygons[i] == None]
        filled_cells_idx = [i for i in range(len(polygons)) if polygons[i] != None]
        empty_reference_line_idx = [i for i in range(len(lines)) if lines[i] == None]
        filled_reference_line_idx = [i for i in range(len(lines)) if lines[i] != None]

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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = PositionCorrectionUI()
    main.show()
    sys.exit(app.exec_())