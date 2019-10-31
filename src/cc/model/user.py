# imports - module imports
from cc.model.resource import Resource

# TODO: Auto Save

class User(Resource):
    """
    A User resource object.

    Usage::

        >>> import cc
        >>> client = cc.Client()
        >>> client.auth(email = "test@cellcollective.org", password = "test")
        >>> user   = client.me()
        >>> user
        <User id=10887 name='Test Test'>
        >>> user.name
        'Test Test'
    """

    FIELDS = {
        "first_name": {
            "target":   "firstName",
            "type":     (str,),
            "none":     True
        },
        "last_name": {
            "target":   "lastName",
            "type":     (str,),
            "none":     True
        },
        "email": {
            "target":   "email",
            "type":     (str,),
            "none":     True
        },
        "institution": {
            "target":   "institution",
            "type":     (str,),
            "none":     True 
        }
    }

    def __init__(self,
        id          = None,
        first_name  = None,
        last_name   = None,
        email       = None,
        institution = None,
        autosave    = False,
        client      = None
    ):
        self.first_name     = first_name
        self.last_name      = last_name

        Resource.__init__(self, id = id, name = self.name, autosave = autosave,
            client = client)

        self.email          = email
        self.institution    = institution

    @property
    def name(self):
        _name = None

        if self.first_name:
            _name = self.first_name

            if self.last_name:
                _name += " " + self.last_name

        return _name

    def save(self):
        """
        Save user details.

        Usage::

            >>> user.first_name = 'foobar'
            >>> user.save()
        """

        data = self._prepare_save_data(self)

        self._client.raise_for_authentication()
        me   = self._client.me()
        if not me == self:
            raise ValueError("User %s cannot save for user %s" % (me, self))
        else:
            self._client.post("_api/user/saveProfile", json = data)