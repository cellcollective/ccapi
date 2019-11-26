import sys
import os, os.path as osp
import datetime as dt

def pardir(path, level = 1):
    for _ in range(level):
        path = osp.dirname(path)
    return path

BASEDIR = osp.abspath(pardir(__file__, 3))
DOCSDIR = osp.join(BASEDIR, "docs")
NOW     = dt.datetime.now()

sys.path.insert(0, BASEDIR)

import ccpaw

project   = ccpaw.__name__
author    = ccpaw.__author__
copyright = "%s %s" % (NOW.year, ccpaw.__author__)

version   = ccpaw.__version__
release   = ccpaw.__version__

source_suffix       = [".rst"]

master_doc          = "index"

exclude_patterns    = [
    osp.join(DOCSDIR,"source","notebooks",".ipynb_checkpoints")
]

extensions          = [
    "sphinx.ext.autodoc",
    "nbsphinx"
]

templates_path      = [
    osp.join(DOCSDIR,"source","_templates")
]

html_static_path    = [
    osp.join(DOCSDIR,"source","_static")
]

html_sidebars       = {
    "index": ["sidebar.html"],
    "**": [
        "sidebar.html"
    ]
}