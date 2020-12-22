
def patch():
    # https://github.com/gevent/gevent/issues/1016#issuecomment-328529454
    # Monkey-Patch
    from gevent import monkey as curious_george
    curious_george.patch_all(thread = False, select = False)