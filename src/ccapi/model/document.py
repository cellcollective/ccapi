# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.model.resource   import Resource
from ccapi.core.config      import Configuration
from bpyutils.util.request     import download_file
from bpyutils.log              import get_logger

config = Configuration()
logger = get_logger()

class Document(Resource):
    _REPR_ATTRIBUTES = [
        dict({
             "name": "user",
            "title": "User"
        })
    ]

    def __init__(self, *args, **kwargs):
        Resource.__init__(self, *args, **kwargs)

    def download(self, location = ".", name = None, **kwargs):
        nchunk   = kwargs.get("nchunk", config.max_chunk_download_bytes)

        url      = self.client._build_url("_api","model","download")
        response = self.client.request("GET", url, params = { "token": self._token })

        if not name:
            name = self.name

        path = osp.abspath(osp.join(location, name))

        path = download_file(response, path, chunk_size = nchunk)

        return path