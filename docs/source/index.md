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

>>> model.regulators[:3]
[<Regulator id=-1332 type='positive'>,
 <Regulator id=-1333 type='positive'>,
 <Regulator id=-1334 type='positive'>]
```

#### Fetching  Models

```python
>>> import cc
>>> client = cc.Client()
>>> models = client.get("model")
[<Model id=2309>,
 <Model id=5128>,
 <Model id=10248>,
 <Model id=2314>,
 <Model id=16659>]
```

#### Searching Models

```python
>>> import cc
>>> client = cc.Client()
>>> models = client.search("model", "T Cell")
[<Model id=2176>,
 <Model id=3521>,
 <Model id=2691>,
 <Model id=2314>,
 <Model id=11916>]
```