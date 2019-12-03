from ccapi.model import Model, BooleanModel

def test_model(client):
    model = Model(client = client)
    model.save()

    model = Model(client = client, name = "Test")
    model.save()

    model = Model(client = client, name = "Multiple Versions")
    bool_ = BooleanModel("Boolean Model")
    model.add_version(bool_)
    model.save()