# imports - standard imports
import collections

# imports - third-party imports
import requests

# imports - module imports
from ccapi.config       import DEFAULT
from ccapi.util.array   import (
    sequencify
)
from ccapi.log          import get_logger

logger = get_logger()

class Service:
    def __init__(self,
        base_url = None,
        proxies  = [ ],
        test     = True
    ):
        if not base_url:
            if not hasattr(self, "BASE_URL"):
                raise ValueError("Base URL not provided.")
            else:
                base_url = getattr(self, "BASE_URL")

        self.base_url    = base_url
        self._session    = requests.Session()

        if proxies and \
            not isinstance(proxies, (collections.Mapping, list, tuple)):
            raise TypeError((
                "proxies %s are not of valid type. You must "
                "either a dictionary of a list of dictionaries of the "
                "following format { protocol: ip }."))

        if isinstance(proxies, collections.Mapping):
            proxies = [proxies]

        self._proxies = proxies

        if test:
            self.ping()

    def _build_url(self, *args, **kwargs):
        prefix = kwargs.get("prefix", True)
        parts  = [ ]

        if prefix:
            parts.append(self.base_url)

        url = "/".join(map(str, sequencify(parts) + sequencify(args)))

        return url

    def request(self, method, url = "", *args, **kwargs):
        raise_error = kwargs.pop("raise_error", True)
        headers     = kwargs.pop("headers",     { })
        proxies     = kwargs.pop("proxies",     self._proxies)
        data        = kwargs.get("params",      kwargs.get("data"))
        prefix      = kwargs.get("prefix",      True)
        user_agent  = kwargs.get("user_agent",  DEFAULT["USER_AGENT"])

        headers.update({
            "User-Agent": user_agent
        })

        if proxies:
            proxies = random.choice(proxies)
            logger.info("Using proxy %s to dispatch request." % proxies)

        url = self._build_url(url, prefix = prefix)

        logger.info("Dispatching a %s request to URL: %s with Arguments - %s" \
            % (method, url, kwargs))
        response = self._session.request(method, url,
            headers = headers, proxies = proxies, *args, **kwargs)

        if not response.ok and raise_error:
            if response.text:
                logger.error("Error recieved from the server: %s" % response.text)

            response.raise_for_status()

        return response

    def ping(self, *args, **kwargs):
        self.request("HEAD", *args, **kwargs)