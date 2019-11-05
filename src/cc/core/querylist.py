# imports - module imports
from cc.core.mixins import JupyterHTMLViewMixin

class QueryList(list, JupyterHTMLViewMixin):
    def _repr_html_(self):
        repr_ = ""
        return repr_