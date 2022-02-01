# imports - standard imports
import os.path as osp
import tempfile
import gzip

# imports - module imports
from bpyutils.util.imports import import_handler
from bpyutils.util.system  import read

def read_id(client, id_, **kwargs):
    BioModels   = import_handler("bioservices.biomodels.BioModels")
    biomodels   = BioModels()

    model       = None

    info        = biomodels.get_model_files(id_)

    filename    = info["main"][0]["name"]

    if ".xml" in filename:
        with tempfile.TemporaryDirectory() as dir_:
            output = osp.join(dir_, "model.xml")
            
            biomodels.get_model_download(id_, filename = filename,
                output_filename = output)

            gzipped = osp.join(dir_, "model.xml.gz")

            with gzip.open(gzipped, "wb") as f:
                content = read(output, mode = "rb")
                f.write(content)
            
            model = client.read(gzipped, **kwargs)
    else:
        raise ValueError("No SBML found for BioModel ID %s." % id_)

    return model