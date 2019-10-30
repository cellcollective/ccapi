# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import read
from cc.config      import PATH

def render_template(template, args = None):
    path = osp.join(PATH["TEMPLATES"], template)
    html = read(path)
    
    rendered = html

    if args:
        rendered = html.format(**args)
    
    return rendered