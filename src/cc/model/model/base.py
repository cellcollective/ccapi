# imports - module imports
from cc.model.resource      import Resource
from cc.core.querylist      import QueryList
from cc.core.mixins         import JupyterHTMLViewMixin
from cc.model.model         import BooleanModel, InternalComponent
from cc.model.model.boolean import (
    ConditionType,
    ConditionState,
    ConditionRelation
)
from cc.config              import DEFAULT
from cc.constant            import MODEL_TYPE, MODEL_DOMAIN_TYPE
from cc.template            import render_template
from cc.util.string         import ellipsis, upper
from cc.util.types          import flatten
from cc.model.util          import get_temporary_id
from cc._compat             import itervalues, iteritems

_ACCEPTED_MODEL_TYPES           = tuple([t["value"] for t in itervalues(MODEL_TYPE)])
_ACCEPTED_MODEL_DOMAIN_TYPES    = tuple([t["value"] for t in itervalues(MODEL_DOMAIN_TYPE)])

_MODEL_TYPE_CLASS               = dict({ "boolean": BooleanModel })
_ACCEPTED_MODEL_CLASSES         = tuple(itervalues(_MODEL_TYPE_CLASS))

_API_CONDITION_TYPE             = dict({
    ConditionType.IF:       "IF_WHEN",
    ConditionType.UNLESS:   "UNLESS"
})
_API_CONDITION_STATE            = dict({
    ConditionState.ON:  "ON",
    ConditionState.OFF: "OFF"
})
_API_CONDITION_RELATION         = dict({
    ConditionRelation.INDEPENDENT: "OR",
    ConditionRelation.COOPERATIVE: "AND"
})

