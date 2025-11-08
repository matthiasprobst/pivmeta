# PIV Meta

![Tests](https://github.com/matthiasprobst/pivmeta/actions/workflows/tests.yml/badge.svg)

This repository contains the (draft) PIV metadata ontology to describe PIV data. The ontology stored in the turtle file
[pivmeta.ttl](pivmeta.ttl) is extending the [metadata4ing ontology](http://w3id.org/nfdi4ing/metadata4ing/) by using
standard names as defined in the [sSNO ontology](https://matthiasprobst.github.io/ssno/).

The ontology is documented online [here](https://matthiasprobst.github.io/pivmeta/).

## Motivation/Background

Particle Image Velocimetry is missing a common standard to describe the resources (images, results, setups, ...).
However, it is important to make data understandable, especially if made available for others or to re-interpret
past results. In both cases, without proper description of used software, algorithms and their parameters, data quickly
becomes useless as those meta information constitute vital information.

Moreover, state-of-the-art and good scientific practice of current and future research require to enrich scientific
data with metadata.

*PIVMeta* is a first attempt to establish a standard for the description of PIV data. The concept is based on
semantic web technology by describing PIV data with a newly established ontology. The main design principle is to
reuse already existing ontologies and concepts, which reduces the overhead and allows smooth integration in other
engineering workflows and datasets. Ultimately, PIVMeta contributes to significantly improve the FAIRness scientific
practice like
of data sets.

[//]: # (The ontology shall enrich your PIV data with information about involved researchers, projects and most importantly about)

[//]: # (the parameters and variables used or created.)
As a main outcome of adopting the concept to your data, it not only becomes self-descriptive and
hence easily re-usable, a great benefit by automatic exploration and post-processing is obtained.

## Usage and Documentation

A detailed guide on how to use the ontology is provided in
[Guide document](Guide.md). This documents builds the JSON-LD file from scratch. It requires some knowledge, which can
be acquired by referring to the `m4i` ontology [First Step Guide](
https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/training/first-steps-guide.md) as this
ontology is built upon it. The ontology also uses the [sSNO ontology](https://matthiasprobst.github.io/ssno/), which is
a standard name ontology. It allows to use standard names for the description of PIV data. The sSNO ontology is
documented in the [sSNO Guide](https://github.com/matthiasprobst/ssno/blob/main/GUIDE.md).

### Simplified interface: `pivmetalib`

Writing JSON-LD files from scratch can be cumbersome. Therefore, a python package is provided to simplify the process of
writing JSON-LD files. Please refer to [pivmetalib](https://github.com/matthiasprobst/pivmetalib), which is the pythonic
way to describe PIV data using the *PIVMeta* ontology. It covers many examples of describing various PIV data from PIV
images, to PIV evaluation results of synthetic and real recordings.

## Developer instructions:

DONT touch the `pivmeta.ttl` file directly. Instead, use the `pivmeta_orig.ttl` file and the `deploy.py` script to
generate the `pivmeta.ttl` file. Here are detailed instructions on how to do so:

1. Updating the ontology:

- Update the `.ttl` file [pivmeta_orig.ttl](pivmeta_orig.ttl)
- You may use Protégé or any other ontology editor to do so.
- Update the [standard name table file](standard_name_table.yaml)

2. Generate the context file:

- Run `deploy.py`
- This will insert the standard names into the ontology
- It will build the ontology web page (using [widoco](https://dgarijo.github.io/Widoco/doc/tutorial/))
- It will also generate the context file

### Describing PIV data (a tutorial)

Tutorials are outsourced to a separate package: Please refer
to [pivmetalib](https://github.com/matthiasprobst/pivmetalib), which is the pythonic way to describe PIV data using
the *PIVMeta* ontology. It covers many examples of describing various PIV data from PIV images, to PIV evaluation
results of synthetic and real recordings.

## Background

In the late 1990th and early 2000th, the, especially during the PIV Challenges, initial attempts were made to
standardize the description of PIV data. Although netCDF was proposed as a common file format, for some reason, the
standardization process was not continued. Today PIV landscape reveals a variety of file formats and metadata. Often,
even metadata is missing completely or is only provided as column header in a CSV file. With this ontology, we provide a
first attempt to standardize the description of PIV data. The ontology is based on current good scientific practice and
ensures FAIRness of data. It is designed to be used in combination with the metadata4ing ontology and the sSNO ontology.

## Contribution

Contributions are happily taken via issues in the repository.
