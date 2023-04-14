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

import os
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from pyIMD.plotting.figures import create_montage_array
from pyIMD.imd import InertialMassDetermination

# Create the inertial mass determination object
imd = InertialMassDetermination()

# Create a config file for the project / experiment to analyze using default values. Note non default parameters can be
# added as optional arguments for e.g. spring_constant = 5.
file_path1 = str(Path(Path(__file__).parent, 'data', 'show_case', '20190110_ShowCase_PLL_A.txt'))
file_path2 = str(Path(Path(__file__).parent, 'data', 'show_case', '20190110_ShowCase_PLL_B.txt'))
file_path3 = str(Path(Path(__file__).parent, 'data', 'show_case', '20190110_ShowCase_PLL_LongTerm.txt'))
imd.create_pyimd_project(file_path1, file_path2, file_path3, '\t', 23, 'PLL', figure_width=5.4, figure_height=9.35,
                         initial_parameter_guess=[73.0, 5.2, 0.0, 0.0], upper_parameter_bounds=[100.0, 8.0, 3.0, 3.0],
                         spring_constant=8.0, cell_position=10, cantilever_length=100.0)
# Run the inertial mass determination
imd.run_inertial_mass_determination()

image_file_path = str(Path(Path(__file__).parent, 'data', 'show_case', 'images'))
data_path = str(Path(Path(__file__).parent, 'data', 'show_case', 'CalculatedCellMass.csv'))
figure_rows = 1
rows_to_plot = 10  # 1 := all data
images_to_plot = 6

# Create list of all image files
files = []
for file in os.listdir(image_file_path):
    if file.endswith(".tif"):
        files.append(os.path.join(image_file_path, file))

# Read images to image stack
image_array = []
for iFile in files:
    a = plt.imread(iFile) #, flatten=1)
    image_array.append(a)
image_stack = np.array(image_array)

size = np.array([figure_rows, np.nan])
montage = create_montage_array(image_stack[0:images_to_plot, :, :], size)

# Read the calculated mass data from csv
p = Path(data_path)
mass_data = pd.read_csv(data_path, sep=',')
mass_data['Mean mass (ng)'] = mass_data['Mass (ng)'].rolling(window=1000).mean()

# Plot data
fig = plt.figure(figsize=(4.74, 4.74))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.plot(mass_data.iloc[0::rows_to_plot, 0]*60, mass_data.iloc[0::rows_to_plot, 1], 'ko', alpha=0.07, markersize=3)
ax1.plot(mass_data.iloc[0::rows_to_plot, 0]*60, mass_data.iloc[0::rows_to_plot, 2], 'r-', linewidth=0.8)
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Mass (ng)')
ax1.legend(['Measured data', 'Rolling mean', 'Bud event'], frameon=False)

# Plot images
ax2.imshow(montage, cmap='gray', vmin=0, vmax=256)
# Set proper figure labels
ticks_x = np.arange(0, montage.shape[1], step=image_stack.shape[2]/2)
x_names = []
x_ticks = []
for i in range(1, ticks_x.shape[0], 2):
    x_names.append(i)
    x_ticks.append(ticks_x[i])
x_names = np.array(x_names)
x_ticks = np.array(x_ticks)

x_tick_names = np.arange(0, x_names.shape[0]) * 3
plt.xticks(x_ticks, x_tick_names)
ticks_y = np.arange(0, montage.shape[0], step=image_stack.shape[1]/2)
y_names = []
for i in range(1, int(montage.shape[0]/image_stack.shape[1])*int(montage.shape[1]/image_stack.shape[2]),
               int(montage.shape[1]/image_stack.shape[2])):
    y_names.append(i)

y_ticks = []
for i in range(1, ticks_y.shape[0], 2):
    y_ticks.append(ticks_y[i])

y_names = np.array(y_names)
y_ticks = np.array(y_ticks)
y_tick_names = np.arange(y_names.shape[0])

plt.yticks(y_ticks, y_names)
plt.xlabel('Time (min)')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
plt.savefig(str(Path(p.parent, 'ResultFigureMontage.png')), dpi=300)
print(f"Figure saved: {str(Path(p.parent, 'ResultFigureMontage.png'))}")




