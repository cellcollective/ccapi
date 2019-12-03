# imports - module imports
from ccapi.services import Service

class BioModels(Service):
    BASE_URL = "https://www.ebi.ac.uk/biomodels"
    VERSION  = "beta2"

    def __init__(self, *args, **kwargs):
        Service.__init__(self, *args, **kwargs)