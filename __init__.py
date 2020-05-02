import sys

if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
    pass
else:
    raise Exception("dynamic_plot: Python 3.6 or a more recent version is required.")

from .dynamic_plot import *
