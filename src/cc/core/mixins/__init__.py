# imports - standard imports
from abc import ABCMeta

class JupyterViewMixin(ABCMeta):
    def _repr_html(self):
        pass