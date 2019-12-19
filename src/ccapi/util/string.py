# imports - standard imports
import re
import uuid

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
_REGEX_HTML        = re.compile("<.*?>")

def strip(string):
    string = string.lstrip()
    string = string.rstrip()

    return string 

def strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string

def pluralize(string, count = 1):
    # A very shitty pluralizer
    if not string.endswith("s"):
        if count > 1:
            string += "s"
    
    return string

def kebab_case(string, delimiter = " "):
    words = string.replace(delimiter, " ").split()
    kebab = "-".join([word.lower() for word in words])
    
    return kebab

def safe_encode(obj, encoding = "utf-8"):
    try:
        obj = obj.encode(encoding)
    except (AttributeError, UnicodeEncodeError):
        pass
    
    return obj

def safe_decode(obj, encoding = "utf-8"):
    try:
        obj = obj.decode(encoding)
    except (AttributeError, UnicodeEncodeError):
        pass
    
    return obj

def sanitize_html(html):
    sanitized = re.sub(_REGEX_HTML, "", html)
    return sanitized

def sanitize_text(text):
    text = text.replace("&nbsp;", " ")
    text = strip(text)
    return text

def upper(text):
    text = text.upper()
    return text

def lower(text):
    text = text.lower()
    return text

def capitalize(text):
    text = text.capitalize()
    return text

def ellipsis(string, threshold = 50, pattern = "..."):
    length      = len(string)
    expected    = threshold + len(pattern) 

    if length > expected:
        string = string[:expected]
        string = "%s%s" % (string, pattern)

    return string

def get_random_str(string):
    uuid_   = uuid.uuid4()
    string  = str(uuid_)
    string  = string.replace("-", "")

    return string 