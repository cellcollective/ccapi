# imports - module imports
from cc.template import render_template

def test_render_template():
    render_template("test.html",
        context = dict(name = "Test"))  == "Hello, Test!"
    render_template("test.html",
        context = dict(name = "World")) == "Hello, World!"