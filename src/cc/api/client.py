# imports - standard imports
import datetime as dt
import collections
import re
import random

# imports - third-party imports
import requests

# imports - module imports
from cc.util.types  import (
    sequencify,
    squash,
    merge_dict
)
from cc.util.string import (
    sanitize_html,
    sanitize_text,
    lower
)
from cc.exception   import (
    ValueError,
    AuthenticationError,
    HTTPError
)
from cc.constant    import (
    DEFAULT_URL,
    HEADER_AUTHENTICATION,
    USER_AGENT,
    MAXIMUM_API_RESOURCE_FETCH,
    _AUTHENTICATION_ERROR_STRING
)
from cc.model       import (
    User,
    Model,
    BooleanModel, Species, Regulator, Condition, SubCondition,
    Document
)
from cc.core.querylist  import QueryList
from cc.log             import get_logger

logger = get_logger()

def _cc_datetime_to_python_datetime(datetime_):
    datetime_object = dt.datetime.strptime(
        datetime_,
        "%a, %d %b %Y %H:%M:%S %Z"
    )
    return datetime_object

def _section_type_to_dict_key(section_type):
    splits  = re.findall("[A-Z][^A-Z]*", section_type)
    key     = "_".join([s.lower() for s in splits])

    return key

def _model_get_by_id_response_object_to_model_object(client, response):
    _, data             = next(iter(response.items()))

    model               = BooleanModel()

    if "score" in data:
        model.score = data["score"]["score"]

    species_map = dict()
    for species_id, species_data in data["speciesMap"].items():
        species = Species(
            id_     = int(species_id),
            name    = species_data["name"],
            type    = "external" if species_data["external"] else "internal",
            created = _cc_datetime_to_python_datetime(
                species_data["creationDate"]
            ) if species_data.get("creationDate") else None,
            updated = _cc_datetime_to_python_datetime(
                species_data["updateDate"]
            ) if species_data.get("updateDate")   else None,
        )

        # knowledge base
        page_id_found = None
        for page_id, page_data in data["pageMap"].items():
            if page_data["speciesId"] == species.id:
                page_id_found = int(page_id)

        sections = dict()
        if page_id_found:
            for section_id, section_data in data["sectionMap"].items():
                if section_data["pageId"] == page_id_found:
                    section_type = section_data.get("type")
                    if section_type:
                        for _, content_data in data["contentMap"].items():
                            if content_data["sectionId"] == int(section_id):
                                text = sanitize_html(content_data["text"])
                                text = sanitize_text(text)
                                key  = _section_type_to_dict_key(section_type)
                                
                                if not key in sections:
                                    sections[key] = [ ]
                                
                                sections[key].append({
                                    "position": content_data["position"],
                                    "text":     text
                                })

            sections_formatted = dict()
            for key, section in sections.items():
                sections_formatted[key] = "\n".join([i["text"]
                    for i in sorted(section, key = lambda s: s["position"])])
            sections = sections_formatted
                
        species.information     = sections

        species_map[species.id] = species

        model.species.append(species)

    sub_condition_map   = dict()
    for sub_condition_id, sub_condition_data in data["subConditionMap"].items():
        species         = [ ]
        for _, sub_condition_species_data in data["subConditionSpeciesMap"].items():
            if sub_condition_species_data["subConditionId"] == int(sub_condition_id):
                species_id = sub_condition_species_data["speciesId"]
                species.append(species_map[species_id])

        sub_condition   = SubCondition(
            id          = int(sub_condition_id),
            type        = lower(sub_condition_data["type"]),
            operator    = lower(sub_condition_data["speciesRelation"])
                if sub_condition_data.get("speciesRelation") else None,
            state       = lower(sub_condition_data["state"]),
            species     = species
        )

        sub_condition_map[sub_condition.id] = dict({
            "condition_id":     sub_condition_data["conditionId"],
            "sub_condition":    sub_condition
        })

    condition_map   = dict()
    for condition_id, condition_data in data["conditionMap"].items():
        species     = [ ]
        for _, condition_species_data in data["conditionSpeciesMap"].items():
            if condition_species_data["conditionId"] == int(condition_id):
                species_id = condition_species_data["speciesId"]
                species.append(species_map[species_id])

        condition   = Condition(
            id                      = int(condition_id),
            sub_conditions          = [data["sub_condition"]
                for _, data in sub_condition_map.items()
                    if data["condition_id"] == int(condition_id)
            ],
            type                    = lower(condition_data["type"]),
            operator                = lower(condition_data["speciesRelation"])
                if condition_data.get("speciesRelation") else None,
            sub_condition_operator  = lower(condition_data["subConditionRelation"])
                if condition_data.get("subConditionRelation") else None,
            state                   = lower(condition_data["state"]),
            species                 = species
        )

        condition_map[condition.id] = dict({
            "regulator_id": condition_data["regulatorId"],
            "condition":    condition
        })

    regulator_map       = dict()
    for regulator_id, regulator_data in data["regulatorMap"].items():
        regulator           = Regulator(
            id              = int(regulator_id),
            type            = regulator_data["regulationType"].lower(),
            species         = species_map[regulator_data["regulatorSpeciesId"]],
            of              = species_map[regulator_data["speciesId"]],
            conditions      = [data["condition"]
                for _, data in condition_map.items()
                    if data["regulator_id"] == int(regulator_id)
            ]
        )

        regulator_map[regulator.id] = regulator

    for i, species in enumerate(model.species):
        for regulator_id, regulator in regulator_map.items():
            if regulator.of == species:
                model.species[i].regulators.append(regulator)

    model.permissions   = data.get("permissions")

    model.users         = [ ]
    for _, share_data in data["shareMap"].items():
        user = client.get("user", id_ = share_data["userId"])
        model.users.append(user)

    model._client       = client

    return model

