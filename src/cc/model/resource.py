class Resource:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get("id")
        
    def __eq__(self, other):
        return self.id == other.id