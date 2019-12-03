# imports - test imports
import pytest

# imports - module imports
import ccapi

@pytest.fixture()
def client():
    client = ccapi.Client()
    client.auth(email = "test@cellcollective.org", password = "test")
    return client