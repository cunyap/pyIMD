# -*- mode: python -*-
# Main script to bundle pyIMD
# Author Andreas P. Cuny, andreas.cuny@bsse.ethz.ch
# Use the following command to build the executable with pyinstaller==3.3.1 !
# pyinstaller --noconsole --onefile --icon=/home/andreascuny/Documents/pyIMD/pyIMD/ui/icons/pyIMD_logo_icon.ico /home/andreascuny/Documents/pyIMD/pyIMD/pyIMD_unix.spec


import sys
sys.setrecursionlimit(3000)
block_cipher = None

a = Analysis(['/home/andreascuny/Documents/pyIMD/pyIMD/main.py'],
             pathex=['/home/andreascuny/pyIMDENV/lib/python3.6/site-packages/PyInstaller/'],
             binaries=[],
             datas=[],
             hiddenimports=["tkinter", "tkinter.filedialog", "pandas._libs.tslibs.np_datetime","pandas._libs.tslibs.nattype","pandas._libs.skiplist", 
    			    "scipy.optimize", "scipy.optimize.minipack2", "pyIMD", "plotnine", "mizani", "palettable.colorbrewer", "statsmodels.tsa.statespace",
    			    'statsmodels.tsa.statespace._kalman_filter', 'statsmodels.tsa.statespace._kalman_smoother', 'statsmodels.tsa.statespace._representation',
    			    'statsmodels.tsa.statespace._simulation_smoother', 'statsmodels.tsa.statespace._statespace', 'statsmodels.tsa.statespace._tools',
    			    'statsmodels.tsa.statespace._filters._conventional', 'statsmodels.tsa.statespace._filters._inversions', 
			    'statsmodels.tsa.statespace._filters._univariate', 'statsmodels.tsa.statespace._smoothers._alternative', 
			    'statsmodels.tsa.statespace._smoothers._classical',	'statsmodels.tsa.statespace._smoothers._conventional',
    			    'statsmodels.tsa.statespace._smoothers._univariate', 'PyQt5.sip'],
             hookspath=['/home/andreascuny/Documents/pyIMD/pyIMD/ui/hooks/'],
             runtime_hooks=[],
             excludes=['jinja2'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			  
	 
a.datas += [('ui/icons/pyIMD_logo_icon.ico','/home/andreascuny/Documents/pyIMD/pyIMD/ui/icons/pyIMD_logo_icon.ico','DATA'),
            ('ui/icons/pyIMD_logo.png','/home/andreascuny/Documents/pyIMD/pyIMD/ui/icons/pyIMD_logo.png','DATA'),
            ('ui/icons/pyIMD_logo_vect.svg','/home/andreascuny/Documents/pyIMD/pyIMD/ui/icons/pyIMD_logo_vect.svg','DATA'),
			('ui/main_window.ui','/home/andreascuny/Documents/pyIMD/pyIMD/ui/main_window.ui','DATA'),
			('ui/setting_dialog.ui','/home/andreascuny/Documents/pyIMD/pyIMD/ui/setting_dialog.ui','DATA'),
			('imd.py','/home/andreascuny/Documents/pyIMD/pyIMD/imd.py','DATA'),
			('change_log.txt','/home/andreascuny/Documents/pyIMD/pyIMD/change_log.txt','DATA')]
			    			 			 
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
          upx=False,
          console=False,
	  icon='/home/andreascuny/Documents/pyIMD/pyIMD/ui/icons/pyIMD_logo_icon.ico')
