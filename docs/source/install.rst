.. _install:

### Installation

#### Installation via pip

The recommended way to install **ccapi** is via `pip`.

```shell
$ pip install ccapi
```

For instructions on installing python and pip see “The Hitchhiker’s Guide to Python” 
[Installation Guides](https://docs.python-guide.org/starting/installation/).

#### Building from source

`ccapi` is actively developed on [https://github.com](https://github.com/cellcollective/ccapi)
and is always avaliable.

You can clone the base repository with git as follows:

```shell
$ git clone https://github.com/cellcollective/ccapi
```

Optionally, you could download the tarball or zipball as follows:

##### For Linux Users

```shell
$ curl -OL https://github.com/cellcollective/tarball/ccapi
```

##### For Windows Users

```shell
$ curl -OL https://github.com/cellcollective/zipball/ccapi
```

Install necessary dependencies

```shell
$ cd ccapi
$ pip install -r requirements.txt
```

Then, go ahead and install ccapi in your site-packages as follows:

```shell
$ python setup.py install
```

Check to see if you’ve installed ccapi correctly.

```shell
$ ccapi --help
```