

# imports - module imports
from ccapi.exception import (
    CcapiError
)

# imports - test imports
import pytest

def test_ccapi_error():
    with pytest.raises(CcapiError):
        raise CcapiError