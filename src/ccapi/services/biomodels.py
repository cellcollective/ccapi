# imports - standard imports
import os.path as osp
import tempfile

# imports - module imports
from ccapi.util.imports import import_handler

def read_id(client, id_, **kwargs):
    BioModels   = import_handler("bioservices.biomodels.BioModels")
    biomodels   = BioModels()

    model       = None

    info        = biomodels.get_model_files(id_)

    filename    = info["main"][0]["name"]

    if ".xml" in filename:
        with tempfile.TemporaryDirectory() as dir_:
            output = osp.join(dir_, "model.sbml")

            biomodels.get_model_download(id_, filename = filename,
                output_filename = output)
            
            model = client.read(output, **kwargs)
    else:
        raise ValueError("No SBML found for BioModel ID %s." % id_)

    return model