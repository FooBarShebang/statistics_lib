# statistics_lib

Python 3 implementation of a basic statistics on sequences of not only real numbers, but also the 'real life measurements', i.e. 2-tuple values of the most probale / mean value and asssociated uncertainty / standard error. The statistical analysis can be performed with help of the implemented functions on such sequences directly , or using special classes, which encapsulate such sequences and provide the methods and propeties for the respective analisys.

The library also implements a number of continuous and discrete distributions as classes with the similar API, which can be used for the analysis of the shape and comparison of the statististical properties of the data sequence distribution with the model expectactions.

Finally, the library provides a number of functions to perform basic statistical hypothesis testing.

## Installation

Clone the official repository into your local workspace / project folder:

```bash
$git clone <repository_path> "your projects folder"/statistics_lib
```

Check the system requirements and dependencies:

```bash
$cd "your projects folder"/statistics_lib
$python3 ./check_dependencies.py
```

### For developers only

Initialize the UML templates submodule

```bash
$cd "your projects folder"/statistics_lib/Documents/UML/Templates
$git submodule init
```

Download the content of the UML templates submodule

```bash
$git submodule update --recursive --remote
```

## System requirements

This library is written in Python 3 programming language (>= v3.6) and is intended to be OS platform independent. At least, it is tested under MS Windows and GNU Linux OSes, see [Documents/Tests/tested_OS.md](./Documents/Tests/tested_OS.md).

This library depends on additional Python packages, which should be installed as well (see [Dependencies.md](./Dependencies.md)).

## Documentation

* [Design](./Documents/Design/index.md)
* [Requirements](./Documents/Requirements/index.md)
* [Test reports](./Documents/Tests/index.md)
* [User and API references](./Documents/References/index.md)
