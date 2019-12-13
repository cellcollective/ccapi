class Singleton(type):
    instances = { }

    def __call__(self, *args, **kwargs):
        if not self in self.instances:
            super_ = super(Singleton, self)
            self.instances[self] = super_.__call__(*args, **kwargs)

        return self.instances[self]