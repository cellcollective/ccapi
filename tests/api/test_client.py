import pytest

import ccapi
from   ccapi.core.querylist import QueryList

@pytest.fixture
def client():
    client = ccapi.Client()
    return client

def test_get_user(client):
    with pytest.raises(ValueError):
        client.get("user")

    def assert_user(user, id_, first_name, last_name, email = None, institution = None):
        assert isinstance(user, ccapi.User)
        assert user.id          == id_
        assert user.first_name  == first_name
        assert user.last_name   == last_name
        assert user.email       == email
        assert user.institution == institution

    user   = client.get("user", id_ = 686)
    assert_user(user, 686, "Tomas", "Helikar")

    users  = client.get("user", id_ = [70, 73])
    assert isinstance(users, QueryList)
    assert_user(users[0], 70, "Audrey", "Crowther")
    assert_user(users[1], 73, "Benny", "Chain")

def test_get_model(client):
    models = client.get("model")