def _model_get_response_object_to_model_object(client, response):
    data                = response["model"]

    model               = Model()

    model.id            = data["id"]
    model.name          = data["name"]
    model.description   = data["description"]
    model.author        = data["author"]
    model.tags          = data["tags"] and data["tags"].split(", ")

    model.domain        = data["type"]
    model.ncitations    = data["cited"]
    
    model.created       = _cc_datetime_to_python_datetime(
        data["creationDate"]
    ) if data["creationDate"] else None

    model.updated       = dict(
        biologic        = 
            _cc_datetime_to_python_datetime(
                data["biologicUpdateDate"]
            ) if data["biologicUpdateDate"] else None,
        knowledge       =
            _cc_datetime_to_python_datetime(
                data["knowledgeBaseUpdateDate"]
            ) if data["knowledgeBaseUpdateDate"] else None,
    )

    model.user          = client.get("user", id_ = data["userId"])
    model.public        = data["published"]

    model.hash          = data.get("hash")

    model.permissions   = response["modelPermissions"]
    
    for version in data["modelVersionMap"].keys():
        model_version = client.get("model",
            id_     = model.id,
            version = version,
            hash_   = model.hash,
        )

        model_version.id            = model.id
        model_version.version       = version
        model_version.name          = model.name

        model.versions.append(model_version)

    if response["uploadMap"]:
        for _, upload_data in response["uploadMap"].items():
            document        = Document(
                name        = upload_data["uploadName"],
                user        = client.get("user", id_ = upload_data["userId"]),
                created     = _cc_datetime_to_python_datetime(
                    upload_data["uploadDate"]
                ),
                token       = upload_data["token"],
                client      = client
            )
            model.documents.append(document)

    model._client       = client

    return model

def _user_get_profile_response_object_to_user_object(response):
    user             = User()

    user.id          = response["id"]
    user.email       = response.get("email")
    user.first_name  = response["firstName"]
    user.last_name   = response["lastName"]
    user.institution = response.get("institution")

    return user

