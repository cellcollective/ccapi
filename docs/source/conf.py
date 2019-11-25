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

import ccpaw

project   = ccpaw.__name__
author    = ccpaw.__author__
copyright = "%s %s" % (NOW.year, ccpaw.__author__)

version   = ccpaw.__version__
release   = ccpaw.__version__

source_suffix       = [".rst", ".md"]
source_parsers      = { ".md": "recommonmark.parser.CommonMarkParser" }

master_doc          = "index"

exclude_patterns    = [
    osp.join(BASEDIR,"source","notebooks",".ipynb_checkpoints")
]

extensions          = [
    "sphinx.ext.autodoc",
    "nbsphinx"
]

templates_path      = [osp.join(BASEDIR, "source", "_templates")]

html_static_path    = [osp.join(BASEDIR, "source", "_static")]

html_sidebars       = {
    "index": ["sidebar.html"],
    "**": [
        "sidebar.html"
    ]
}