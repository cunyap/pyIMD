from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
hiddenimports = collect_submodules('pgcolorbar')

datas = collect_data_files('pgcolorbar')