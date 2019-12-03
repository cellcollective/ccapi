# imports - standard imports
import os.path as osp

# imports - test imports
import pytest

# imports - module imports
from ccapi.template  import render_template
from ccapi.exception import TemplateNotFoundError

_TEST_DATA_DIR = osp.join(osp.abspath(osp.dirname(__file__)), "data")

def test_render_template():
    render_template("test.html",
        context = dict(name = "Test")) \
        == "Hello, Test!"
    render_template("test.html",
        context = dict(name = "World")) \
        == "Hello, World!"
    render_template("test.html", name = "Test") \
        == "Hello, Test!"
        
    dir_ = osp.join(_TEST_DATA_DIR, "templates")
    render_template("foobar.html", dirs = dir_,   bar  = "baz") \
        == "foobaz"
    render_template("foobar.html", dirs = [dir_], bar  = "bar") \
        == "foobar"
    render_template("test.html",   dirs = [dir_], name = "Baz") \
        == "Hello, Baz!"

    with pytest.raises(TemplateNotFoundError):
        render_template("foobaz.html")