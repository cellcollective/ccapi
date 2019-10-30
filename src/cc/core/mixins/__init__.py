# imports - standard imports
from abc import ABCMeta, abstractmethod

class JupyterViewMixin(metaclass = ABCMeta):
    @abstractmethod
    def _repr_html(self):
        pass