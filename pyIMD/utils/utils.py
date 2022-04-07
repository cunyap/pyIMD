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

from IPython import get_ipython


def is_in_notebook():
    """
    Test if code is run from a ipython/jupyter notebook or form the shell / gui.
    For more information see https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook

    Returns:
        ret (`bool`):      Returns true if code is run from ipython/jupyter, false otherwise.
    """
    ipy = get_ipython()
    if ipy is None:
        return False
    elif "IPKernelApp" in ipy.config:
        return True


def set_backend():
    """
    Returns the appropriate matplotlib backend to be set depending on the platform.

    Returns:
        backend (`str`):      Returns the matplotlib backend to be set.
    """
    if is_in_notebook():
        return 'nbAgg'
    else:
        return 'Qt5Agg'
