# imports - module imports
from cc.model.resource      import Resource
from cc.core.querylist      import QueryList
from cc.core.mixins         import JupyterHTMLViewMixin
from cc.model.model         import BooleanModel, InternalComponent
from cc.config              import DEFAULT
from cc.constant            import MODEL_TYPE
from cc.template            import render_template
from cc.util.string         import ellipsis
from cc._compat             import itervalues

_MODEL_TYPE_CLASS       = dict({
    "boolean": BooleanModel
})
_ACCEPTED_MODEL_TYPES   = tuple([t["value"] for t in itervalues(MODEL_TYPE)])
_ACCEPTED_MODEL_CLASSES = tuple(itervalues(_MODEL_TYPE_CLASS))

class Model(Resource, JupyterHTMLViewMixin):
    """
    The Base Model class.

    Usage::

        >>> from cc.model import Model
        >>> model = Model('Cortical Area Development')
        >>> model.save()
    """
    
    def __init__(self, name = DEFAULT["MODEL_NAME"], id = None, autosave = False,
        client = None, default_type = DEFAULT["MODEL_TYPE"]["value"]
    ):
        """
        A model instance.
        """
        if not default_type in _ACCEPTED_MODEL_TYPES:
            raise ValueError("Cannot find model type %s. Accepted types are %s."
                % (default_type, _ACCEPTED_MODEL_TYPES))

        Resource.__init__(self, id = id, name = name, autosave = autosave,
            client = client)

        self._domain_type   = DEFAULT["MODEL_DOMAIN_TYPE"]["value"]
        
        self._default_type  = default_type
        class_              = _MODEL_TYPE_CLASS[default_type]
        self._versions      = QueryList([class_(base_model = self)])

    @property
    def default_type(self):
        """
        The default model type.
        """
        return getattr(self, "_default_type", DEFAULT["MODEL_TYPE"]["value"])

    @default_type.setter
    def default_type(self, value):
        if self.default_type == value:
            pass
        elif not default_type in _ACCEPTED_MODEL_TYPES:
            raise TypeError("%s is not a valid model type. Accepted types are %s."
                % (default_type, _ACCEPTED_MODEL_TYPES)
            )
        else:
            self._default_type = value

    @property
    def versions(self):
        """
        List of model versions.
        """
        class_ = _MODEL_TYPE_CLASS[self.default_type]
        return getattr(self, "_versions", QueryList([class_(base_model = self)]))

    @versions.setter
    def versions(self, value):
        versions = value

        if self.versions == versions:
            pass
        elif isinstance(versions, (list, tuple)):
            versions = QueryList(versions)
        
        if not isinstance(versions, QueryList):
            raise TypeError("Versions must be of type (list, tuple, QueryList).")
        else:
            self._versions = versions

    def _repr_html_(self):
        # TODO: Check model details.
        html = render_template("model.html")
        return html

    def add_version(self, version):
        if not isinstance(version, _ACCEPTED_MODEL_CLASSES):
            raise TypeError("Model must be of type %s, found %s." % 
                (_ACCEPTED_MODEL_CLASS, type(version))
            )
        else:
            self.versions.append(version)

    def add_versions(self, *versions):
        for version in versions:
            if not isinstance(version, _ACCEPTED_MODEL_CLASSES):
                raise TypeError("Model must be of type %s, found %s." %
                    (_ACCEPTED_MODEL_CLASS, type(version))
                )
                
        for version in versions:
            self.versions.append(version)

    def save(self):
        self._before_save()

        me   = self.client.me()
        data = dict()

        for version in self.versions:
            key       = "%s/%s" % (self.id, version.version)
            data[key] = dict({
                "name":     self.name,
                "type":     self._domain_type,
                "userId":   me.id,
                "modelVersionMap": dict({
                    version.version: dict({
                        "name": version.name
                    })
                })
            })

            if isinstance(version, BooleanModel):
                species_map  = dict()
                for component in version.components:
                    external = not isinstance(component, InternalComponent)
                    species_map[component.id] = dict({
                            "name": component.name, 
                        "external": external,
                    })

                data[key]["speciesMap"] = species_map

        response = self._client.post("_api/model/save", json = data)

        return self

    def delete(self):
        data = dict(("%s/%s" % (self.id, model.version), None)
            for model in self.versions
        )
        self._client.post("_api/model/save", json = data)
        
        return self