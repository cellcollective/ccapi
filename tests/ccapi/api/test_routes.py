import ccapi

def test_initialize():
    client = ccapi.Client()

    data   = client.get("_api/initialize")

    print(data)