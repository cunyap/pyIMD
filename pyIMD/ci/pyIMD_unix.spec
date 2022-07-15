# -*- mode: python -*-
# Main script to bundle pyIMD
# Author Andreas P. Cuny, andreas.cuny@bsse.ethz.ch
# Use the following command to build the executable with pyinstaller==3.3.1 !
# pyinstaller --noconsole --onefile --icon=/home/travis/build/cunyap/pyIMD/pyIMD/ui/icons/pyIMD_logo_icon.ico /home/travis/build/cunyap/pyIMD/pyIMD/build/pyIMD_unix.spec

import os
import sys
from pathlib import Path
# sys.setrecursionlimit(3000)

block_cipher = None

working_dir = Path(os.path.abspath(SPECPATH)).parent
from PyInstaller.utils.hooks import collect_dynamic_libs

# additionalLibs = []
# additionalLibs.append( ("libGL.so.1", "/usr/lib64/libGL.so.1", 'BINARY') )

a = Analysis([str(Path(working_dir / 'main.py' ))],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=["tkinter", "tkinter.filedialog", "pandas._libs.tslibs.np_datetime","pandas._libs.tslibs.nattype","pandas._libs.skiplist",
    			    "scipy.optimize", "scipy.optimize.minipack2", "pyIMD", "plotnine", "mizani", "palettable.colorbrewer", "statsmodels.tsa.statespace",
    			    'statsmodels.tsa.statespace._kalman_filter', 'statsmodels.tsa.statespace._kalman_smoother', 'statsmodels.tsa.statespace._representation',
    			    'statsmodels.tsa.statespace._simulation_smoother', 'statsmodels.tsa.statespace._statespace', 'statsmodels.tsa.statespace._tools',
    			    'statsmodels.tsa.statespace._filters._conventional', 'statsmodels.tsa.statespace._filters._inversions',
			    'statsmodels.tsa.statespace._filters._univariate', 'statsmodels.tsa.statespace._smoothers._alternative',
			    'statsmodels.tsa.statespace._smoothers._classical',	'statsmodels.tsa.statespace._smoothers._conventional',
    			    'statsmodels.tsa.statespace._smoothers._univariate', 'PyQt5.sip', 'cmlib', 'imagecodecs',
    			    "pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt5", "pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt5",
    			    "pyqtgraph.imageview.ImageViewTemplate_pyqt5"],
             hookspath=[str(Path(working_dir / 'ui' / 'hooks'))],
             runtime_hooks=[],
             excludes=['jinja2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


a.datas += [('ui/icons/pyIMD_logo_icon.ico', str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo_icon.ico')),'DATA'),
            ('ui/icons/pyIMD_logo.png', str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo.png')),'DATA'),
            ('ui/icons/pyIMD_logo_vect.svg',  str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo_vect.svg')),'DATA'),
            ('ui/icons/Icons-01.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-01.png')),'DATA'),
            ('ui/icons/Icons-02.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-02.png')),'DATA'),
            ('ui/icons/Icons-03.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-03.png')),'DATA'),
            ('ui/icons/Icons-04.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-04.png')),'DATA'),
            ('ui/icons/Icons-05.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-05.png')),'DATA'),
            ('ui/icons/Icons-06.png',  str(Path(working_dir / 'ui' / 'icons' / 'Icons-06.png')),'DATA'),
			('ui/main_window.ui', str(Path(working_dir / 'ui' / 'main_window.ui')),'DATA'),
			('ui/positioncorrectionui.ui', str(Path(working_dir / 'ui' / 'positioncorrectionui.ui')), 'DATA'),
			('ui/setting_dialog.ui', str(Path(working_dir / 'ui' / 'setting_dialog.ui')),'DATA'),
			('imd.py', str(Path(working_dir / 'imd.py')),'DATA'),
			('change_log.txt', str(Path(working_dir / 'change_log.txt')),'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyIMD',
          debug=True,
          strip=False,
          upx=True,
          console=True,
		  icon=str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo_icon.ico')))
