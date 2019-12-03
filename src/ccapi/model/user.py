# imports - module imports
from ccapi.model.resource  import Resource
from ccapi.core.mixins     import JupyterHTMLViewMixin
from ccapi.template        import render_template

class User(Resource, JupyterHTMLViewMixin):
    """
    A User resource object.

    Usage::

        >>> import ccapi
        >>> client = ccapi.Client()
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
        first_name  = None,
        last_name   = None,
        email       = None,
        institution = None,
        *args, **kwargs
    ):
        self.first_name     = first_name
        self.last_name      = last_name

        Resource.__init__(self, name = self.name, *args, **kwargs)

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
        data = self._prepare_save_data()

        self.client.raise_for_authentication()
        me   = self.client.me()
        if not me == self:
            raise ValueError("User %s cannot save for user %s" % (me, self))
        else:
            self._client.post("_api/user/saveProfile", json = data)

    def _repr_html_(self):
        context = dict({
            "id":               self.id,
            "name":             self.name,
            "memory_address":   "0x0%x" % id(self),
            "first_name":       self.first_name,
            "last_name":        self.last_name,
            "email":            self.email,
            "institution":      self.institution
        })

        html = render_template("user.html", context = context)

        return html