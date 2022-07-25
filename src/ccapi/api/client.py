# imports - standard imports
import sys
import os.path as osp
import random
import collections

import requests
# from   requests_cache.core      import CachedSession
# import grequests as greq
# from   grequests                import AsyncRequest

# imports - module imports
from bpyutils.util.environ      import getenv
from ccapi.api.helper           import (
    _build_model_urls,
    _user_response_to_user,
    _model_content_to_model,
    _model_version_response_to_boolean_model,
    _merge_metadata_to_model
)
from bpyutils.util.imports      import import_handler
from ccapi.model.model.base     import Model, _ACCEPTED_MODEL_DOMAIN_TYPES
from ccapi.model.user           import User
from ccapi.core.querylist       import QueryList
from ccapi.core.config          import Configuration
from ccapi.constant             import (
    PATH,
    AUTHENTICATION_HEADER,
    _AUTHENTICATION_ERROR_STRING
)
from ccapi._compat              import (
    string_types,
    iteritems,
    iterkeys,
    itervalues,
    urlencode
)
from bpyutils.util.array           import (
    sequencify,
    squash,
    find
)
from bpyutils.util._dict           import merge_dict
from ccapi.exception            import (
    TypeError,
    AuthenticationError
)
from bpyutils.log                  import get_logger

logger = get_logger()
config = Configuration()

