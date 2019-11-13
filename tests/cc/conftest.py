# imports - test imports
import pytest

# imports - module imports
import cc

@pytest.fixture()
def client():
    client = cc.Client()
    client.auth(email = "test@cellcollective.org", password = "test")
    return client