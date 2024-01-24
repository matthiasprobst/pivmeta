# PIV Meta

![Tests](https://github.com/matthiasprobst/pivmeta/actions/workflows/tests.yml/badge.svg)

This repository contains the (draft) PIV metadata ontology to describe PIV data. The ontology stored in the turtle file
[pivmeta.ttl](pivmeta.ttl) is extends the [metadata4ing ontology](http://w3id.org/nfdi4ing/metadata4ing/) by using
standard names as defined in the [sSNO ontology](https://matthiasprobst.github.io/ssno/).

These tow general ontologies complement each other very well, as the "ssno:hasStandardName"-property allows to specify
the meaning of a "m4i:NumericalVariable".

Beyond this symbiosis, the PIVMeta ontology provides a set of classes and properties to describe PIV processes and
properties such as pre-processing steps, evaluation algorithms, peak finding methods etc.

The ontology reuses multiple ontologies:

- m4i: [Metadata4Ing](http://w3id.org/nfdi4ing/metadata4ing/): An ontology for describing the generation of research
  data within a scientific activity
- schema: [schema.org](https://schema.org/)
- sd: [Software Description Ontology](https://w3id.org/okn/o/sd#)
- dcat: [Data Catalog Vocabulary](https://www.w3.org/TR/vocab-dcat-3/)
- *to be completed*
- ...

The web version can be found [here](https://matthiasprobst.github.io/pivmeta/). A [Tutorial](Guide.md) helps with the
first steps. The latest context file
is [here](https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld)

## Usage

A detailed guide on how to use the ontology is provided in
[a separate document](Guide.md). It is also worth checking the [First Step Guide](
https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/training/first-steps-guide.md) of
*m4i* and the [Guide](https://github.com/matthiasprobst/ssno/blob/main/GUIDE.md) of *sSNO*, as PIVMeta extends and uses
both ontologies.

### Describing a PIV dataset

A separate example/guide to describe a PIV dataset can be found [here](tutorial/DescribeDataset.md).

## Motivation

For PIV data, there is no standard to describe the data. However, state-of-the-art and good scientific practice require
to enrich scientific data with metadata. *PIVMeta* is a first attempt to establish a standard for the description of PIV
data, based on current good scientific practice like ensuring FAIRness of data.

## Goal

The ontology shall enrich your PIV data with information about involved researchers, projects and most importantly about
the parameters and variables used or created. Using a standardized metadata approach like *PIVMeta*, PIV data becomes
interoperable, which improves sharing and reusing of it. As data becomes machine-actionable, PIV post-processing can
easily be automated, resulting in efficient workflows.

## Background

In the late 1990th and early 2000th, the, especially during the PIV Challenges, initial attempts were made to
standardize the description of PIV data. Although netCDF was proposed as a common file format, for some reason, the
standardization process was not continued. Today PIV landscape reveals a variety of file formats and metadata. Often,
even metadata is missing completely or is only provided as column header in a CSV file.

## Concept

The ontology extends the metadata4ing ontology by adding

- PIV specific classes for the description of PIV parameters
- the concept of *standard names* through the *sSNO* ontology.

## Documentation

The documentation of the ontology is available [here](https://matthiasprobst.github.io/pivmeta/).

## Contribution

Contributions are happily taken via issues in the repository.
