# imports - module imports
from bpyutils.table import _sanitize_string, Table

def test_table():
    table  = Table()
    assert table.empty
    
    dummy  = ["foo", "bar"]

    table.insert(dummy)
    assert not table.empty
    
    string = table.render()
    assert string.count("\n") == 1

    table.header = dummy
    string = table.render()
    assert string.count("\n") == 2

    table.insert(dummy)
    string = table.render()
    assert string.count("\n") == 3