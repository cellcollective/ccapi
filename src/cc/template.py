# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import read
from cc.config import PATH

def render_template(template, context = None):
    """
    Renders a template.

    :param context: Contextual arguments to be passed to the template.

    Usage::

        >>> from cc.template import render_template
        >>> render_template("test.html", context = dict(name = "Test"))
        'Hello, Test!'

    """
    path = osp.join(PATH["TEMPLATES"], template)
    html = read(path)
    
    rendered = html

    if context:
        rendered = html.format(**context)
    
    return rendered