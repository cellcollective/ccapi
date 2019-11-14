# imports - module imports
from cc.core.mixins import JupyterHTMLViewMixin

class QueryList(list, JupyterHTMLViewMixin):
    # def __init__(self, *args):
    #     if len(args) > 2:
    #         raise TypeError("QueryList takes atmost one argument \
    #             (%s given)." % len(args))

    #     self.super = super(QueryList, self)
    #     self.super.__init__(self)

    #     self._indices   = { }

    # def get_by_id(self):
    #     pass

    # def extend(self, iterable):
    #     """
    #     Extend the QueryList.
    #     """

    #     if not hasattr(self, "_indices"):
    #         self._indices = { }

    #     list.extend(self, iterable)

    #     for i, obj in enumerate(iterable):
    #         id_ = obj.id
    #         if id_ not in self._indices:
    #             self._indices[id_] = i

    def _repr_html_(self):
        repr_ = ""
        return repr_