# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import read
from cc.constant    import TEMPLATES_DIRECTORY

def render_template(template, args = None):
    path = osp.join(TEMPLATES_DIRECTORY, template)
    html = read(path)
    
    rendered = html

    if args:
        rendered = html.format(*args)
    
    return rendered