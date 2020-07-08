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

from skimage import exposure
from skimage.morphology import disk
from skimage.filters import rank
from PyQt5.Qt import QSizePolicy, QGroupBox, QLabel, QGridLayout, QSpinBox, QDoubleSpinBox, QComboBox, QVBoxLayout,\
    QWidget, QSpacerItem, QPushButton


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


def get_image_filter(filter_box):

    if filter_box.isApplyFilter:
        if filter_box.filter_widget.filter_name == 'Gamma Correction':

            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': {'gain': filter_box.filter_widget.gain.value(),
                                            'gamma': filter_box.filter_widget.gamma.value()}}
        elif filter_box.filter_widget.filter_name == 'Global Histogram Equalization':

            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': {'n_bins': filter_box.filter_widget.n_bins.value()}}
        elif filter_box.filter_widget.filter_name == 'Local Histogram Equalization':

            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': {'disk_val': filter_box.filter_widget.disk.value()}}
        elif filter_box.filter_widget.filter_name == 'Adaptive Histogram Equalization':

            kernel_size = filter_box.filter_widget.kernel_size.value()
            if kernel_size == 0:
                kernel_size = None
            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': {'kernel_size': kernel_size,
                                            'clip_limit': filter_box.filter_widget.clip_limit.value(),
                                            'n_bins': filter_box.filter_widget.n_bins.value()}}
        elif filter_box.filter_widget.filter_name == 'Logarithmic Correction':
            inv = filter_box.filter_widget.inv.value()
            if inv == 0:
                inv = False
            else:
                inv = True
            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': {'inv': inv,
                                            'gain': filter_box.filter_widget.gain.value()}}
        elif filter_box.filter_widget.filter_name == 'None':
            filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                           'filter_param': None}
    else:
        filter_data = {'filter_name': filter_box.filter_widget.filter_name,
                       'filter_param': None}
    return filter_data


def filter_image(image, filter_data):
    print(image, 'image')
    if filter_data['filter_name'] == 'Gamma Correction':
        filtered_img = exposure.adjust_gamma(image, filter_data['filter_param']['gamma'],
                                             filter_data['filter_param']['gain'])

    elif filter_data['filter_name'] == 'Global Histogram Equalization':
        filtered_img = exposure.equalize_hist(image, filter_data['filter_param']['n_bins'])

    elif filter_data['filter_name'] == 'Local Histogram Equalization':

        filtered_img = rank.equalize(image, selem=disk(filter_data['filter_param']['disk_val']))

    elif filter_data['filter_name'] == 'Adaptive Histogram Equalization':
        filtered_img = exposure.equalize_adapthist(image, kernel_size=filter_data['filter_param']['kernel_size'],
                                                   clip_limit=filter_data['filter_param']['clip_limit'],
                                                   nbins=filter_data['filter_param']['n_bins'])

    elif filter_data['filter_name'] == 'Logarithmic Correction':
        filtered_img = exposure.adjust_log(image, gain=filter_data['filter_param']['gain'],
                                           inv=filter_data['filter_param']['inv'])

    elif filter_data['filter_name'] == 'None':
        filtered_img = image
    else:
        filtered_img = image
    return filtered_img
