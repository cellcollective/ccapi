from ccapi.core.singleton import Singleton

class Configuration(Singleton):
    def __init__(self):
        self.DEFAULT = DEFAULT