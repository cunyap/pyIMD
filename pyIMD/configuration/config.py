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

import ast
import operator
import pathlib
import xmltodict
import json
import yaml
import datetime
import numpy as np
from lxml import etree
from pyIMD.configuration.defaults import *

__author__ = 'Andreas P. Cuny'


class Settings(object):
    """
    Settings initialization with default parameter values stored in pyIMD.configuration.defaults
    """
    def __init__(self):
        # General parameters (initialized with default parameters)
        self.figure_width = FIGURE_WIDTH
        self.figure_height = FIGURE_HEIGHT
        self.figure_units = FIGURE_UNITS
        self.figure_format = FIGURE_FORMAT
        self.figure_resolution_dpi = FIGURE_RESOLUTION_DPI
        self.figure_name_pre_start_no_cell = FIGURE_NAME_PRE_START_NO_CELL
        self.figure_name_pre_start_with_cell = FIGURE_NAME_PRE_START_WITH_CELL
        self.figure_name_measured_data = FIGURE_NAME_MEASURED_DATA
        self.figure_plot_every_nth_point = FIGURE_PLOT_EVERY_NTH_POINT
        self.conversion_factor_hz_to_khz = CONVERSION_FACTOR_HZ_TO_KHZ
        self.conversion_factor_deg_to_rad = CONVERSION_FACTOR_DEG_TO_RAD
        self.conversion_factor_px_to_mum = CONVERSION_FACTOR_PX_TO_MUM
        self.spring_constant = SPRING_CONSTANT
        self.initial_parameter_guess = INITIAL_PARAMETER_GUESS
        self.lower_parameter_bounds = LOWER_PARAMETER_BOUNDS
        self.upper_parameter_bounds = UPPER_PARAMETER_BOUNDS
        self.rolling_window_size = ROLLING_WINDOW_SIZE
        self.correct_for_frequency_offset = CORRECT_FOR_FREQUENCY_OFFSET
        self.frequency_offset_mode = FREQUENCY_OFFSET_MODE
        self.frequency_offset_n_measurements_used = FREQUENCY_OFFSET_N_MEASUREMENTS_USED
        self.frequency_offset = FREQUENCY_OFFSET
        self.read_text_data_from_line = READ_TEXT_DATA_FROM_LINE
        self.cantilever_length = CANTILEVER_LENGTH
        self.cell_position = CELL_POSITION
        self.text_data_delimiter = TEXT_DATA_DELIMITER
        # Project parameters
        self.project_folder_path = ''
        self.calculation_mode = 'PLL'
        self.pre_start_no_cell_path = ''
        self.pre_start_with_cell_path = ''
        self.measurements_path = ''
        self.selected_files = []
        # Position correction parameters
        self.position_correction_data = []
        self.image_files = []
        self.cell_offsets = []
        self.cell_center_of_mass_x = []
        self.cell_center_of_mass_y = []
        self.ref_line_1_x = []
        self.ref_line_1_y = []
        self.ref_line_2_x = []
        self.ref_line_2_y = []
        self.area = []

        self.image_start_index = 0
        self.position_correction_end_frame = 0
        self.number_of_data_per_frame = 0.0
        self.is_zero_outside_correction_range = True

    def __repr__(self):
        """
        Settings representation.

        Returns:
               text (`str`):      Settings representation of pyIMD parameters and project configuration as formatted text.
        """
        return "General settings: \n\tfigure_with: %s (%s) \n\tfigure_height: %s (%s) \n\tfigure_units: %s (%s) " \
               "\n\tfigure_format: %s (%s) \n\tfigure_resolution_dpi: %s (%s) " \
               "\n\tfigure_name_pre_start_no_cell: %s (%s) \n\tfigure_name_pre_start_with_cell: %s (%s)" \
               "\n\tfigure_name_measured_data: %s(%s) \n\tfigure_plot_every_nth_point: % s( % s) " \
               "\n\tconversion_factor_hz_to_khz: %s (%s) " \
               "\n\tconversion_factor_deg_to_rad: %s (%s) \n\tconversion_factor_px_to_mum: %s (%s)" \
               "\n\tspring_constant: %s (%s) " \
               "\n\tinitial_parameter_guess: %s (%s) \n\tlower_parameter_bounds: %s (%s) " \
               "\n\tupper_parameter_bounds: %s (%s) \n\trolling_window_size: % s( % s) " \
               "\n\tcorrect_for_frequency_offset: % s( % s) \n\tfrequency_offset_mode: % s( % s) " \
               "\n\tfrequency_offset_n_measurements_used: % s( % s) \n\tfrequency_offset: % s( % s) " \
               "\n\tread_text_data_from_line: %s (%s) \n\tcantilever_length: %s (%s) \n\tcell_position: %s (%s) " \
               "\n\ttext_data_delimiter: %s (%s) \n" "Project settings: \n\tproject_folder_path: %s (%s) " \
               "\n\tcalculation_mode: %s (%s) \ \n\tpre_start_no_cell_path: %s (%s) " \
               "\n\tpre_start_with_cell_path: %s (%s) \n\tmeasurements_path: %s (%s) \n\tselected_files: %s (%s) " \
               % (
                   self.figure_width, type(self.figure_width), self.figure_height, type(self.figure_height),
                   self.figure_units, type(self.figure_units), self.figure_format, type(self.figure_format),
                   self.figure_resolution_dpi, type(self.figure_resolution_dpi), self.figure_name_pre_start_no_cell,
                   type(self.figure_name_pre_start_no_cell), self.figure_name_pre_start_with_cell,
                   type(self.figure_name_pre_start_with_cell), self.figure_name_measured_data,
                   type(self.figure_name_measured_data), self.figure_plot_every_nth_point,
                   type(self.figure_plot_every_nth_point), self.conversion_factor_hz_to_khz,
                   type(self.conversion_factor_hz_to_khz), self.conversion_factor_deg_to_rad,
                   type(self.conversion_factor_deg_to_rad), self.conversion_factor_px_to_mum,
                   type(self.conversion_factor_px_to_mum), self.spring_constant, type(self.spring_constant),
                   self.initial_parameter_guess, type(self.initial_parameter_guess),
                   self.lower_parameter_bounds, type(self.lower_parameter_bounds), self.upper_parameter_bounds,
                   type(self.upper_parameter_bounds), self.rolling_window_size, type(self.rolling_window_size),
                   self.correct_for_frequency_offset, type(self.correct_for_frequency_offset), self.frequency_offset_mode,
                   type(self.frequency_offset_mode), self.frequency_offset_n_measurements_used,
                   type(self.frequency_offset_n_measurements_used), self.frequency_offset, type(self.frequency_offset),
                   self.read_text_data_from_line, type(self.read_text_data_from_line), self.cantilever_length,
                   type(self.cantilever_length), self.cell_position, type(self.cell_position), self.text_data_delimiter,
                   type(self.text_data_delimiter), self.project_folder_path, type(self.project_folder_path),
                   self.calculation_mode, type(self.calculation_mode), self.pre_start_no_cell_path,
                   type(self.pre_start_no_cell_path), self.pre_start_with_cell_path,
                   type(self.pre_start_with_cell_path), self.measurements_path, type(self.measurements_path),
                   self.selected_files, type(self.selected_files))

    figure_format = property(operator.attrgetter('_figure_format'))
    """
    Parameter defining the result figure(s) format.

    Args:
        unit (`str`):    Pdf and png ar currently supported.
    """
    @figure_format.setter
    def figure_format(self, unit):
        if not (type(unit) == str):
            raise Exception("Figure format should be of type string. 'png' and 'pdf' are valid")
        self._figure_format = unit

    figure_width = property(operator.attrgetter('_figure_width'))
    """
    Parameter defining the result figure(s) width.

    Args:
        width (`float`):    Figure width in the unit specified.
    """
    @figure_width.setter
    def figure_width(self, width):
        if not (type(width) == float or type(width) == int):
            raise Exception("Figure width should be float or int")
        self._figure_width = width

    figure_height = property(operator.attrgetter('_figure_height'))
    """
    Parameter defining the result figure(s) height.

    Args:
        height (`float`):    Figure height in the unit specified.
    """
    @figure_height.setter
    def figure_height(self, height):
        if not (type(height) == float or type(height) == int):
            raise Exception("Figure height should be of type float or int")
        self._figure_height = height

    figure_units = property(operator.attrgetter('_figure_units'))
    """
    Parameter defining the result figure(s) unit.

    Args:
        unit (`str`):    Figure unit. E.g. mm, cm, in.
    """
    @figure_units.setter
    def figure_units(self, unit):
        if not (type(unit) == str):
            raise Exception("Figure unit should be of type string. 'mm', 'cm' and 'in' are valid")
        self._figure_units = unit

    figure_resolution_dpi = property(operator.attrgetter('_figure_resolution_dpi'))
    """
    Parameter defining the result figure(s) resolution in dpi.

    Args:
        resolution (`int`):    Figure resolution. E.g. 72, 150, 300.
    """
    @figure_resolution_dpi.setter
    def figure_resolution_dpi(self, resolution):
        if not (type(resolution) == int):
            raise Exception("Figure resolution should be a of type int.")
        self._figure_resolution_dpi = resolution

    figure_name_pre_start_no_cell = property(operator.attrgetter('_figure_name_pre_start_no_cell'))
    """
    Parameter defining the figure name for the function fit pre start no cell.

    Args:
        name (`str`):    Figure name for the function fit pre start no cell.
    """
    @figure_name_pre_start_no_cell.setter
    def figure_name_pre_start_no_cell(self, name):
        if not (type(name) == str):
            raise Exception("Figure name should be a of type string.")
        self._figure_name_pre_start_no_cell = name

    figure_name_pre_start_with_cell = property(operator.attrgetter('_figure_name_pre_start_with_cell'))
    """
    Parameter defining the figure name for the function fit pre start with cell.

    Args:
        name (`str`):    Figure name for the function fit pre start with cell.
    """
    @figure_name_pre_start_with_cell.setter
    def figure_name_pre_start_with_cell(self, name):
        if not (type(name) == str):
            raise Exception("Figure name should be a of type string.")
        self._figure_name_pre_start_with_cell = name

    figure_name_measured_data = property(operator.attrgetter('_figure_name_measured_data'))
    """
    Parameter defining the figure name for resulting calculated mass of the measured data.

    Args:
        name (`str`):    Figure name for resulting calculated mass of the measured data.
    """
    @figure_name_measured_data.setter
    def figure_name_measured_data(self, name):
        if not (type(name) == str):
            raise Exception("Figure name of measured data should be a of type string.")
        self._figure_name_measured_data = name

    figure_plot_every_nth_point = property(operator.attrgetter('_figure_plot_every_nth_point'))
    """
    Parameter defining how many data points are used for visualization. For very large data sets a number > 1 could 
    increase the readability of the figure and lower the file size.

    Args:
        nth_point (`int`):    Pdf and png ar currently supported.
    """
    @figure_plot_every_nth_point.setter
    def figure_plot_every_nth_point(self, nth_point):
        if not (type(nth_point) == int):
            raise Exception("Plot every nth point with n > 1 < max nr of rows of your data set.")
        self._figure_plot_every_nth_point = nth_point

    conversion_factor_hz_to_khz = property(operator.attrgetter('_conversion_factor_hz_to_khz'))
    """
    Parameter defining the data conversion factor from Hz to kHz.

    Args:
        factor (`float`):    Data conversion factor from hertz to kilo hertz.
    """
    @conversion_factor_hz_to_khz.setter
    def conversion_factor_hz_to_khz(self, factor):
        if not (type(factor) == float or type(factor) == int):
            raise Exception("Conversion factor should be a of type float or int.")
        self._conversion_factor_hz_to_khz = factor

    conversion_factor_deg_to_rad = property(operator.attrgetter('_conversion_factor_deg_to_rad'))
    """
    Parameter defining the data conversion factor from degrees to radians.

    Args:
        factor (`float`):    Data conversion factor from degrees to radians.
    """
    @conversion_factor_deg_to_rad.setter
    def conversion_factor_deg_to_rad(self, factor):
        if not (type(factor) == float or type(factor) == int):
            raise Exception("Conversion factor should be a of type float or int.")
        self._conversion_factor_deg_to_rad = factor

    conversion_factor_px_to_mum = property(operator.attrgetter('_conversion_factor_px_to_mum'))
    """
    Parameter defining the conversion factor from pixel of a microscopy image to microns.

    Args:
        factor (`float`):    Conversion factor from pixel to microns.
    """

    @conversion_factor_px_to_mum.setter
    def conversion_factor_px_to_mum(self, factor):
        if not (type(factor) == float or type(factor) == int):
            raise Exception("Conversion factor should be a of type float or int.")
        self._conversion_factor_px_to_mum = factor

    spring_constant = property(operator.attrgetter('_spring_constant'))
    """
    Parameter defining the spring constant of the cantilever.

    Args:
        spring_constant (`float`):    Spring constant of the cantilever.
    """
    @spring_constant.setter
    def spring_constant(self, spring_constant):
        if not (type(spring_constant) == float or type(spring_constant) == int):
            raise Exception("Spring constant should be a of type float or int.")
        self._spring_constant = spring_constant

    initial_parameter_guess = property(operator.attrgetter('_initial_parameter_guess'))
    """
    Parameter defining the initial parameter guess.

    Args:
        array (`list`):    Initial parameter guess.
    """
    @initial_parameter_guess.setter
    def initial_parameter_guess(self, array):
        if not (array.__len__() == 4 and all(isinstance(n, int) or isinstance(n, float) for n in array)):
            raise Exception("Initial parameter guess list should be a of type list.")
        self._initial_parameter_guess = array

    lower_parameter_bounds = property(operator.attrgetter('_lower_parameter_bounds'))
    """
    Parameter defining the lower parameter bounds.
    
    Args:
        array (`list`):    Lower parameter bounds.
    """
    @lower_parameter_bounds.setter
    def lower_parameter_bounds(self, array):
        if not (array.__len__() == 4 and all(isinstance(n, int) or isinstance(n, float) for n in array)):
            raise Exception("Lower parameter bounds list should be a of type list.")
        self._lower_parameter_bounds = array

    upper_parameter_bounds = property(operator.attrgetter('_upper_parameter_bounds'))
    """
    Parameter defining the upper parameter bounds.

    Args:
        array (`list`):    Upper parameter bounds.
    """
    @upper_parameter_bounds.setter
    def upper_parameter_bounds(self, array):
        if not (array.__len__() == 4 and all(isinstance(n, int) or isinstance(n, float) for n in array)):
            raise Exception("Upper parameter bounds list should be a of type list.")
        self._upper_parameter_bounds = array

    rolling_window_size = property(operator.attrgetter('_rolling_window_size'))
    """
    Parameter defining the window size of the rolling window applied to the data for visualizing the trend. 

    Args:
        window_size (`int`):    Rolling window size.
    """
    @rolling_window_size.setter
    def rolling_window_size(self, window_size):
        if not (type(window_size == int)):
            raise Exception("Window size should be of type int.")
        self._rolling_window_size = window_size

    correct_for_frequency_offset = property(operator.attrgetter('_correct_for_frequency_offset'))
    """
    Parameter defining if PLL measurement data should be corrected for a potential frequency offset between the 
    frequency pre start measured after a cell is attached to the cantilever and the actual measurement.

    Args:
        correction (`boolean`):    Boolean. False by default. True runs in the PLL case a frequency offset correction.
    """

    @correct_for_frequency_offset.setter
    def correct_for_frequency_offset(self, correction):
        if not (type(correction == bool)):
            raise Exception("Correct for frequency offset should be of type bool.")
        self._correct_for_frequency_offset = correction

    frequency_offset_mode = property(operator.attrgetter('_frequency_offset_mode'))
    """
    Parameter defining the mode to be used to calculate the frequency offset. This applies only to in PLL recorded data.

    Args:
        mode (`str`):    Mode for frequency offset calculation. Either Auto or Manual.
    """

    @frequency_offset_mode.setter
    def frequency_offset_mode(self, mode):
        if not (type(mode == str), mode == 'Auto', mode == 'Manual'):
            raise Exception("Frequency offset mode should be of type str. Auto or Manual")
        self._frequency_offset_mode = mode

    frequency_offset_n_measurements_used = property(operator.attrgetter('_frequency_offset_n_measurements_used'))
    """
    Parameter defining how many data points of the measurement should be used to calculate the average frequency offset. 

    Args:
        n_measurements (`int`):    Number of measurement data points to be used to calculate the average freq. offset.
    """

    @frequency_offset_n_measurements_used.setter
    def frequency_offset_n_measurements_used(self, n_measurements):
        if not (type(n_measurements == float), type(n_measurements) == int, n_measurements > 0):
            raise Exception("Frequency offset n measurements used should be of of type int or float.")
        self._frequency_offset_n_measurements_used = n_measurements

    frequency_offset = property(operator.attrgetter('_frequency_offset'))
    """
    Parameter defining the frequency offset. 

    Args:
        freq_offset (`int`):    Frequency offset with which the measurement data will be corrected with.
    """

    @frequency_offset.setter
    def frequency_offset(self, freq_offset):
        if not (type(freq_offset == float), type(freq_offset) == int):
            raise Exception("Frequency offset should be of of type int or float.")
        self._frequency_offset = freq_offset

    read_text_data_from_line = property(operator.attrgetter('_read_text_data_from_line'))
    """
    Parameter defining the length of the header inside the initial sweep files. From this line number the data will be 
    imported.

    Args:
        line_number (`int`):    Line number from where on to read the data from.
    """
    @read_text_data_from_line.setter
    def read_text_data_from_line(self, line_number):
        if not (type(line_number) == float or type(line_number) == int):
            raise Exception("Line number should be a of type float or int.")
        self._read_text_data_from_line = line_number

    cantilever_length = property(operator.attrgetter('_cantilever_length'))
    """
    Parameter defining the cantilever length.

    Args:
        cantilever_length (`float`):    Cantilever length in microns.
    """
    @cantilever_length.setter
    def cantilever_length(self, cantilever_length):
        if not (type(cantilever_length) == float or type(cantilever_length) == int):
            raise Exception("Cantilever length should be a of float or int.")
        self._cantilever_length = cantilever_length

    cell_position = property(operator.attrgetter('_cell_position'))
    """
      Parameter defining the cell position offset.

      Args:
          cell_position (`float`):    Cell position offset in microns from the free end of the cantilever.
    """
    @cell_position.setter
    def cell_position(self, cell_position):
        if not (type(cell_position) == float or type(cell_position) == int):
            raise Exception("Cell position offset should be a of float or int.")
        self._cell_position = cell_position

    text_data_delimiter = property(operator.attrgetter('_text_data_delimiter'))
    """
      Parameter defining the text file data delimiter.

      Args:
          delimiter (`str`):    Text file data delimiter i.e '\t' for tab delimited or ',' for comma separated data.
    """
    @text_data_delimiter.setter
    def text_data_delimiter(self, delimiter):
        if not (type(delimiter) == str):
            raise Exception("Data text delimiter should be a of type string.")
        self._text_data_delimiter = delimiter

    project_folder_path = property(operator.attrgetter('_project_folder_path'))
    """
       Parameter defining the path to the files.

       Args:
           path (`str`):     The path to the files.
    """
    @project_folder_path.setter
    def project_folder_path(self, path):
        if not (type(path) == str):
            raise Exception("pyIMD project path should be a of type string.")
        self._project_folder_path = path

    calculation_mode = property(operator.attrgetter('_calculation_mode'))
    """
       Parameter defining the calculation mode.

       Args:
           mode (`str`):     The calculation mode. PLL, Cont.Sweep or Auto.
    """
    @calculation_mode.setter
    def calculation_mode(self, mode):
        if not (type(mode) == str):
            raise Exception("Calculation mode should be a of type string.")
        self._calculation_mode = mode

    pre_start_no_cell_path = property(operator.attrgetter('_pre_start_no_cell_path'))
    """
       Parameter defining the path to the pre start no cell file.

       Args:
           path (`str`):     Path to the pre start no cell file (.txt).
    """
    @pre_start_no_cell_path.setter
    def pre_start_no_cell_path(self, path):
        if not (type(path) == str):
            raise Exception("Pre start no cell path should be a of type string.")
        self._pre_start_no_cell_path = path

    pre_start_with_cell_path = property(operator.attrgetter('_pre_start_with_cell_path'))
    """
       Parameter defining the path to the pre start with cell file.

       Args:
           path (`str`):     Path to the pre start with cell file (.txt).
    """
    @pre_start_with_cell_path.setter
    def pre_start_with_cell_path(self, path):
        if not (type(path) == str):
            raise Exception("Pre start with cell path should be a of type string.")
        self._pre_start_with_cell_path = path

    measurements_path = property(operator.attrgetter('_measurements_path'))
    """
       Parameter defining the path to the measurement file.

       Args:
           path (`str`):     Path to the measurement file. (.tdms or .txt file).
    """
    @measurements_path.setter
    def measurements_path(self, path):
        if not (type(path) == str):
            raise Exception("Measurements data path should be a of type string.")
        self._measurements_path = path

    selected_files = property(operator.attrgetter('_selected_files'))
    """
      Parameter defining the selected files for calculation.

      Args:
          files (`list`):    Selected files for calculation.
    """
    @selected_files.setter
    def selected_files(self, files):
        if not (type(files) == list):
            raise Exception("Selected files should be a of type list.")
        self._selected_files = files

    image_files = property(operator.attrgetter('_image_files'))
    """
      Parameter defining the image files used for cell tip offset determination.

      Args:
          files (`list`):    Selected files for cell tip offset determination.
    """
    @image_files.setter
    def image_files(self, files):
        if not (type(files) == list):
            raise Exception("Selected files should be a of type list.")
        self._image_files = files

    cell_offsets = property(operator.attrgetter('_cell_offsets'))
    """
      Parameter defining the cell position offset in respect to the cantilever tip for the given image files.

      Args:
          offsets (`list`):    List of the cell position offsets for the given image files.
    """
    @cell_offsets.setter
    def cell_offsets(self, offsets):
        if not (type(offsets) == list):
            raise Exception("Offsets should be a of type list.")
        self._cell_offsets = offsets

    cell_center_of_mass_x = property(operator.attrgetter('_cell_center_of_mass_x'))
    """
      Parameter defining the x component of the cell position centroid for the given image files.

      Args:
          cell_center_of_mass_x (`list`):    List of the x component of the cell position centroid offsets for the given
                                             image files.
    """
    @cell_center_of_mass_x.setter
    def cell_center_of_mass_x(self, x):
        if not (type(x) == list):
            raise Exception("Center of mass x components should be a of type list.")
        self._cell_center_of_mass_x = x

    cell_center_of_mass_y = property(operator.attrgetter('_cell_center_of_mass_y'))
    """
      Parameter defining the y component of the cell position centroid for the given image files.

      Args:
          cell_center_of_mass_y (`list`):    List of the y component of the cell position centroid offsets for the given
                                             image files.
    """
    @cell_center_of_mass_y.setter
    def cell_center_of_mass_y(self, y):
        if not (type(y) == list):
            raise Exception("Center of mass y components should be a of type list.")
        self._cell_center_of_mass_y = y

    ref_line_1_x = property(operator.attrgetter('_ref_line_1_x'))
    """
      Parameter defining the x component of the reference line point 1 for the given image files.

      Args:
          ref_line_1_x (`list`):    List of the x component of the reference line point 1 for the given image files.
    """
    @ref_line_1_x.setter
    def ref_line_1_x(self, x):
        if not (type(x) == list):
            raise Exception("Reference line point 1 x components should be a of type list.")
        self._ref_line_1_x = x

    ref_line_1_y = property(operator.attrgetter('_ref_line_1_y'))
    """
      Parameter defining the y component of the reference line point 1 for the given image files.

      Args:
          ref_line_1_y (`list`):    List of the y component of the reference line point 1 for the given image files.
    """
    @ref_line_1_y.setter
    def ref_line_1_y(self, y):
        if not (type(y) == list):
            raise Exception("Reference line point 1 y components should be a of type list.")
        self._ref_line_1_y = y

    ref_line_2_x = property(operator.attrgetter('_ref_line_2_x'))
    """
      Parameter defining the x component of the reference line point 2 for the given image files.

      Args:
          ref_line_2_x (`list`):    List of the x component of the reference line point 1 for the given image files.
    """

    @ref_line_2_x.setter
    def ref_line_2_x(self, x):
        if not (type(x) == list):
            raise Exception("Reference line point 2 x components should be a of type list.")
        self._ref_line_2_x = x

    ref_line_2_y = property(operator.attrgetter('_ref_line_2_y'))
    """
      Parameter defining the y component of the reference line point 2 for the given image files.

      Args:
          ref_line_2_y (`list`):    List of the y component of the reference line point 2 for the given image files.
    """

    @ref_line_2_y.setter
    def ref_line_2_y(self, y):
        if not (type(y) == list):
            raise Exception("Reference line point 2 y components should be a of type list.")
        self._ref_line_2_y = y

    area = property(operator.attrgetter('_area'))
    """
      Parameter defining the area of the polygon for the given image files.

      Args:
          area (`list`):    List of the area of the polygon for the given image files.
    """

    @area.setter
    def area(self, a):
        if not (type(a) == list):
            raise Exception("Polygon area should be a of type list.")
        self._area = a

    image_start_index = property(operator.attrgetter('_image_start_index'))
    """
      Parameter defining the image start data index for the given image files if experiment and imaging were not started 
      synchronously.

      Args:
          image_start_index (`int`):    Image start data index for the given image files.
    """

    @image_start_index.setter
    def image_start_index(self, idx):
        if not (type(idx) == int):
            raise Exception("Image start data index should be a of type int.")
        self._image_start_index = idx

    position_correction_end_frame = property(operator.attrgetter('_position_correction_end_frame'))
    """
      Parameter defining the image end frame number for the given image files to indicate until where the data can be 
      position correction.

      Args:
          position_correction_end_frame (`int`):    Image end frame number for the given image files.
    """

    @position_correction_end_frame.setter
    def position_correction_end_frame(self, idx):
        if not (type(idx) == int):
            raise Exception("Image end frame number should be a of type int.")
        self._position_correction_end_frame = idx

    number_of_data_per_frame = property(operator.attrgetter('_number_of_data_per_frame'))
    """
      Parameter defining the number of acquired data points between two image frames.

      Args:
          number_of_data_per_frame (`float`):    Number of acquired data points between two image frames.
    """

    @number_of_data_per_frame.setter
    def number_of_data_per_frame(self, idx):
        if not (type(idx) == float):
            raise Exception("Number of data per frame should be a of type float.")
        self._number_of_data_per_frame = idx

    is_zero_outside_correction_range = property(operator.attrgetter('_is_zero_outside_correction_range'))
    """
      Parameter defining the condition if measured data points outside the position correction range should be set to 
      zero (true) or to one (false)

      Args:
          is_zero_outside_correction_range (`bool`):    True if measured data points outside the position correction 
                                                        range should be set to zero. If false to one.
    """

    @is_zero_outside_correction_range.setter
    def is_zero_outside_correction_range(self, condition):
        if not (type(condition) == bool):
            raise Exception("Condition should be of type bool.")
        self._is_zero_outside_correction_range = condition

    def new_pyimd_project(self, pre_start_no_cell_path, pre_start_with_cell_path, measurements_path,
                          text_data_delimiter, read_text_data_from_line, calculation_mode, ** kwargs):
        """
        Create a new pyIMD project with the following arguments. Two modes \
        enable the analysis of different experimental setups. PLL mode and Cont.Sweep mode. For more information please
        read the documentation.

        Args:
            pre_start_no_cell_path (`str`):       File path + file name of initial frequency \
                                                  shift measurement before cell attachment (txt file).
            pre_start_with_cell_path (`str`):     File path + file name of initial frequency \
                                                  shift measurement after cell attachment (txt file).
            measurements_path (`str`):            File path + file name of the actual \
                                                  measurement (tdms file (default) or txt file).
            text_data_delimiter (`str`):          Text file data delimiter i.e '\t' for tab delimited or ',' for
                                                  comma separated data.
            read_text_data_from_line (`int`):     Line number from which data of pre start measurements should be
                                                  read. Typically the first few lines contain header information
                                                  and no data.
            calculation_mode (`str`):             PLL         := phase lock loops mode
                                                  Cont.Sweep  := sweep mode
                                                  Auto        := Auto detection of the mode (experimental)
        Keyword Args:
            figure_width (`float`):                  Width of result figures
            figure_height (`float`):                 Height of result figures
            figure_units (`str`):                    Figure units i.e cm, inch
            figure_format (`str`):                   Figure format i.e png or pdf
            figure_resolution_dpi (`int`):           Resolution of result figures in dpi
            figure_name_pre_start_no_cell (`str`):   Figure name of function fit for pre start with no cell loaded
                                                     data
            figure_name_pre_start_with_cell (`str`): Figure name of function fit for pre start with cell loaded
                                                     data
            figure_name_measured_data (`str`):       Figure name of the resulting mass of the measured data
            figure_plot_every_nth_point ('int'):     Parameter defining how many data points will be plotted. For large
                                                     data stets to increase readability and reducing file size.
            conversion_factor_hz_to_khz (`float`):   Conversion factor to convert from hertz to kilo hertz
            conversion_factor_deg_to_rad (`float`):  Conversion factor to convert from degrees to radian
            conversion_factor_px_to_mum (`float`):   Conversion factor to convert from pixels to microns
            spring_constant (`float`):               Spring constant value of the cantilever
            initial_parameter_guess (`list`):        Initial parameter guess
            lower_parameter_bounds (`list`):         Lower parameter bounds
            upper_parameter_bounds (`list`):         Upper parameter bounds
            rolling_window_size ('int'):             Window size for calculating the rolling average.
            correct_for_frequency_offset ('bool'):   Correct for potential frequency offset during PLL mode.
            frequency_offset_mode ('str'):           Frequency offset correction mode (Auto or Manual)
            frequency_offset_n_measurements_used ('int'): Number of measurement data points to be used for automatic
                                                     frequency offset correction
            frequency_offset ('float'):              Frequency offset either set manually or calculated automatically
            cantilever_length (`float`):             Cantilever length in microns
            cell_position (`float`):                 Cell position offset from cantilever tip in microns
            project_folder_path (`str`):             Path to project data files. Also used to store pyIMD results
                                                     such as data and figures.
            image_files (`list`):                    List of strings with image file name paths used for cell position
                                                     offset determination.
            cell_offsets (`list`):                   List of cell position offsets for the given image series in
                                                     image_files.
            cell_center_of_mass_x (`list`):          List of cell center of mass x components for the given image series
                                                     in image_files.
            cell_center_of_mass_y (`list`):          List of cell center of mass y components for the given image series
                                                     in image_files.
            ref_line_1_x (`list`):                   List of reference line point 1 x components for the given image
                                                     series in image_files.
            ref_line_1_y (`list`):                   List of reference line point 1 y components for the given image
                                                     series in image_files.
            ref_line_2_x (`list`):                   List of reference line point 2 x components for the given image
                                                     series in image_files.
            ref_line_2_y (`list`):                   List of reference line point 2 y components for the given image
                                                     series in image_files.
            area (`list`):                           List of area of polygon for the given image series in image_files.
            image_start_index (`int`):               Measured data index which corresponds to first image frame
            position_correction_end_frame (`int`):   Image frame until which the position should be computed
            number_of_data_per_frame (`float`):        Number of measurement points between two image frames.
            is_zero_outside_correction_range (`bool`):Bool determining if data will be set to zero outside of position
                                                     corrected range
        """

        try:
            attr_names = ['pre_start_no_cell_path', 'pre_start_with_cell_path', 'measurements_path']
            file_names = []
            for idx, file in enumerate([pre_start_no_cell_path, pre_start_with_cell_path, measurements_path]):
                p = pathlib.Path(file)
                if p.is_file():
                    setattr(self, attr_names[idx], file)
                    file_names.append(str(p.name))
                    self.project_folder_path = str(p.parent)
            self.selected_files = file_names

            if any(text_data_delimiter in s for s in ['\t', ' ', ',', ';']):
                self.text_data_delimiter = repr(text_data_delimiter).replace("'", "")
            if read_text_data_from_line == int(read_text_data_from_line) and read_text_data_from_line > 0:
                self.read_text_data_from_line = read_text_data_from_line
            if any(calculation_mode in s for s in ['Auto', 'PLL', 'Cont.Sweep']):
                self.calculation_mode = calculation_mode

            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        except Exception as e:
            "Error during creating a new pyIMD project: " + str(e)

    def read_pyimd_project(self, file_path):
        """
        Read a pre defined pyIMD project form a XML file from disk.

        Args:
            file_path (`str`)   Full path + file name to the pyIMD project file.

        Returns:
            status (`str`):     String reporting the success of failure of loading a pyIMD project.
        """
        try:
            with open(file_path) as fd:
                doc = xmltodict.parse(fd.read())

            # Load pyIMD general settings (parameters)
            general_settings = doc['PyIMDSettings']['GeneralSettings']
            for key, value in general_settings.items():
                if not key == 'text_data_delimiter':
                    try:
                        setattr(self, key, yaml.safe_load(json.loads(json.dumps(value))))
                    except Exception as e:
                        print('General settings error:', e)
                else:
                    # fix escape characters ie \\t or \\n or \\s
                    setattr(self, key, value.replace("'", ""))

            # Update ui with loaded data:
            ui_settings = doc['PyIMDSettings']['ProjectSettings']

            for key, value in ui_settings.items():
                try:
                    if key == 'selected_files' or key == 'image_files':
                        setattr(self, key, value['File'])
                    elif key == 'cell_offsets':
                        setattr(self, key, self.parse_list(value['Offset'])) #[float(i) for i in value['Offset']])
                    elif key == 'cell_center_of_mass_x':
                        setattr(self, key, self.parse_list(value['CenterOfMassX']))
                    elif key == 'cell_center_of_mass_y':
                        setattr(self, key, self.parse_list(value['CenterOfMassY']))
                    elif key == 'ref_line_1_x':
                        setattr(self, key, self.parse_list(value['RefLine1X']))
                    elif key == 'ref_line_1_y':
                        setattr(self, key, self.parse_list(value['RefLine1Y']))
                    elif key == 'ref_line_2_x':
                        setattr(self, key, self.parse_list(value['RefLine2X']))
                    elif key == 'ref_line_2_y':
                        setattr(self, key, self.parse_list(value['RefLine2Y']))
                    elif key == 'area':
                        setattr(self, key, self.parse_list(value['Area']))
                    elif key == 'PositionCorrection':
                        for p_key, p_value in value.items():
                            if p_key == 'image_files':
                                setattr(self, p_key, p_value['File'])
                            elif p_key == 'CorrectionObject':
                                data = []
                                for el in p_value:
                                    tmp = {}
                                    for o_key, o_value in el.items():
                                        tmp[o_key] = ast.literal_eval(o_value)
                                    data.append(tmp)
                                setattr(self, 'position_correction_data', data)
                    else:
                        setattr(self, key, yaml.safe_load(json.loads(json.dumps(value))))

                except Exception as e:
                    if key not in ['PositionCorrection', 'cell_offsets', 'cell_center_of_mass_x', 'cell_center_of_mass_y',
                               'ref_line_1_x', 'ref_line_1_y', 'ref_line_2_x', 'ref_line_2_y', 'area']:
                        print(f'Project settings error: {key} {value}', e)
            return "Project {} successfully opened".format(pathlib.Path(file_path).name)
        except Exception as e:
            return "Error during opening project: " + str(e)

    @staticmethod
    def parse_list(list_in):
        """
        Parses a list of string.
        Args:
            list_in (`list`)      List of strings.

        Returns:
            list_out (`list`):     Converted list of correct data type (float, nan).
        """
        list_out = []
        for i in list_in:
            if i == 'nan':
                list_out.append(np.nan)
            else:
                list_out.append(float(i))
        return list_out

    def write_pyimd_project(self, file_path):
        """
        Write the current pyIMD project as XML file to disk.
        Args:
            file_path (`str`)   Full path + file name to the pyIMD project file.

        Returns:
            status (`str`):     String reporting the success of failure of loading a pyIMD project.
        """
        try:
            # Create the root element
            root = etree.Element('PyIMDSettings', creator='pyIMD',
                                 timestamp=datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S'))
            # Make a new document tree
            doc = etree.ElementTree(root)
            # Add the SubElements
            general_settings = etree.SubElement(root, 'GeneralSettings')
            project_settings = etree.SubElement(root, 'ProjectSettings')
            position_correction = etree.SubElement(project_settings, 'PositionCorrection')

            # Add the SubSubElements for the general settings
            figure_format = etree.SubElement(general_settings, 'figure_format')
            figure_width = etree.SubElement(general_settings, 'figure_width')
            figure_height = etree.SubElement(general_settings, 'figure_height')
            figure_units = etree.SubElement(general_settings, 'figure_units')
            figure_resolution = etree.SubElement(general_settings, 'figure_resolution_dpi')
            figure_name_pre_start_no_cell = etree.SubElement(general_settings, 'figure_name_pre_start_no_cell')
            figure_name_pre_start_with_cell = etree.SubElement(general_settings, 'figure_name_pre_start_with_cell')
            figure_name_measured_data = etree.SubElement(general_settings, 'figure_name_measured_data')
            figure_plot_every_nth_point = etree.SubElement(general_settings, 'figure_plot_every_nth_point')
            conversion_factor_hz_to_khz = etree.SubElement(general_settings, 'conversion_factor_hz_to_khz')
            conversion_factor_deg_to_rad = etree.SubElement(general_settings, 'conversion_factor_deg_to_rad')
            conversion_factor_px_to_mum = etree.SubElement(general_settings, 'conversion_factor_px_to_mum')
            spring_constant = etree.SubElement(general_settings, 'spring_constant')
            cantilever_length = etree.SubElement(general_settings, 'cantilever_length')
            cell_position = etree.SubElement(general_settings, 'cell_position')
            initial_parameter_guess = etree.SubElement(general_settings, 'initial_parameter_guess')
            lower_parameter_bounds = etree.SubElement(general_settings, 'lower_parameter_bounds')
            upper_parameter_bounds = etree.SubElement(general_settings, 'upper_parameter_bounds')
            rolling_window_size = etree.SubElement(general_settings, 'rolling_window_size')
            correct_for_frequency_offset = etree.SubElement(general_settings, 'correct_for_frequency_offset')
            frequency_offset_mode = etree.SubElement(general_settings, 'frequency_offset_mode')
            frequency_offset_n_measurements_used = etree.SubElement(general_settings,
                                                                    'frequency_offset_n_measurements_used')
            frequency_offset = etree.SubElement(general_settings, 'frequency_offset')
            read_text_data_from_line = etree.SubElement(general_settings, 'read_text_data_from_line')
            text_data_delimiter = etree.SubElement(general_settings, 'text_data_delimiter')
            # Add the SubSubElements for the project settings
            project_folder_path = etree.SubElement(project_settings, 'project_folder_path')
            data_pre_start_no_cell = etree.SubElement(project_settings, 'pre_start_no_cell_path')
            data_pre_start_with_cell = etree.SubElement(project_settings, 'pre_start_with_cell_path')
            data_measured = etree.SubElement(project_settings, 'measurements_path')
            calculation_mode = etree.SubElement(project_settings, 'calculation_mode')
            selected_files = etree.SubElement(project_settings, 'selected_files')
            image_files = etree.SubElement(position_correction, 'image_files')
            cell_offsets = etree.SubElement(project_settings, 'cell_offsets')
            cell_center_of_mass_x = etree.SubElement(project_settings, 'cell_center_of_mass_x')
            cell_center_of_mass_y = etree.SubElement(project_settings, 'cell_center_of_mass_y')
            ref_line_1_x = etree.SubElement(project_settings, 'ref_line_1_x')
            ref_line_1_y = etree.SubElement(project_settings, 'ref_line_1_y')
            ref_line_2_x = etree.SubElement(project_settings, 'ref_line_2_x')
            ref_line_2_y = etree.SubElement(project_settings, 'ref_line_2_y')
            area = etree.SubElement(project_settings, 'area')
            image_start_index = etree.SubElement(project_settings, 'image_start_index')
            position_correction_end_frame = etree.SubElement(project_settings, 'position_correction_end_frame')
            number_of_data_per_frame = etree.SubElement(project_settings, 'number_of_data_per_frame')
            is_zero_outside_correction_range = etree.SubElement(project_settings, 'is_zero_outside_correction_range')

            # Add the data
            figure_format.text = str(self.figure_format)
            figure_width.text = str(self.figure_width)
            figure_height.text = str(self.figure_height)
            figure_units.text = str(self.figure_units)
            figure_resolution.text = str(self.figure_resolution_dpi)
            figure_name_pre_start_no_cell.text = str(self.figure_name_pre_start_no_cell)
            figure_name_pre_start_with_cell.text = str(self.figure_name_pre_start_with_cell)
            figure_name_measured_data.text = str(self.figure_name_measured_data)
            figure_plot_every_nth_point.text = str(self.figure_plot_every_nth_point)
            conversion_factor_hz_to_khz.text = str(self.conversion_factor_hz_to_khz)
            conversion_factor_deg_to_rad.text = str(self.conversion_factor_deg_to_rad)
            conversion_factor_px_to_mum.text = str(self.conversion_factor_px_to_mum)
            spring_constant.text = str(self.spring_constant)
            cantilever_length.text = str(self.cantilever_length)
            cell_position.text = str(self.cell_position)
            initial_parameter_guess.text = str(self.initial_parameter_guess)
            lower_parameter_bounds.text = str(self.lower_parameter_bounds)
            upper_parameter_bounds.text = str(self.upper_parameter_bounds)
            rolling_window_size.text = str(self.rolling_window_size)
            correct_for_frequency_offset.text = str(self.correct_for_frequency_offset)
            frequency_offset_mode.text = str(self.frequency_offset_mode)
            frequency_offset_n_measurements_used.text = str(self.frequency_offset_n_measurements_used)
            frequency_offset.text = str(self.frequency_offset)
            read_text_data_from_line.text = str(self.read_text_data_from_line)
            text_data_delimiter.text = self.text_data_delimiter
            project_folder_path.text = str(self.project_folder_path)
            data_pre_start_no_cell.text = str(self.pre_start_no_cell_path)
            data_pre_start_with_cell.text = str(self.pre_start_with_cell_path)
            data_measured.text = str(self.measurements_path)
            calculation_mode.text = str(self.calculation_mode)
            image_start_index.text = str(self.image_start_index)
            position_correction_end_frame.text = str(self.position_correction_end_frame)
            number_of_data_per_frame.text = str(self.number_of_data_per_frame)
            is_zero_outside_correction_range.text = str(self.is_zero_outside_correction_range)

            file_dict = {}
            for i in range(0, len(self.selected_files)):
                file_dict["string{0}".format(i)] = etree.SubElement(selected_files, 'File')
                file_dict["string{0}".format(i)].text = pathlib.Path(self.selected_files[i]).name

            image_files_dict = {}
            for i in range(0, len(self.image_files)):
                image_files_dict["string{0}".format(i)] = etree.SubElement(image_files, 'File')
                image_files_dict["string{0}".format(i)].text = self.image_files[i]

            cell_offsets_dict = {}
            cell_center_of_mass_x_dict = {}
            cell_center_of_mass_y_dict= {}
            ref_line_1_x_dict = {}
            ref_line_1_y_dict = {}
            ref_line_2_x_dict = {}
            ref_line_2_y_dict = {}
            area_dict = {}
            for i in range(0, len(self.cell_offsets)):
                cell_offsets_dict["string{0}".format(i)] = etree.SubElement(cell_offsets, 'Offset')
                cell_offsets_dict["string{0}".format(i)].text = str(self.cell_offsets[i])
                cell_center_of_mass_x_dict["string{0}".format(i)] = etree.SubElement(cell_center_of_mass_x,
                                                                                     'CenterOfMassX')
                cell_center_of_mass_x_dict["string{0}".format(i)].text = str(self.cell_center_of_mass_x[i])
                cell_center_of_mass_y_dict["string{0}".format(i)] = etree.SubElement(cell_center_of_mass_y,
                                                                                     'CenterOfMassY')
                cell_center_of_mass_y_dict["string{0}".format(i)].text = str(self.cell_center_of_mass_y[i])
                ref_line_1_x_dict["string{0}".format(i)] = etree.SubElement(ref_line_1_x, 'RefLine1X')
                ref_line_1_x_dict["string{0}".format(i)].text = str(self.ref_line_1_x[i])
                ref_line_1_y_dict["string{0}".format(i)] = etree.SubElement(ref_line_1_y, 'RefLine1Y')
                ref_line_1_y_dict["string{0}".format(i)].text = str(self.ref_line_1_y[i])
                ref_line_2_x_dict["string{0}".format(i)] = etree.SubElement(ref_line_2_x, 'RefLine2X')
                ref_line_2_x_dict["string{0}".format(i)].text = str(self.ref_line_2_x[i])
                ref_line_2_y_dict["string{0}".format(i)] = etree.SubElement(ref_line_2_y, 'RefLine2Y')
                ref_line_2_y_dict["string{0}".format(i)].text = str(self.ref_line_2_y[i])
                area_dict["string{0}".format(i)] = etree.SubElement(area, 'Area')
                area_dict["string{0}".format(i)].text = str(self.area[i])

            for i in self.position_correction_data:
                correction_object = etree.SubElement(position_correction, 'CorrectionObject')
                element_dict = {}
                for key in i.keys():
                    element_dict["string{0}".format(i)] = etree.SubElement(correction_object, key)
                    element_dict["string{0}".format(i)].text = str(i[key])

            # Check for correct file suffix. If not provided by user or wrong suffix given correct it
            if not pathlib.Path(file_path).suffix:
                save_file_name = file_path + '.xml'
            elif pathlib.Path(file_path).suffix != '.xml':
                file_path.suffix = '.xml'
                save_file_name = file_path
            else:
                save_file_name = file_path

            # Save to XML file
            doc.write(save_file_name, xml_declaration=True, encoding='utf-8', method="xml", standalone=False,
                      pretty_print=True)

            return "Project saved successfully"
        except Exception as e:
            return "Error during saving project: " + str(e)

