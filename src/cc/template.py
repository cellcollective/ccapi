# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import read
from cc.config      import PATH

def render_template(template, *args, **kwargs):
    """
    Renders a template. The template must be of the string format. For more 
    details, see 
    https://docs.python.org/3.4/library/string.html#string-formatting.

    :param template: Path to template file.
    :param context: The context passed to the template.
    :param dirs: Path/List of Directory Paths to search for templates.

    :return: Returns the rendered template.
    :rtype: str

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