# imports - module imports
from bpyutils.util.types import (
    dict_from_list,
    get_function_arguments
)

_TEST_GLOBAL = "foobar"

def test_dict_from_list():
    assert dict_from_list(["foo", "bar"], [1, 2]) == dict(foo = 1, bar = 2)
    assert dict_from_list([1, 2], ["foo", "bar"]) == { 1: "foo", 2: "bar" }

def test_get_function_arguments():
    def foobar(foo = "bar", bar = "baz"):
        pass
    def barfoo():
        pass
    foobar(); barfoo() # Increase coverage
    
    assert get_function_arguments(foobar) == dict(foo = "bar", bar = "baz")
    assert get_function_arguments(barfoo) == dict()