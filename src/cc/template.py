# imports - standard imports
import os.path as osp
import cgi

# imports - module imports
from cc.util.system import read
from cc.config      import PATH
from cc.util.types  import sequencify
from cc.log         import get_logger
from cc.exception   import TemplateNotFoundError
from cc.util.string import _REGEX_HTML
from cc._compat     import iteritems

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

        >>> from cc.template import render_template
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
            item = cgi.escape(item)
            
            context[name] = item

        rendered = html.format(**context)
    
    return rendered