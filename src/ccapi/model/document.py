# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.model.resource import Resource

class Document(Resource):
    def __init__(self, *args, **kwargs):
        self.name       = kwargs.get("name")
        self.created    = kwargs.get("created")
        self.user       = kwargs.get("user")
        self._token     = kwargs.get("token")
        self._client    = kwargs.get("client")

    def download(self, location = ".", name = None, **kwargs):
        nchunk   = kwargs.get("nchunk", 1024)

        url      = self._client._build_url("_api", "model", "download")
        response = self._client._request("GET", url, params = { "token": self._token })

        if not name:
            name = self.name

        path = osp.abspath(osp.join(location, name))

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size = nchunk):
                if chunk:
                    f.write(chunk)