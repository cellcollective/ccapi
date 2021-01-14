import pytest

import ccapi

def test_imports():
    from ccapi import (
        __name__    as _,
        __version__ as _,
        __author__  as _,
        Client,
        Configuration
    )

def test_load_model():
    with pytest.raises(ValueError):
        ccapi.load_model("foobar")
        
    # model = ccapi.load_model("fibroblasts")
