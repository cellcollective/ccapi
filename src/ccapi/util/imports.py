class HandlerRegistry(dict):
    def __missing__(self, name):
        if '.' not in name:
            handler = __import__(name)
        else:
            module_name, handler_name = name.rsplit('.', 1)

            module = __import__(module_name, {}, {}, [handler_name])
            handler = getattr(module, handler_name)

            self[name] = handler

        return handler

_HANDLER_REGISTRY = HandlerRegistry()

def import_handler(name, default = None, raise_err = True, err_str = None):
    handler = default

    try:
        handler = _HANDLER_REGISTRY[name]
    except ImportError:
        if raise_err:
            if err_str:
                raise ImportError(err_str)
            else:
                raise

    return handler