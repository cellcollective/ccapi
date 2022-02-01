# imports - standard imports
import collections

# imports - compatibility imports
from ccapi._compat      import string_types, iterkeys, iteritems

# imports - third-party imports
import requests

# imports - module imports
from bpyutils.util.array   import (
    sequencify
)
from ccapi.core.config  import Configuration
from bpyutils.log          import get_logger

logger = get_logger()
config = Configuration()

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
        
        self._build_service()

    def _path_to_method(self, path):
        path = path.lstrip("/")
        path = path.rstrip("/")

        path = path.replace("/", "_")

        return path

    def _build_service_function(self, api, request_args = None):
        def fn(**kwargs):
            # reqargs = kwargs.get("request_args", { })
            args    = iterkeys(kwargs)
            
            # if "headers" in reqargs:
            #     headers = reqargs.get("headers", { })
            #     headers.update()

            if "parameters" in api:
                for param in api["parameters"]:
                    if isinstance(param, string_types):
                        param = dict({
                            "name": param
                        })

                    name        = param["name"]
                    required    = param.get("required", False)
                    type_       = param.get("type",     string_types)

                    if required and name not in args:
                        raise ValueError("Required parameter: %s" % name)
                
                    if arg == name:
                        if not isinstance(value, type_):
                            raise TypeError("%s is not of type %s, expected %s" % (arg, name, type_))

            response = self.request("GET", path, params = kwargs)

            return response
        
        return fn

    def _build_service(self):
        if hasattr(self, "API"):
            API = getattr(self, "API", None)

            if API:
                for api in API["paths"]:
                    path    = api["path"]
                    method  = self._path_to_method(path)

                    setattr(self, method, self._build_service_function(api))

            # if API:
            #     for api in API["paths"]:
            #         path    = api["path"]
                    
            #         method  = self._path_to_method(path)

            #         reqargs = dict({
            #             "headers": dict({
            #                 "content-type": API["content-type"]
            #             })
            #         })

            #         setattr(self, method, self._build_service_function(api,
            #             request_args = request_args))
                    
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
        prefix      = kwargs.pop("prefix",      True)
        user_agent  = kwargs.pop("user_agent",  config.user_agent)

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

    def post(self, url, *args, **kwargs):
        """
        Dispatch a POST request to the server.

        :param url: URL part (does not include the base URL).
        :param args: Arguments provided to ``client.request``
        :param kwargs: Keyword Arguments provided to ``client.request``

        Usage::

            >>> import ccapi
            >>> client   = ccapi.Client()
            >>> response = client.post("api/module/12345/report")
            >>> response.content
            b'"First Name","Last Name","Email","Institution","Last Updated Date"\n'
        """
        response = self.request("POST", url, *args, **kwargs)
        return response

    def ping(self, *args, **kwargs):
        self.request("HEAD", *args, **kwargs)