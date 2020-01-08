# imports - standard imports
import sys
import os.path as osp
import random
import collections

# imports - third-party imports
# https://github.com/gevent/gevent/issues/1016#issuecomment-328529454
# Monkey-Patch
from gevent import monkey as curious_george
curious_george.patch_all(thread = False, select = False)

import requests
from   requests_cache.core      import CachedSession
import grequests as greq
from   grequests                import AsyncRequest

# imports - module imports
from ccapi.api.helper          import (
    _user_response_to_user,
    _model_response_to_model,
    _model_version_response_to_boolean_model,
    _merge_metadata_to_model
)
from ccapi.model.model.base    import Model, _ACCEPTED_MODEL_DOMAIN_TYPES
from ccapi.model.user          import User
from ccapi.core.querylist      import QueryList
from ccapi.core.config         import Configuration
from ccapi.config              import DEFAULT
from ccapi.constant            import (
    PATH,
    AUTHENTICATION_HEADER,
    _AUTHENTICATION_ERROR_STRING
)
from ccapi._compat             import (
    string_types,
    iteritems,
    iterkeys
)
from ccapi.util.array          import (
    sequencify,
    squash
)
from ccapi.util._dict          import merge_dict
from ccapi.exception           import (
    AuthenticationError
)
from ccapi.log                 import get_logger

logger = get_logger()
config = Configuration()

