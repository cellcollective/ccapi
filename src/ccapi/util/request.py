# imports - module imports
from ccapi.util.string  import get_random_str
from ccapi.core.config  import Configuration
from ccapi.log          import get_logger

config = Configuration()
logger = get_logger()

def response_download(response, path = None, chunk_size = None):
    chunk_size  = chunk_size or config.max_chunk_download_bytes
    path        = path or get_random_str()

    with open(path, "wb") as f:
        for content in response.iter_content(chunk_size = chunk_size):
            if content:
                f.write(content)

    return path