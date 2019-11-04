<div align="center">
    <h1>
      CCPy
    </h1>
    <h4>
      A Python Library to interact with the 
      <a href="https://cellcollective.org">Cell Collective</a> API v2
    </h4>
</div>

<p align="center">
    <a href="https://travis-ci.org/achillesrasquinha/ccpy">
        <img src="https://img.shields.io/travis/achillesrasquinha/ccpy.svg?style=flat-square">
    </a>
    <a href="https://ci.appveyor.com/project/achillesrasquinha/ccpy">
        <img src="https://img.shields.io/appveyor/ci/achillesrasquinha/ccpy.svg?style=flat-square&logo=appveyor">
    </a>
    <a href="https://coveralls.io/github/achillesrasquinha/ccpy">
        <img src="https://img.shields.io/coveralls/github/achillesrasquinha/ccpy.svg?style=flat-square">
    </a>
    <a href="https://pypi.org/project/ccpy/">
		<img src="https://img.shields.io/pypi/v/ccpy.svg?style=flat-square">
	</a>
    <a href="https://pypi.org/project/ccpy/">
		<img src="https://img.shields.io/pypi/l/ccpy.svg?style=flat-square">
	</a>
    <a href="https://pypi.org/project/ccpy/">
		<img src="https://img.shields.io/pypi/pyversions/ccpy.svg?style=flat-square">
	</a>
    <a href="https://hub.docker.com/r/achillesrasquinha/ccpy">
		<img src="https://img.shields.io/docker/build/achillesrasquinha/ccpy.svg?style=flat-square&logo=docker">
	</a>
    <a href="https://git.io/boilpy">
      <img src="https://img.shields.io/badge/made%20with-boilpy-red.svg?style=flat-square">
    </a>
	<a href="https://saythanks.io/to/achillesrasquinha">
		<img src="https://img.shields.io/badge/Say%20Thanks-🦉-1EAEDB.svg?style=flat-square">
	</a>
	<a href="https://paypal.me/achillesrasquinha">
		<img src="https://img.shields.io/badge/donate-💵-f44336.svg?style=flat-square">
	</a>
</p>

**CCPy** is a Python Package that provides a simple interface to 
[Cell Collective](https://cellcollective.org) for modelling and analysis of 
biological networks.

### Table of Contents
* [Features](#Features)
* [Installation](#installation)
* [Usage](#usage)
* [License](#license)

#### Features

#### Installation

```shell
$ pip install <package>
```

#### Usage

```python
>>> import cc
>>> client = cc.Client()
>>> model  = client.read("sample.sbml")
>>> model.species[:3]
[<Species id=-1026 name='MMP3'>,
 <Species id=-1028 name='MMP1'>,
 <Species id=-1030 name='MMP1'>]
```

##### Authentication

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

##### Reading Models

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

##### Fetching  Models

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

##### Searching Models

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

#### License

This repository has been released under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using <a href="https://git.io/boilpy">boilpy</a>.
</div>