from ccapi.model.model.metabolic import (
    ConstraintBasedModel,
    Metabolite,
    Reaction
)

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
        
        # if cache_timeout:
        #     self._session = CachedSession(
        #         cache_name   = osp.join(PATH["CACHE"], "requests"),
        #         expire_after = cache_timeout
        #     )
        # else:
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

    @property
    def version(self):
        """
        Version of the Build Service.

        Usage::

            >>> import ccapi
            >>> client = ccapi.Client()
            >>> client.version
            '2.6.2'
        """
        response = self.request("GET", "api/ping")

        if response.ok:
            content = response.json()
            version = content.get("version")

            return version
        else:
            response.raise_for_status()

    def _build_url(self, *args, **kwargs):
        params  = kwargs.pop("params", None) 
        prefix  = kwargs.get("prefix", True)
        parts   = [ ]

        if prefix:
            parts.append(self.base_url)

        url = "/".join(map(str, sequencify(parts) + sequencify(args)))

        if params:
            encoded  = urlencode(params)
            url     += "?%s" % encoded

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
            AsyncRequest = import_handler("grequests.AsyncRequest")
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

    def put(self, url, *args, **kwargs):
        """
        Dispatch a PUT request to the server.
        """
        response = self.request("PUT", url, *args, **kwargs)
        return response

    def ping(self, *args, **kwargs):
        """
        Check if the URL is alive.

        :param args: Arguments provided to ``client.request``
        :param kwargs: Keyword Arguments provided to ``client.request``

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
            email    = getenv("AUTH_EMAIL",    kwargs.get("email",    None))
            password = getenv("AUTH_PASSWORD", kwargs.get("password", None))

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
        user     = _user_response_to_user(content, client = self)

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
        domain    = filters.get("domain",   "research")
        category  = filters.get("category", "published")
        modelTypes = filters.get("modelTypes", ["boolean", "metabolic"])

        size      = kwargs.get("size",  config.max_api_resource_fetch)
        since     = kwargs.get("since", 1)
        since     = since if since > 0 else 1

        orderBy    = "recent"

        if id_:
            if isinstance(id_, string_types) and id_.isdigit():
                id_ = int(id_)
            id_ = sequencify(id_)

        if   _resource == "model":
            url         = self._build_url("api/model/cards/%s" % domain, prefix = False)
            params      = [
                ("modelTypes", "&".join(modelTypes)),
                ("orderBy",    orderBy),
                ("category",   category),
                ("cards",      size)
            ]

            if query:
                params  = params + (
                    ("search", "species"),
                    ("search", "knowledge"),
                    ("name",   query)
                )

            response    = self.request("GET", url, params = params)
            content     = response.json()

            if id_:
                urls    = dict()

                version = kwargs.get("version")
                hash_   = kwargs.get("hash")

                if isinstance(hash_, str):
                    if not len(id_) == 1:
                        raise ValueError((
                            "Hash provided cannot be a string. ",
                            "To provide multiple hashes, pass a dict of the ",
                            "format { id: hash }"
                        ))

                models  = dict()

                for i in id_:
                    model = find(content, lambda x: (x["model"]["id"] if "model" in x else x["id"]) == i)
                    
                    if not model:
                        raise ValueError("Model with ID %s not found." % i)
                    else:
                        models[i]   = dict({
                            "metadata": model,
                            "versions": dict()
                        })

                        versions    = [ ]

                        if not version:
                            versions = list(iterkeys(model["model"]["modelVersionMap"])) if "model" in model \
                                else [model["version"] for model in model["versions"]]

                        hash_def = None
                        if not hash_:
                            hash_def = model.get("hash", None)

                        urls.update(_build_model_urls(self,
                            id_ = i, version = version if version else versions,
                            hash_ = hash_ if hash_ else hash_def
                        ))

                arequests   = (self.request("GET", url, async_ = True) for url in itervalues(urls))
                greq        = import_handler("grequests")
                responses   = greq.imap(arequests)

                keys        = list(iterkeys(urls))

                for i, response in enumerate(responses):
                    _id, _version = list(map(int, keys[i].split("/")))

                    if response.ok:
                        json = response.json()
                        models[_id]["versions"].update({
                            _version: json
                        })
                    else:
                        logger.warn("Unable to fetch model %s with version %s." % (_id, _version))

                user_ids    = [ ]
                for id_, model in iteritems(models):
                    metadata    = model["metadata"]

                    if "model" in metadata:
                        user_id     = metadata["model"]["userId"]

                        user_ids.append(user_id)

                        for version_id, version_data in iteritems(model["versions"]):
                            version_data = next(iter(itervalues(version_data)))

                            for _, share_data in iteritems(version_data["shareMap"]):
                                user_id = share_data["userId"]
                                user_ids.append(user_id)

                        if metadata["uploadMap"]:
                            for upload_id, upload_data in iteritems(metadata["uploadMap"]):
                                user_id = upload_data["userId"]
                                user_ids.append(user_id)
                    else:
                        user_id = metadata["_createdBy"]
                        user_ids.append(user_id)

                user_ids    = set(user_ids)

                users       = QueryList(sequencify(self.get("user", id = user_ids)))

                resources   = QueryList([
                    _model_content_to_model(model,
                        users = users, client = self) \
                            for _, model in iteritems(models)
                ])
            else:
                if filters:
                    if "user" in filters:
                        user = filters["user"]

                        if isinstance(user, int):
                            user = self.get("user", id = user)

                        if not isinstance(user, User):
                            raise TypeError("Expected type for user is User \
                                or ID, type %s found." % type(user))

                        content = list(filter(lambda x: x["model"]["userId"] == user.id, content))

                    if "domain" in filters:
                        domain = filters["domain"]

                        if domain not in _ACCEPTED_MODEL_DOMAIN_TYPES:
                            raise TypeError("Not a valid domain type: %s" % domain)
                        else:
                            content = list(filter(lambda x: (x["model"]["type"] if "model" in x else x["domainType"]) == domain, content))

                from_, to   = since - 1, min(len(content), size)
                
                content     = content[from_ : from_ + to]
                ids         = [(data["model"]["id"] if "model" in data else data["id"]) for data in content]
                
                resources   = self.get("model", id = ids, size = size)
        elif _resource == "user":
            if not id_:
                raise ValueError("id required.")

            response    = self.request("GET", "_api/user/lookupUsers",
                params = [("id", i) for i in id_]
            )
            content     = response.json()

            resources   = QueryList([
                _user_response_to_user(
                    merge_dict({ "id": user_id }, user_data),
                    client = self
                ) for user_id, user_data in iteritems(content)
            ])

        return squash(resources)

    def read(self, filename, type = None, save = False):
        """
        Read a model file.

        :param filename: Name of the file locally present to read a model file.
        :param save: Save model after importing.
        """
        type_           = type or config.model_type["value"]
        
        model           = Model(client = self)
        # HACK: remove default version provided.
        model.versions.pop()

        if   type_ == "boolean":
            files           = dict({ "file": (filename, open(filename, "rb")) })

            response        = self.post("api/model/import", files = files)
            content         = response.json()

            boolean, meta   = _model_version_response_to_boolean_model(content,
                client = self)

            model           = _merge_metadata_to_model(model, meta)
            
            model.add_version(boolean)
        elif type_ == "metabolic":
            data            = dict(type = type_)
            files           = [("file", open(filename, "rb"))]

            response        = self.post("api/model/import", data = data,
                files = files)
            content         = response.json()

            data            = content["data"]

            model           = Model(client = self)

            # HACK: remove default version provided.
            model.versions.pop()

            for file_data in data:
                print(file_data)
                
                model_data  = file_data["data"]
                
                model.id    = model_data["id"]
                model.name  = model_data["name"]

                for version in model_data["versions"]:
                    if model_data["modelType"] == "metabolic":
                        metabolic = ConstraintBasedModel(
                            id = model.id, version = version["id"], client = self)

                        for metabolite in version["metabolites"]:
                            m = Metabolite(
                                id          = metabolite["id"],
                                name        = metabolite["name"],
                                compartment = metabolite["compartment"],
                                formula     = metabolite["formula"],
                                charge      = metabolite["charge"],
                                client      = self
                            )
                            metabolic.add_metabolite(m)

                        for reaction in version["reactions"]:
                            r = Reaction(
                                id          = reaction["id"],
                                name        = reaction["name"],
                                lower_bound = reaction["lowerBound"],
                                upper_bound = reaction["upperBound"],
                                client      = self
                            )
                            metabolic.add_reaction(r)

                        model.add_version(metabolic)
        else:
            raise TypeError("Unknown type %s." % type_)
        
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