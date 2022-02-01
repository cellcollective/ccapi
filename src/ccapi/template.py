# imports - compat imports
from ccapi._compat import PY2

# imports - standard imports
import os.path as osp

if PY2:
    import cgi as module_escape
else:
    import html as module_escape

# imports - module imports
from bpyutils.util.system import read
from bpyutils.util.array  import sequencify
from bpyutils.log         import get_logger
from ccapi.exception   import TemplateNotFoundError
from bpyutils.util.string import _REGEX_HTML
from ccapi._compat     import iteritems
from ccapi.constant    import PATH

logger = get_logger()

def render_template(template, dirs = [ ], context = None, **kwargs):
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

        >>> from ccapi.template import render_template
        >>> render_template("test.html", context = dict(name = "Test"))
        'Hello, Test!'
        >>> render_template("test.html", name = "Test")
        'Hello, Test!'
        >>> render_template("foobar.html", dirs = "templates", bar = "baz")
        'foobaz'
    """
    dirs = sequencify(dirs)
    if PATH["TEMPLATES"] not in dirs:
        dirs.append(PATH["TEMPLATES"])

    dirs = [osp.abspath(dir_) for dir_ in dirs]

    logger.info("Searching for templates within directories: %s" % dirs)

    path = None
    for dir_ in dirs:
        temp = osp.join(dir_, template)
        if osp.exists(temp):
            path = temp
            break
    
    if not path:
        raise TemplateNotFoundError("Template %s not found." % template)
    
    html     = read(path)
    rendered = html

    if not context:
        context  = kwargs

    if context:
        for name, item in iteritems(context):
            item = str(item)
            item = module_escape.escape(item)
            
            context[name] = item

        rendered = html.format(**context)
    
    return rendered