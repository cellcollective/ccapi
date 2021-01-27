def patch():
    from gevent.monkey import monkey as curious_george
    curious_george.patch_all()