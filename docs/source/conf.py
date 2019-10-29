import sys
import os, os.path as osp
import datetime as dt

def pardir(path, level = 1):
    for _ in range(level):
        path = osp.dirname(path)
    return path

BASEDIR = osp.abspath(pardir(__file__, 2))
NOW     = dt.datetime.now()

sys.path.insert(0, BASEDIR)

import cc

project   = cc.__name__
author    = cc.__author__
copyright = "%s %s" % (NOW.year, cc.__author__)

version   = cc.__version__
release   = cc.__version__

source_suffix  = [".rst", ".md"]
source_parsers = { ".md": "recommonmark.parser.CommonMarkParser" }

master_doc  = "index"

extensions  = [
    'sphinx.ext.autodoc',

    # IPython directive
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive'
]