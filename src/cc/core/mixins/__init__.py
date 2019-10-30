# imports - standard imports
from abc import ABCMeta, abstractmethod

class JupyterHTMLViewMixin(metaclass = ABCMeta):
    @abstractmethod
    def _repr_html_(self):
        pass