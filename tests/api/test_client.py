import pytest

import ccapi
from   ccapi.core.querylist import QueryList
from   ccapi.constant       import MODELS

config = ccapi.Configuration()

def test_get_model(client):
    models = client.get("model")
    assert len(models) == config.max_api_resource_fetch
    assert all((isinstance(m, ccapi.Model) for m in models))

    models = client.get("model", size = 10)
    assert len(models) == 10

def test_get_model_id(client):
    model   = client.get("model", id_ = 2176)
    assert model.name == "T-LGL Survival Network 2008"
    assert len(model.versions)      == 1

    version = model.default_version
    assert len(version.components)  == 61

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

def test_read_boolean(client):
    model   = client.read(MODELS["fibroblasts"]["path"])
    assert len(model.versions) == 1

    version = model.default_version
    assert len(version.components)          == 139
    assert len(version.internal_components) == 130
    assert len(version.external_components) == 9

def test_read_metabolic(client):
    @client.on("model")
    def on_model(model):
        assert len(model.versions) == 1

    client.read(MODELS["dehalococcoides"]["path"],
        type_ = MODELS["dehalococcoides"]["type"])