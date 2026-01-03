<div align="center">

# PIVMeta: A Particle Image Velocimetry Ontology

Making PIV Data Understandable

![Tests](https://github.com/matthiasprobst/pivmeta/actions/workflows/tests.yml/badge.svg)

**PIVMeta is an ontology for Particle Image Velocimetry (PIV) that gives your experiments a clear, machine-readable
structure - helping others (and your future self) understand, reuse, and build upon your data.**

</div>

---

## Background

In the late 1990s and early 2000s — particularly during the PIV Challenges — several attempts were made to
standardize PIV data description. Although *netCDF* was suggested as a common file format, standardization efforts
were not continued.

Today, the PIV landscape features a wide variety of file formats and metadata conventions. Frequently,
metadata is incomplete, missing entirely, or stored informally in CSV file headers.  
**PIVMeta** reintroduces the idea of standardization by providing a formal ontology-based description of PIV data,
aligned with current good scientific practice and designed to ensure data **FAIRness** (Findable, Accessible,
Interoperable, Reusable).

The ontology is meant to be used alongside [metadata4ing](https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing)
and the [sSNO ontology](https://matthiasprobst.github.io/ssno/). This combination provides a robust metadata
infrastructure for describing experimental setups, processing workflows, and derived results.

Without proper documentation of used software, algorithms, and parameters, data quickly becomes useless for
re-analysis or sharing. Modern research practice increasingly demands metadata-rich datasets to ensure
transparency, reproducibility, and long-term value.

*PIVMeta* introduces a standard for describing PIV data using semantic web technology. It emphasizes reuse of existing
ontologies to minimize redundancy and to support smooth integration into broader engineering workflows.  
By adopting this approach, your data becomes **self-descriptive**, **reusable**, and **automatically explorable**,
enhancing both scientific collaboration and automated post-processing.

PIV experiments generate valuable data — but without context:

- ❌ Others can’t reproduce your results
- ❌ Crucial experimental details are lost over time
- ❌ Shared data lacks meaning
- ❌ Automated analysis becomes impossible

---

## The Solution

PIVMeta defines a **standardized, semantic structure** for every component of a PIV experiment:

- 📸 Image acquisition and camera setup
- ⚙️ Processing algorithms and parameters
- 📊 Velocity fields, uncertainties, and quality metrics
- 🔬 Experimental conditions and measurement environment

This ensures metadata is **interoperable, searchable, and reusable** - both by humans and machines.

---

## Key Benefits for Researchers

- **Reproducibility** – Enable exact replication of experiments.
- **Collaboration** – Share data with clear, interpretable structure.
- **Longevity** – Keep your datasets meaningful over time.
- **Automation-ready** – Allow tools to parse and process your data automatically.
- **Integration** – Combine datasets consistently across projects or labs.
- **Validation** – Check parameter consistency and identify anomalies early.

---

## Usage and Documentation

A detailed step-by-step guide is available in the  
[Guide document](Guide.md). It demonstrates how to construct the ontology’s JSON-LD files manually.

This requires some familiarity with the `m4i` ontology — see the
[First Step Guide](https://git.rwth-aachen.de/nfdi4ing/metadata4ing/metadata4ing/-/blob/1.2.1/training/first-steps-guide.md).  
PIVMeta also integrates with the [sSNO ontology](https://matthiasprobst.github.io/ssno/), providing standardized names
for PIV quantities (see the [sSNO Guide](https://github.com/matthiasprobst/ssno/blob/main/GUIDE.md)).

### Simplified interface: `pivmetalib`

### Simplified Interface: `pivmetalib`

Writing RDF data like JSON-LD manually can be cumbersome.  
The [**pivmetalib**](https://github.com/matthiasprobst/pivmetalib) Python package offers a high-level interface to
create and manage PIVMeta descriptions conveniently. It provides numerous examples across different PIV data types —
from raw images to evaluated experimental results (both synthetic and real).

## Developer instructions:

Do **not** edit `pivmeta.ttl` directly.  
Instead, modify `pivmeta_orig.ttl` and use the deployment script.

### 1. Update the ontology

- Edit [pivmeta_orig.ttl](pivmeta_orig.ttl) using an ontology editor (e.g., Protégé).
- Update the [standard name table](standard_name_table.yaml).

### 2. Generate the context file

- Run `deploy.py` to:
    - Insert standard names into the ontology
    - Build the ontology webpage (via [Widoco](https://dgarijo.github.io/Widoco/doc/tutorial/))
    - Generate the updated context file

## Tutorials (Describing PIV data)

Detailed examples and tutorials are provided in the
[pivmetalib repository](https://github.com/matthiasprobst/pivmetalib).  
There, you’ll find practical demonstrations of using *PIVMeta* to describe PIV images, synthetic datasets,
and evaluated velocity fields.

## Learn more

- 📘 **Ontology documentation**: [https://matthiasprobst.github.io/pivmeta/](https://matthiasprobst.github.io/pivmeta/)
- 💬 **Questions?** [Open an issue](https://github.com/matthiasprobst/pivmeta/issues)

## How to Cite

If you use PIVMeta in your research, please  
**[cite our work to support continued development](CITATION.cff)**.

