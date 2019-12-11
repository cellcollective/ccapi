# imports - standard imports
import os.path as osp

# imports - compatibility imports
from ccapi._compat      import urljoin

# imports - third-party imports
import requests
import grequests

# imports - module imports
from ccapi.config       import DEFAULT
from ccapi.constant     import PATH, URL
from ccapi.util         import iz
from ccapi.util.system  import makedirs
from ccapi.log          import get_logger

logger = get_logger()

def get_ginsim_executable(version = None):
    version     = version or DEFAULT["GINSIM_VERSION"]
    dirs        = osp.join(PATH["CACHE"], "ginsim", version)
    executable  = osp.join(dirs, "ginsim.jar")

    if not osp.exists(executable):
        makedirs(dirs, exist_ok = True)
        
        url = "/".join([URL["GINSIM_FILES"], "GINsim-%s.jar" % version])

        logger.info("Dispatching request to %s..." % url)
        with requests.get(url, stream = True) as response:
            response.raise_for_status()
            
            with open(executable, "wb") as f:
                for chunk in response.iter_content(
                    chunk_size = DEFAULT["MAX_CHUNK_DOWNLOAD_BYTES"]
                ):
                    if chunk:
                        f.write(chunk)
    
    return executable

class GINsim:
    def __init__(self, version = None, executable = None):
        self._executable = get_ginsim_executable(version = version)

    def read(self, *paths):
        paths   = [dict({ "path": path, "local": iz.url(path) }) \
            for path in paths]
        urls    = [path["path"] for path in paths if not path["local"]]
        
        java    = which("java", raise_err = True)