class Client:
    """
    The :class:`Client` class provides a convenient access to the 
    Cell Collective API. Instances of this class are a gateway to interacting 
    with Cell Collective's API through the CCPy.

    :param base_url: Base URL to use.
    :param proxies: A dictionary/list of proxies to use. If a list is passed,
        each element in the list should be a dictionary of the format 
        ``{ protocol: ip }``.
    :param test: Attempt to test the connection to the base url.

    Usage::

        >>> import cc
        >>> client = cc.Client()
        >>> client
        <Client url='https://cellcollective.org'>
    """

    def __init__(self,
        base_url = DEFAULT_URL, proxies = [ ], test = True):
        self.base_url    = base_url
        self._auth_token = None
        self._session    = requests.Session()

        if proxies and (
                not isinstance(proxies, collections.Mapping) or \
                not isinstance(proxies, (list, tuple))
            ):
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

    def _build_url(self, *args, **kwargs):
        prefix = kwargs.get("prefix", True)
        parts  = [ ]

        if prefix:
            parts.append(self.base_url)

        url = "/".join(map(str, [*parts, *args]))

        return url

    def _request(self, method, url, *args, **kwargs):
        raise_error = kwargs.pop("raise_error", True)
        token       = kwargs.pop("token",   None)
        headers     = kwargs.pop("headers", { })
        proxies     = kwargs.pop("proxies", self._proxies)
        data        = kwargs.get("params",  kwargs.get("data"))

        headers.update({
            "User-Agent": USER_AGENT
        })

        if token:
            headers.update({
                HEADER_AUTHENTICATION: token
            })
        else:
            if self._auth_token:
                headers.update({
                    HEADER_AUTHENTICATION: self._auth_token
                })

        if proxies:
            proxies = random.choice(proxies)
            logger.info("Using proxy %s to dispatch request." % proxies)

        logger.info("Dispatching a %s Request to URL: %s with Arguments - %s" \
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
        :param args: Arguments provided to ``client._request``
        :param kwargs: Keyword Arguments provided to ``client._request``

        Usage::

            >>> import cc
            >>> client   = cc.Client()
            >>> response = client.post("api/module/12345/report")
            >>> response.content
            b'"First Name","Last Name","Email","Institution","Last Updated Date"\n'
        """

        url      = self._build_url(url)
        response = self._request("POST", url, *args, **kwargs)
        return response

    def ping(self, *args, **kwargs):
        """
        Check if the URL is alive.

        :param args: Arguments provided to ``client._request``
        :param kwargs: Keyword Arguments provided to ``client._request``

        Usage::

            >>> import cc
            >>> client = cc.Client()
            >>> client.ping()
            'pong'
        """

        url      = self._build_url("api", "ping")
        response = self._request("GET", url, *args, **kwargs)

        content  = response.json()

        if content["data"] == "pong":
            return "pong"
        else:
            raise ValueError("Unable to ping to URL %s." % self.base_url)

    def auth(self, *args, **kwargs):
        """
        Authenticate client.

        Usage::

            >>> import cc
            >>> client = cc.Client()
            >>> client.auth(email = "test@cellcollective.org", password = "test")
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

            url             = self._build_url("_api", "login", prefix = False)
            data            = dict(
                username    = email,
                password    = password
            )
            response        = self.post(url, data = data)
            
            auth_token      = response.headers.get(HEADER_AUTHENTICATION)

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

    @property
    def authenticated(self):
        _authenticated = bool(self._auth_token)
        return _authenticated

    def me(self, *args, **kwargs):
        """
        Get the user profile of the authenticated client.

        Usage::

            >>> import cc
            >>> client = cc.Client()
            >>> client.auth(email = "test@cellcollective.org", password = "test")
            >>> client.me()
            <User id=10887 name='Test Test'>
        """

        url      = self._build_url("_api", "user", "getProfile")
        response = self._request("GET", url, *args, **kwargs)
        
        content  = response.json()

        user     = _user_get_profile_response_object_to_user_object(content)

        return user

    def get(self, resource, *args, **kwargs):
        _resource   = resource.lower()
        resources   = [ ]

        id_         = kwargs.get("id_")
        query       = kwargs.get("query")

        size        = min(
            kwargs.get("size", MAXIMUM_API_RESOURCE_FETCH),
            MAXIMUM_API_RESOURCE_FETCH
        )
        since       = kwargs.get("since", 1)

        if id_:
            if isinstance(id_, str) and id_.isdigit():
                id_ = int(id_)

            id_ = sequencify(id_)

        if   _resource == "model":
            url     = self._build_url("_api", "model", "get")
            params  = None

            version = kwargs.get("version")
            hash_   = kwargs.get("hash_")

            if id_:
                url = self._build_url(url, str(id_[0]), prefix = False)

                if version:
                    params = { "version": str(version) + ("&%s" % hash_ if hash_ else "") }

            if query:
                url     = self._build_url(url, prefix = False)
                params  = [
                    ("search", "species"),
                    ("search", "knowledge"),
                    ("name",   query)
                ]

            response    = self._request("GET", url, params = params)
            content     = response.json()

            if id_:
                resources = QueryList([
                    _model_get_by_id_response_object_to_model_object(self, content)
                ])
            else:
                content   = content[since - 1 : since - 1 + size]
                resources = QueryList([
                    _model_get_response_object_to_model_object(self, obj)
                        for obj in content
                ])
        elif _resource == "user":
            if not id_:
                raise ValueError("id required.")

            url         = self._build_url("_api", "user", "lookupUsers")
            response    = self._request("GET", url,
                params = [("id", i) for i in id_]
            )

            content     = response.json()

            for user_id, user_data in content.items():
                user = _user_get_profile_response_object_to_user_object(
                    merge_dict({ "id": user_id }, user_data)
                )
                resources.append(user)

        return squash(resources)

    def read(self, filename, save = False):
        url         = self._build_url("_api", "model", "import", prefix = False)
        
        files       = dict({
            "upload": (filename, open(filename, "rb"))
        })

        response    = self.post(url, files = files)

        content     = response.json()

        model       = _model_get_by_id_response_object_to_model_object(self,
            content)
        model.dirty = True

        return model

    def search(self, resource, query, *args, **kwargs):
        return self.get(resource, query = query, *args, **kwargs)