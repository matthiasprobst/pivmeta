# PIV Meta

This repository contains the (draft) PIV metadata ontology to describe PIV data. The ontology stored in the turtle file
[pivmeta.ttl](pivmeta.ttl) is built upon the [metadata4ing ontology](http://w3id.org/nfdi4ing/metadata4ing/). The web
version can be found [here](https://matthiasprobst.github.io/pivmeta/). A [Tutorial](Guide.md) helps with the 
first steps.

## Motivation
For PIV data, there is no standard to describe the data. However, state-of-the-art and good scientific 
practice require to enrich scientific data with metadata. *PIVMeta* is a first attempt to establish a
standard for the description of PIV data, based on current good scientific practice like ensuring FAIRness 
of data.

## Goal
The ontology shall enrich your PIV data with information about involved researchers, projects and most 
importantly about the parameters and variables used or created. Using a standardized metadata approach 
like *PIVMeta*, PIV data becomes interoperable, which improves sharing and reusing of it. As data becomes 
machine-actionable, PIV post-processing can easily be automated, resulting in efficient workflows.

## Background
In the late 1990th and early 2000th, 
the, especially during the PIV Challenges, initial attempts were made to standardize the description of PIV data. 
Although netCDF was proposed as a common file format, for some reason, the standardization process was not continued.
Today PIV landscape reveals a variety of file formats and metadata. Often, even metadata is missing completely or is 
only provided as column header in a CSV file.

## Usage
PIVMeta is built upon m4i, an ontology designed by the NFDI4Ing to support the engineering sciences with 
documenting their research. A detailed guide on how to use the ontology is provided in 
[a separate document](Guide.md). It is also worth checking the [First Step Guide](
https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/training/first-steps-guide.md) of 
*m4i*, as 
PIVMeta is built upon the metadata4ing ontology.

## Concept
The ontology extends the metadata4ing ontology by adding
- PIV specific classes for the description of PIV parameters
- Coordinate concept to allow to distinguish between data in local (moving, rotating) and global (stationary) coordinate systems
- the concept of *standard names*.

## Documentation
The documentation of the ontology is available [here](https://matthiasprobst.github.io/pivmeta/).

## Contribution
Contributions are happily taken via issues in the repository.