class Model(Resource, JupyterHTMLViewMixin):
    """
    The Base Model class.

    Usage::

        >>> from cc.model import Model
        >>> model = Model('Cortical Area Development')
    """
    def __init__(self, name = DEFAULT["MODEL_NAME"], default_type = DEFAULT["MODEL_TYPE"]["value"],
        domain = DEFAULT["MODEL_DOMAIN_TYPE"]["value"], *args, **kwargs):
        """
        A model instance.
        """
        if not default_type in _ACCEPTED_MODEL_TYPES:
            raise TypeError("Cannot find model type %s. Accepted types are %s."
                % (default_type, _ACCEPTED_MODEL_TYPES))
        
        self._default_type  = default_type

        if not domain in _ACCEPTED_MODEL_DOMAIN_TYPES:
            raise TypeError("Cannot find model domain type %s. Accepted \
                types are %s." % (domain, _ACCEPTED_MODEL_DOMAIN_TYPES))

        self._domain        = domain
        
        class_              = _MODEL_TYPE_CLASS[default_type]
        self._versions      = QueryList([class_(model = self, *args, **kwargs)])

        Resource.__init__(self, name = name, *args, **kwargs)

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
        elif not value in _ACCEPTED_MODEL_TYPES:
            raise TypeError("%s is not a valid model type. Accepted types are %s."
                % (value, _ACCEPTED_MODEL_TYPES)
            )
        else:
            self._default_type = value

    @property
    def domain(self):
        """
        The domain type of the model.
        """
        return getattr(self, "_domain", DEFAULT["MODEL_DOMAIN_TYPE"]["value"])

    @domain.setter
    def domain(self, value):
        if self.domain == value:
            pass
        elif not value in _ACCEPTED_MODEL_DOMAIN_TYPES:
            raise TypeError("Cannot find model domain type %s. Accepted \
                types are %s." % (domain, _ACCEPTED_MODEL_DOMAIN_TYPES))
        else:
            self._domain = value

    @property
    def versions(self):
        """
        List of model versions.
        """
        class_ = _MODEL_TYPE_CLASS[self.default_type]
        return getattr(self, "_versions",
            QueryList([class_(model = self)]))

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
        html = render_template("model.html", context = dict({
            "id":                   self.id,
            "name":                 self.name,
            "memory_address":       "0x0%x" % id(self),
            "number_of_versions":   len(self.versions),
            "versions":             self.versions
        }))
        return html

    def add_version(self, version):
        if not isinstance(version, _ACCEPTED_MODEL_CLASSES):
            raise TypeError("Model must be of type %s, found %s." % 
                (_ACCEPTED_MODEL_CLASSES, type(version))
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
                "name": self.name,
                "type": self.domain,
                "userId": me.id,
                "modelVersionMap": dict({
                    version.version: dict({
                        "name": version.name
                    })
                })
            })

            if isinstance(version, BooleanModel):
                species_map                 = dict()
                regulator_map               = dict()
                
                condition_map               = dict()
                condition_species_map       = dict()

                sub_condition_map           = dict()
                sub_condition_species_map   = dict()

                for component in version.components:
                    external = not isinstance(component, InternalComponent)
                    species_map[component.id] = dict({
                            "name": component.name,
                        "external": external,
                    })

                    for regulator in component.regulators:
                        regulator_map[regulator.id] = dict({
                                "regulationType": upper(regulator.type),
                            "regulatorSpeciesId": regulator.component.id,
                                     "speciesId": component.id,
                        })

                        for condition in regulator.conditions:
                            condition_map[condition.id] = dict({
                                    "regulatorId": regulator.id,
                                          "state": _API_CONDITION_STATE[condition.state],
                                           "type": _API_CONDITION_TYPE[condition.type],
                                "speciesRelation": _API_CONDITION_RELATION[condition.relation]
                            })

                            for component in condition.components:
                                id_ = get_temporary_id()
                                condition_species_map[id_] = dict({
                                    "conditionId": condition.id,
                                      "speciesId": component.id
                                })

                data[key]["speciesMap"]             = species_map
                data[key]["regulatorMap"]           = regulator_map

                data[key]["conditionMap"]           = condition_map
                data[key]["conditionSpeciesMap"]    = condition_species_map
                
                data[key]["subConditionMap"]        = sub_condition_map
                data[key]["subConditionSpeciesMap"] = sub_condition_species_map

        response = self._client.post("_api/model/save", json = data)
        content  = response.json()
        
        for key, data in iteritems(content):
            model_id, model_version_id = list(map(int, key.split("/")))
            
            if "id" in data:
                self.id = data["id"]

            for i, version in enumerate(self.versions):
                if model_version_id == version.version:
                    model_version_id            = int(data["currentVersion"])
                    self.versions[i].id         = self.id
                    self.versions[i].version    = model_version_id
                    
                    if "speciesIds" in data:
                        species_ids = data["speciesIds"]
                        for previous_species_id, species_id in iteritems(species_ids):
                            for j, component in enumerate(version.components):
                                if int(previous_species_id) == component.id:
                                    self.versions[i].components[j].id = species_id

                    if "regulatorIds" in data:
                        regulator_ids = data["regulatorIds"]
                    
                        for previous_regulator_id, regulator_id in iteritems(regulator_ids):
                            for j, component in enumerate(version.components):
                                for k, regulator in enumerate(component.regulators):
                                    if int(previous_regulator_id) == regulator.id:
                                        self.versions[i].components[j].regulators[k].id = regulator_id

                    if "conditionIds" in data:
                        condition_ids = data["conditionIds"]

                        for previous_condition_id, condition_id in iteritems(condition_ids):
                            for j, component in enumerate(version.components):
                                for k, regulator in enumerate(component.regulators):
                                    for l, condition in enumerate(regulator.conditions):
                                        if int(previous_condition_id) == condition.id:
                                            self.versions[i].components[j].regulators[k].conditions[l].id = condition_id

        return self

    def delete(self):
        data = dict(("%s/%s" % (self.id, model.version), None)
            for model in self.versions
        )
        self.client.post("_api/model/save", json = data)
        
        return self
