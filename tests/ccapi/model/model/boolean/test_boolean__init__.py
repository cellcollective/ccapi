# imports - module imports
from ccapi.model import Model, BooleanModel, InternalComponent

def test_boolean_model(client):
    model    = Model(client = client, name = 'Cortical Area Development')
    bool_    = BooleanModel()
    
    Coup_fti = InternalComponent('Coup_fti')
    Sp8      = InternalComponent('Sp8')
    Pax6     = InternalComponent('Pax6')
    Fgf8     = InternalComponent('Fgf8')
    Emx2     = InternalComponent('Emx2')
    
    bool_.add_components(Coup_fti, Sp8, Pax6, Fgf8, Emx2)
    model.add_version(bool_)
    model.save()