# -*- mode: python -*-
# Main script to bundle pyIMD on OSX.
# Author Andreas P. Cuny, andreas.cuny@bsse.ethz.ch
# Use the following command to build the executable with pyinstaller and adjust the file paths first according to your installation.
# PyInstaller --noconsole --onefile /Users/travis/build/cunyap/pyIMD/pyIMD/build/pyIMD_osx.spec

# work-around for https://github.com/pyinstaller/pyinstaller/issues/4064
# import distutils
# if distutils.distutils_path.endswith('__init__.py'):
#     distutils.distutils_path = os.path.dirname(distutils.distutils_path)
import os
from pathlib import Path
working_dir = Path(os.path.abspath(SPECPATH)).parent
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

a = Analysis([str(Path(working_dir / 'main.py' ))],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=["PyQt5", "numpy", "PyQt5.QtWidgets", "PyQt5.sip", "platinfo", "tkinter", "tkinter.filedialog", "pandas._libs.tslibs.np_datetime","pandas._libs.tslibs.nattype","pandas._libs.skiplist",
							"scipy.optimize", "scipy.optimize.minipack", "pyIMD", "plotnine", "mizani", "palettable.colorbrewer", "statsmodels", "statsmodels.tools", "statsmodels.tsa.statespace._filters",
							"statsmodels.tsa.statespace._filters._conventional", "statsmodels.tsa.statespace._filters._inversions",  "statsmodels.tsa.statespace._filters._univariate",
							"statsmodels.tsa.statespace._smoothers", "statsmodels.tsa.statespace._smoothers._alternative", "statsmodels.tsa.statespace._smoothers._classical",
							"statsmodels.tsa.statespace._smoothers._conventional", "statsmodels.tsa.statespace._smoothers._univariate", "scipy._lib.messagestream", "palettable","statsmodels.__init__",
							"pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt5", "pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt5", "pyqtgraph.imageview.ImageViewTemplate_pyqt5"],
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
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon=str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo_icon.ico')))

app = BUNDLE(exe,
         name='pyIMD.app',
         icon=str(Path(working_dir / 'ui' / 'icons' / 'pyIMD_logo_icon.ico')),
         bundle_identifier=None,
         info_plist={'NSHighResolutionCapable': 'True'},
         )
