

## Build executable from source:

Has been tested under `Windows 10 Enterprise LTC 64-bit (10.0, Build 17763)` with `miniconda3` version: 
```bash
conda version : 4.6.8                                   
conda-build version : 3.17.8                            
python version : 3.6.8.final.0
```

and `Python 3.7.0 (default, Jun 28 2018, 08:04:48) [MSC v.1912 64 bit (AMD64)] :: Anaconda, Inc. on win32` and  the following Python module versions in a clean environment:

```
altgraph==0.17
certifi==2020.12.5
cycler==0.10.0
descartes==1.1.0
future==0.18.2
importlib-metadata==3.4.0
kiwisolver==1.3.1
lxml==4.6.2
matplotlib==3.3.4
mizani==0.7.2
npTDMS==1.1.0
numpy==1.20.0
palettable==3.3.0
pandas==1.1.5
patsy==0.5.1
pefile==2019.4.18
Pillow==8.1.0
plotnine==0.7.1
pyinstaller==4.2
pyinstaller-hooks-contrib==2020.11
pyparsing==2.4.7
PyQt5==5.15.2
PyQt5-sip==12.8.1
pyqtgraph==0.11.1
python-dateutil==2.8.1
pytz==2021.1
pywin32-ctypes==0.2.0
PyYAML==5.4.1
scipy==1.6.0
six==1.15.0
statsmodels==0.12.2
tqdm==4.56.0
typing-extensions==3.7.4.3
wincertstore==0.2
xmltodict==0.12.0
zipp==3.4.0
```




1. Install system `Python3` or `miniconda3`.

    [Download miniconda](https://docs.conda.io/en/latest/miniconda.html)

       If you have other Python installations it is good practice to install everything new into a separate environment. Also such an environment  can be later used to create a snapshot of your installation and shared  with other to build exactly the identical environment.

2. Create a new environment "pyimd" with:

    ```bash
    conda create -n pyimd python=3.7
    activate pyimd
    ```

    Note: More information about conda environments can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

3. You can clone the public repository:

    ```
    git clone https://github.com/cunyap/pyIMD.git
    git checkout win10
    ```
    With the activated environment pip install the above mentioned modules:
    
    ```bash
    pip install pandas>=0.20.0 numpy>=1.14.5 scipy==1.6.0 nptdms>=0.12.0 tqdm>=4.23.4 plotnine==0.7.1 PyQT5 lxml==4.6.2 xmltodict==0.12.0 matplotlib==3.3.4 pyyaml==5.4.1 pyqtgraph==0.11.1 xmlunittest PyInstaller==4.2
    ```

4. Compile the exe with

   ```
   pyinstaller --onefile <PATH\TO\REPO>\pyIMD\pyIMD\pyIMD_win10.spec                                 
   ```

5. Run the app with from the cmd or by double clicking on the exe

   ```
   <PATH\TO\REPO>\pyIMD\dist\pyIMD.exe
   ```

   
