# imports - standard imports
from os.path import join

# imports - module imports
from ccapi.model.model.version  import ModelVersion
from ccapi.core.querylist       import QueryList
from ccapi.core.mixins          import JupyterHTMLViewMixin
from ccapi.template             import render_template
from bpyutils.util.string          import ellipsis
from bpyutils.util.system          import makepath
from bpyutils.util.request         import download_file
from ccapi.constant             import CONSTRAINT_BASED_MODEL_EXPORT_TYPE
from ccapi.core.config          import Configuration

# imports - constraint-based model imports
from ccapi.model.model.metabolic.metabolite  import Metabolite
from ccapi.model.model.metabolic.gene        import Gene
from ccapi.model.model.metabolic.reaction    import Reaction

config = Configuration()

class ConstraintBasedModel(ModelVersion, JupyterHTMLViewMixin):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "number_of_metabolites",
            "title": "Number of Metabolites",
              "key": lambda x: len(x.metabolites) 
        })
    ]

    def __init__(self, *args, **kwargs):
        self.super          = super(ConstraintBasedModel, self)
        self.super.__init__(*args, **kwargs)

        self._metabolites   = QueryList()
        self._reactions     = QueryList()

    def _repr_html_(self):
        repr_ = render_template(join("metabolic", "model.html"), context = dict({
            "id":                   self.id,
            "version":              self.version,
            "name":                 self.name,
            "memory_address":       "0x0%x" % id(self),
            "number_of_metabolites": len(self.metabolites),
            "metabolites":           ellipsis(", ".join([s.name for s in self.metabolites]), threshold = 500),
            "number_of_reactions":   len(self.reactions),
            "reactions":             ellipsis(", ".join([s.name for s in self.reactions]),   threshold = 500)
        }))
        return repr_

    @property
    def metabolites(self):
        metabolites = getattr(self, "_metabolites", QueryList())
        return metabolites

    @metabolites.setter
    def metabolites(self, value):
        if self.metabolites == value:
            pass
        elif not isinstance(value, (list, tuple, QueryList)):
            raise TypeError("ID must be an integer.")
        else:
            self._metabolites = value
        
        if not isinstance(value, QueryList):
            raise TypeError("Components must be of type (list, tuple, QueryList).")
        else:
            for metabolite in value:
                if not isinstance(metabolite, Metabolite):
                    raise TypeError("Element must be of type Metabolite.")

            self._metabolites = value

    def add_metabolite(self, metabolite):
        if not isinstance(metabolite, Metabolite):
            raise TypeError("Metabolite must be of type %s, found %s." % 
                (Metabolite, type(metabolite))
            )
        else:
            if metabolite in self.metabolites:
                raise ValueError("Metabolite already exists.")
            else:
                self.metabolites.append(metabolite)

    def add_metabolites(self, *metabolites):
        for metabolite in metabolites:
            if not isinstance(metabolite, Metabolite):
                raise TypeError("Metabolite must be of type %s, found %s." % 
                    (Metabolite, type(Metabolite))
                )

        for metabolite in metabolites:
            self.add_metabolite(metabolite)

    @property
    def reactions(self):
        reactions = getattr(self, "_reactions", QueryList())
        return reactions

    @reactions.setter
    def reactions(self, value):
        if self.reactions == value:
            pass
        elif not isinstance(value, (list, tuple, QueryList)):
            raise TypeError("ID must be an integer.")
        else:
            self._reactions = value
        
        if not isinstance(value, QueryList):
            raise TypeError("Components must be of type (list, tuple, QueryList).")
        else:
            for reaction in value:
                if not isinstance(reaction, Reaction):
                    raise TypeError("Element must be of type Reaction.")

            self._reactions = value

    def add_reaction(self, reaction):
        if not isinstance(reaction, Reaction):
            raise TypeError("Reaction must be of type %s, found %s." % 
                (Reaction, type(reaction))
            )
        else:
            if reaction in self.reactions:
                raise ValueError("Reaction already exists.")
            else:
                self.reactions.append(reaction)

    def add_reactions(self, *reactions):
        for reaction in reactions:
            if not isinstance(reaction, Reaction):
                raise TypeError("Reaction must be of type %s, found %s." % 
                    (Reaction, type(Reaction))
                )

        for reaction in reactions:
            self.add_reaction(reaction)

    def write(self, path = None, type = "sbml", **kwargs):
        type_           = CONSTRAINT_BASED_MODEL_EXPORT_TYPE[type]["value"]
        params          = { "version": self.version, "type": type_ }

        response        = self.client.request("GET", "api/model/%s/export" % self.id,
            params = params)

        if not path:
            header  = response.headers["content-disposition"]
            name    = re.findall("filename=(.+)", header)[0]
            path    = abspath(name)

        nchunk      = kwargs.get("nchunk", config.max_chunk_download_bytes)

        makepath(path)

        path        = download_file(response, path, chunk_size = nchunk)

        return path

    def to_json(self):
        data                = self.super.to_json()

        data["id"]          = str(self.version)

        data["metabolites"] = [ ]
        for metabolite in self.metabolites:
            json = metabolite.to_json()
            data["metabolites"].append(json)

        data["reactions"]   = [ ]
        for reaction in self.reactions:
            json = reaction.to_json()
            data["reactions"].append(json)

        data["genes"]       = [ ]
        

        return data

    def analyse(self, type_ = "fba"):
        model               = self.to_json()
        data                = dict(type = "metabolic", model = model,
            analysis = type_)

        response            = self.client.post("api/model/analyse", json = data)
        content             = response.json()

        return content