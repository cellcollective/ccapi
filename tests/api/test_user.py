import pytest

import ccapi

def test_me(auth_client):
    user = auth_client.me()
    assert isinstance(user, ccapi.User)
    assert auth_client.authenticated