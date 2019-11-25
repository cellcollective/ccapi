# imports - test imports
import pytest

# imports - module imports
import ccpaw

@pytest.fixture()
def client():
    client = ccpaw.Client()
    client.auth(email = "test@cellcollective.org", password = "test")
    return client