.. highlight:: shell

============
Installation
============


Stable release
--------------
As module
^^^^^^^^^


To install pyIMD, just run this command in your terminal:

.. code-block:: console

    $ pip install pyIMD

Installing pyIMD this way ensures that you get always the latest release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

As stand alone executable
^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to install pyIMD on your system without installing Python yourself just download the
pre-compiled executable matching your operating system:

.. only:: html

    * `Download the latest in one portable for WINDOWS, UNIX, OSX x64 systems <https://github.com/cunyap/pyIMD/releases/>`_

pyIMD can then be used trough its graphical user interface (GUI) directly.

From sources
------------

First, install Python. An easy way to do so is to install miniconda for your operating system with Python 3.7-11.

`https://docs.conda.io/en/latest/miniconda.html`

If you have other Python installations it is good practice to install everything new into a separate environment.
Also such an environment can be later used to create a snapshot of your installation and shared with other to build
exactly the identical environment.

Start the terminal (Linux, Mac OS) or (Anaconda Prompt under Windows) and type:

.. code-block:: console

    conda create -n <MYENV> python=3.7


Rename <MYENV> with the name you want to give to your environment. For example pyIMD.
pyIMD has been tested with Python 3.7-3.11.

Activate the environment you just created.

.. code-block:: console

    conda activate <MYENV>


_Note: more information about conda environments can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)_

The latest sources for pyIMD can be downloaded from the `Github repo`_.

You can clone the public repository:

.. code-block:: console

    $ git clone https://github.com/cunyap/pyIMD.git

Once you have a copy of the source, navigate into the directory and run:

.. code-block:: console

    $ python setup.py install .

Then add the repository to the Python path:

.. code-block:: console

    export PYTHONPATH=$PYTHONPATH:pwd

To run the demo Jupyter notebook also install Jupyter Lab:

.. code-block:: console

    pip install jupyterlab

For development we suggest to install PyCharm where pyIMD can be run from source to either as script or with the GUI.

.. _Github repo: https://github.com/cunyap/pyIMD
