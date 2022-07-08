# -*- mode: python -*-
# Main script to bundle pyIMD
# Author Andreas P. Cuny, andreas.cuny@bsse.ethz.ch
# Use the following command to build the executable with pyinstaller
# C:\\Python35-3-3-64\\Scripts pyinstaller.exe --noconsole --onefile <PATH\TO>\pyIMD_win.spec

block_cipher = None

import os
from pathlib import Path
working_dir = Path(os.path.abspath(SPECPATH)).parent
from PyInstaller.utils.hooks import collect_dynamic_libs

a = Analysis([str(Path(working_dir / 'main.py' ))],
             pathex=['C:\\Python35-3-3-64\\lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Python35-3-3-64\\Scripts'],
             binaries=collect_dynamic_libs("rtree"),
             datas=[],
             hiddenimports=["tkinter", "tkinter.filedialog", "pandas._libs.tslibs.np_datetime","pandas._libs.tslibs.nattype","pandas._libs.skiplist", 
			 "scipy.optimize", "scipy.optimize.minipack2", "pyIMD", "plotnine", "mizani", "palettable.colorbrewer", "statsmodels.tsa.statespace", "cmlib", "imagecodecs"],
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