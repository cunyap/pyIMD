from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
hiddenimports = collect_submodules('distributed')

datas = collect_data_files('distributed')