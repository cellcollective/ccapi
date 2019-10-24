### CCPy: Python Client Library for the [Cell Collective](https://cellcollective.org) API

**CCPy** is a Python Package that provides a simple interface to 
[Cell Collective](https://cellcollective.org) for modelling and analysis of 
biological networks.

```python
>>> import cc
>>> client = cc.Client()
>>> model  = client.read("sample.sbml")
>>> model.species[:3]
[<Species id=-1026 name='MMP3'>,
 <Species id=-1028 name='MMP1'>,
 <Species id=-1030 name='MMP1'>]
```

#### Authentication

[Cell Collective](https://cellcollective.org) API supports a basic 
*password flow* authentication scheme in order to fetch data from your own 
account.

```python
>>> import cc
>>> client = cc.Client()
>>> client.auth(email = "<YOUR_EMAIL_ADDRESS>", password = "<YOUR_PASSWORD>")
>>> client.authenticated
True
```

#### Reading Models

```python
>>> import cc
>>> client = cc.Client()
>>> model  = client.read("sample.sbml")
>>> model.species[:3]
[<Species id=-1026 name='MMP3'>,
 <Species id=-1028 name='MMP1'>,
 <Species id=-1030 name='MMP1'>]
```