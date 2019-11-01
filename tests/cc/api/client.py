# imports - module imports
import cc
from   cc.exception import (
    ConnectionError,
    AuthenticationError
)

# imports - standard imports
import pytest

_INVALID_URL    = "http://thisisaninvalidurl.com"
_TEST_EMAIL     = "test@cellcollective.org"
_TEST_PASSWORD  = "test"

_BASE_CLIENT    = cc.Client()

def test_client():
    # Check proxy definitions.
    with pytest.raises(TypeError):
        cc.Client(proxies = "foobar")
    with pytest.raises(TypeError):
        cc.Client(proxies = [{ "foobar": "barbaz" }])
    with pytest.raises(TypeError):
        cc.Client(proxies = [{ "foobar": "barbaz" }, { "protocol": "barbaz" }])

    with pytest.raises(ConnectionError):
        cc.Client(base_url = _INVALID_URL)

    cc.Client(base_url = _INVALID_URL, test = False)

    assert not _BASE_CLIENT.authenticated

def test_client_repr():
    repr_  = "<Client url='{}'>"

    def _test(client):
        assert repr(client) == repr_.format(client.base_url)

    _test(_BASE_CLIENT)

    client = cc.Client(_INVALID_URL, test = False)
    _test(client)

def test__build_url():
    def _test(parts):
        url = _BASE_CLIENT._build_url(*parts)
        assert url == "/".join([_BASE_CLIENT.base_url, *parts])

    parts  = ["foo", "bar"]
    _test(parts)

    parts  = ["bar", "baz"]
    _test(parts)

def test__request():
    raise NotImplementedError

def test_post():
    raise NotImplementedError

def test_ping():
    assert _BASE_CLIENT.ping() == "pong"

def test_auth():
    with pytest.raises(ValueError):
        _BASE_CLIENT.auth()
    with pytest.raises(ValueError):
        _BASE_CLIENT.auth(email = "foobar@gmail.com")

    assert not _BASE_CLIENT.authenticated
    _BASE_CLIENT.auth(email = _TEST_EMAIL, password = _TEST_PASSWORD)
    assert _BASE_CLIENT.authenticated
    
    client = cc.Client()
    assert not client.authenticated
    client.auth(token = _BASE_CLIENT._auth_token)
    assert client.authenticated

    _BASE_CLIENT.logout()
    client.logout()

    with pytest.raises(AuthenticationError):
        _BASE_CLIENT.auth(email = "thisisaninvalidemail.org",
            password = "invalid")

def test_raise_for_authentication():
    with pytest.raises(AuthenticationError):
        _BASE_CLIENT.raise_for_authentication()

def test_me():
    _BASE_CLIENT.auth(email = _TEST_EMAIL, password = _TEST_PASSWORD)
    user = _BASE_CLIENT.me()

    assert user.email == _TEST_EMAIL
    assert user.first_name
    assert user.last_name
    assert user.name  == "%s %s" % (user.first_name, user.last_name)
    assert user.institution

    _BASE_CLIENT.logout()

def test_get():
    raise NotImplementedError

def test_read():
    raise NotImplementedError

def test_search():
    raise NotImplementedError