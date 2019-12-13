# imports - module imports
from ccapi.services.base import Service

class BioModels(Service):
    BASE_URL = "https://www.ebi.ac.uk/biomodels"
    VERSION  = "beta2"

    API      = dict({
        "paths": [
            # dict({
            #           "path": "/<modelId>",
            #     "parameters": [
            #         dict({
            #                "name": "format",
            #                "type": str,
            #             "default": True
            #         })
            #     ]
            # }),
            dict({
                      "path": "/search",
                "parameters": [
                    dict({
                        "name": "query",
                        "required": True
                    }),
                    dict({
                        "name": "offset",
                        "type": int
                    }),
                    dict({
                        "name": "numResults",
                        "type": int
                    }),
                    "sort",
                    "format"
                ]
            }),
            dict({
                      "path": "/search/download",
                "parameters": [
                    dict({
                        "name": "models",
                        "required": True
                    })
                ]
            })
        ]
    })

    def __init__(self, *args, **kwargs):
        Service.__init__(self, *args, **kwargs)