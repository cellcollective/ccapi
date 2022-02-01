# imports - module imports
from bpyutils.util.string import strip, strip_ansi, pluralize, kebab_case

def test_strip():
    string = "foobar"
    assert strip(string) == string

    string = "\n   foobar\nfoobar   \n   "
    assert strip(string) == "foobar\nfoobar"

    string = "\n\n\n"
    assert strip(string) == ""

def test_pluralize():
    assert pluralize("package",  1) == "package"
    assert pluralize("package",  2) == "packages"
    assert pluralize("packages", 2) == "packages"

def test_kebab_case():
    assert kebab_case("foo bar") == "foo-bar"
    assert kebab_case("Foo Bar") == "foo-bar"
    assert kebab_case("FOO BAR") == "foo-bar"

    assert kebab_case("_FOO_BAR_", delimiter = "_") == "foo-bar"
    assert kebab_case("foo_bar",   delimiter = "_") == "foo-bar"