class Client:
    """
    The :class:`Client` class provides a convenient access to the Cell 
    Collective API. Instances of this class are a gateway to interacting 
    with Cell Collective's API through the ccapi.

    :param base_url: A base URL to use.
    :param proxies: A dictionary/list of proxies to use. If a list is passed,
        each element in the list should be a dictionary of the format 
        ``{ protocol: ip }``.
    :param test: Attempt to test the connection to the base url.

    Usage::

        >>> import ccapi
        >>> client = ccapi.Client()
        >>> client
        <Client url='https://cellcollective.org'>
    """
    def __init__(self,
        base_url        = None,
        proxies         = [ ],
        test            = True,
        cache_timeout   = None
    ):
        self.base_url    = base_url or config.url
        self._auth_token = None
        
        if cache_timeout:
            self._session = CachedSession(
                cache_name   = osp.join(PATH["CACHE"], "requests"),
                expire_after = cache_timeout
            )
        else:
            self._session = requests.Session()

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

    def __repr__(self):
        repr_ = "<Client url='%s'>" % (self.base_url)
        return repr_

    def __eq__(self, other):
        equals = False

        if isinstance(other, Client):
            if self.base_url == other.base_url:
                if not self.authenticated and not other.authenticated:
                    equals = True
                else:
                    if self.authenticated:
                        if other.authenticated:
                            if self._auth_token == other._auth_token:
                                equals = True

        return equals

    def _build_url(self, *args, **kwargs):
        prefix = kwargs.get("prefix", True)
        parts  = [ ]

        if prefix:
            parts.append(self.base_url)

        url = "/".join(map(str, sequencify(parts) + sequencify(args)))

        return url

    def request(self, method, url, *args, **kwargs):
        raise_error = kwargs.pop("raise_error", True)
        token       = kwargs.pop("token",       None)
        headers     = kwargs.pop("headers",     { })
        proxies     = kwargs.pop("proxies",     self._proxies)
        data        = kwargs.get("params",      kwargs.get("data"))
        prefix      = kwargs.get("prefix",      True)
        user_agent  = kwargs.get("user_agent",  config.user_agent)
        async_      = kwargs.pop("async_",      False)

        headers.update({
            "User-Agent": user_agent
        })

        if token:
            headers.update({
                AUTHENTICATION_HEADER: token
            })
        else:
            if self._auth_token:
                headers.update({
                    AUTHENTICATION_HEADER: self._auth_token
                })

        if proxies:
            proxies = random.choice(proxies)
            logger.info("Using proxy %s to dispatch request." % proxies)

        url = self._build_url(url, prefix = prefix)

        logger.info("Dispatching a %s request to URL: %s with Arguments - %s" \
            % (method, url, kwargs))

        if async_:
            response = AsyncRequest(method, url, session = self._session,
                headers = headers, proxies = proxies, *args, **kwargs)
        else:
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
        :param args: Arguments provided to ``client._request``
        :param kwargs: Keyword Arguments provided to ``client._request``

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
        """
        Check if the URL is alive.

        :param args: Arguments provided to ``client._request``
        :param kwargs: Keyword Arguments provided to ``client._request``

        Usage::

            >>> import ccapi
            >>> client = ccapi.Client()
            >>> client.ping()
            'pong'
        """
        response = self.request("GET", "api/ping", *args, **kwargs)
        try:
            content = response.json()
            if content.get("data") == "pong":
                return "pong"
            else:
                raise ValueError("Unable to ping to URL %s." % self.base_url)
        except JSONDecodeError:
            raise ResponseError("Unable to decode JSON.")

    def auth(self, *args, **kwargs):
        """
        Authenticate client.

        Usage::

            >>> import ccapi
            >>> client = ccapi.Client()
            >>> client.auth(
                    email    = "test@cellcollective.org",
                    password = "test"
                )
            >>> client.authenticated
            True

            >>> client.auth(token = "<YOUR_AUTH_TOKEN>")
            >>> client.authenticated
            True
        """
        token = kwargs.get("token", None)

        if not token:
            email    = kwargs.get("email",    None)
            password = kwargs.get("password", None)

            if not email:
                raise ValueError("email not provided.")

            if not password:
                raise ValueError("password not provided.")

            data       = dict(username = email, password = password)
            response   = self.post("_api/login", data = data)
            auth_token = response.headers.get(AUTHENTICATION_HEADER)

            if auth_token:
                self._auth_token = auth_token
            else:
                raise AuthenticationError(_AUTHENTICATION_ERROR_STRING)
        else:
            try:
                self.me(token = token)
                self._auth_token = token
            except HTTPError:
                raise AuthenticationError(_AUTHENTICATION_ERROR_STRING)

    def logout(self):
        """
        Logout client.
        """
        self._auth_token = None

    @property
    def authenticated(self):
        _authenticated = bool(self._auth_token)
        return _authenticated

    def raise_for_authentication(self):
        """
        Raise AuthenticationError in case the client hasn't been authenticated.
        """
        
        if not self.authenticated:
            raise AuthenticationError("Client is not authenticated.")

    def me(self, *args, **kwargs):
        """
        Get the user profile of the authenticated client.

        Usage::

            >>> import ccapi
            >>> client = ccapi.Client()
            >>> client.auth(email = "test@cellcollective.org", password = "test")
            >>> client.me()
            <User id=10887 name='Test Test'>
        """
        
        response = self.request("GET", "_api/user/getProfile", *args, **kwargs)
        content  = response.json()
        user     = _user_response_to_user(self, content)

        return user

    def get(self, resource, *args, **kwargs):
        """
        Get resources.

        :param resource: Resource name.
        """
        _resource = resource.lower()
        resources = [ ]

        id_       = kwargs.get("id")
        query     = kwargs.get("query")
        raw       = kwargs.get("raw", False)

        filters   = kwargs.get("filters", { })

        size      = kwargs.get("size",  config.max_api_resource_fetch)
        since     = kwargs.get("since", 1)
        since     = since if since > 0 else 1

        if id_:
            if isinstance(id_, string_types) and id_.isdigit():
                id_ = int(id_)
            id_ = sequencify(id_)

        if   _resource == "model":
            url     = self._build_url("_api","model","get", prefix = False)
            params  = None

            version = kwargs.get("version")
            hash_   = kwargs.get("hash")

            if id_:
                url = self._build_url(url, str(id_[0]), prefix = False)

                if version:
                    params = dict({
                        "version": str(version) + \
                            ("&%s" % hash_ if hash_ else "")
                    })

            if query:
                url     = self._build_url(url, prefix = False)
                params  = [
                    ("search", "species"),
                    ("search", "knowledge"),
                    ("name",   query)
                ]

            response = self.request("GET", url, params = params)
            content  = response.json()

            if id_:
                id_       = squash(id_)

                models    = self.get("model", size = sys.maxsize, raw = True)
                
                model     = squash([model for model in models \
                    if model["model"]["id"] == id_])

                if not model:
                    raise ValueError("Model with ID %s not found." % id_)
                else:
                    resources = content if raw else \
                        _model_response_to_model(self, model)
            else:
                if filters:
                    if "user" in filters:
                        user = filters["user"]

                        if isinstance(user, int):
                            user = self.get("user", id = user)

                        if not isinstance(user, User):
                            raise TypeError("Expected type for user is User or ID, type %s found." % type(user))

                        content = list(filter(lambda x: x["model"]["userId"] == user.id, content))

                    if "domain" in filters:
                        domain = filters["domain"]

                        if domain not in _ACCEPTED_MODEL_DOMAIN_TYPES:
                            raise TypeError("Not a valid domain type: %s" % domain)
                        else:
                            content = list(filter(lambda x: x["model"]["type"] == domain, content))

                from_, to = since - 1, min(len(content), size)
                content   = content[from_ : from_ + to]

                resources = content if raw else \
                    QueryList([
                        _model_response_to_model(self, obj)
                            for obj in content
                    ])
        elif _resource == "user":
            if not id_:
                raise ValueError("id required.")

            response    = self.request("GET", "_api/user/lookupUsers",
                params = [("id", i) for i in id_]
            )
            content     = response.json()

            for user_id, user_data in iteritems(content):
                user = _user_response_to_user(self, 
                    merge_dict({ "id": user_id }, user_data)
                )
                resources.append(user)

        return squash(resources)

    def read(self, filename, type = None, save = False):
        """
        Read an SBML file.

        :param filename: Name of the file locally present to read an SBML file.
        :param save: Save model after importing.
        """
        type_           = type or config.model_type["value"]

        files           = dict({ "upload": (filename, open(filename, "rb")) })

        response        = self.post("_api/model/import", files = files)
        content         = response.json()

        model           = Model(client = self)

        boolean, meta   = _model_version_response_to_boolean_model(self, content)
        
        model           = _merge_metadata_to_model(model, meta)

        # HACK: remove default version provided.
        model.versions.pop()

        model.add_version(boolean)
        
        if save:
            model.save()

        return model

    def search(self, resource, query, *args, **kwargs):
        """
        Search a resource.

        :param resource: Name of the resource.
        :param query: Search a query string.
        """
        return self.get(resource, query = query, *args, **kwargs)