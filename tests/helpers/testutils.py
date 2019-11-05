# imports - standard imports
import requests

# imports - third-party imports
from cc.util.string import safe_decode, strip

_URL_PROXY_LIST = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"

def get_random_proxies():
    lines = [ ]

    response = requests.get(_URL_PROXY_LIST)
    if response.ok:
        content = strip(safe_decode(response.content))
        lines   = content.split("\n")
        lines   = [{ "http": line } for line in lines]
    else:
        response.raise_for_status()

    return lines