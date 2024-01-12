# Guide on how to use PIVMeta

We want to start with writing a metadata file in the JSON-LD format from scratch. What is the other option? You could
write code to generate the file yourself. The package [pivmetalib]()
provides high-level functions, which may be interesting for your PIV workflows. It helps enriching your (metadata) files
by creating JSON files including a validation mechanism. A JSON-LD viewer is also provided.

However, in this document, we go through the steps manually and explain the parts of an example metadata file for a PIV
recording.

After you have worked through this tutorial, you may want to check the example metadata files created for some of the
published PIV datasets of the PIV Challenges.

But know let's finally start...

## Writing a JSON-LD metafile from scratch

The context JSON-LD file can be found
[here](https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta.jsonld). It should be added at the
beginning of the JSON-LD file to be validated. It contains the translation of keys to their IRIs and thereby giving *
context* to the JSON data written afterwards.

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta.jsonld"
  }
}
```

Information, generally key-value pairs, are added in the "@graph" entry of the JSON dictionary. Let's start
by [adding a contact person](#add-contact-persons).

### Add (contact) persons

It is crucial to add a person. This is possibly the first thing you want to do, because this allows to get in touch with
you or your affiliated institution upon questions.

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta.jsonld",
    "orcid": "https://orcid.org/",
    "local": "_:"
  },
  "@graph": [
    {
      "@id": "orcid:0000-0001-8729-0482",
      "@type": [
        "person",
        "contact person"
      ],
      "has ORCID Id": "0000-0001-8729-0482",
      "firstName": "Matthias",
      "lastName": "Probst",
      "role": "contact person",
      "affiliation": {
        "@id": "_:myInstitution",
        "@type": "organization",
        "name": "Karlsruhe Institute of Technology"
      }
    }
  ]
}
```

### Adding information about the PIV setup

The PIV setup tells us, which tools were used, what kind of flow was investigated and which tracer particles were used.
Parameters like the optical magnification could also be noted here. However, technically it is the outcome of the
calibration process and will be set later (Nothing stops you from adding it here, though. As long as we are using the
ontology with the unique identifiers, users will be able to identify the optical magnification securely).

Let's start by adding a camera and a laser to our equipment (tool:)

#### Adding tools (instruments/equipment)

The type of tool, i.e. the camera, laser and optics used may be of interest in later analysis. Adding tools is nothing,
which is specific to PIVMeta, however, for the sake of completeness, it is shown here. For more information, please
refer to the [m4i documentation]().

```json
{
  "@context": {
    ...
  },
  "@graph": [
    ...,
    {
      "@id": "local:piv_cam_01",
      "@type": [
        "tool",
        "camera"
      ],
      "model": 'The best camera',
      "manufacturer": "CameraBuilder"
    }
  ]
}
```

#### Adding PIV specific information

Specific to a PIV setup is the medium under investigation and the tracer particles.

### Add PIV processing steps

The PIV processing steps describe everything from the actual recording of images (including calibration and possibly
backgorund images) to the computational steps like image pre processing, performing the piv algorithm and the outlier
detection in the post processing.

The processing steps will transparently show which actions were taken. Who recorded the images and with which
instruments? Did you perform a calibration and how? Did you apply filters on your data? Which ones? Which software did
you use? Did you use a mask? Which mask method did you apply? Did you perform a validation? Which were the methods to
detect outliers?

#### PIV Measurement

The measurement itself is about recording a calibration and background image as well as the series of images.

We will distinguish two or three measurement steps here.

- calibration
- Recording or computing background image
- recording image series

The order is not really relevant in most PIV cases. Also note, that the background can be either measured (recording
without seeding particles) or computed based on all or a couple of images from the actual measurement. In this tutorial
we will use the latter. We could also argue to put the computation of the background image into a different processing
step, namely the PIV pre processing step. The only importance is, that it is included in one of the processing steps,
that makes sense to you.

First, define the processing step `local:piv_measurement`:

```json
{
  "@context": {
    ...,
{
  "@id": "local:piv_measurement",
  "@type": "processing step",
  "has participant": "orcid:0000-0001-8729-0482",
  "start time": "2024-09-01T08:14:31",
  "end time": "2024-09-01T10:30:04",
  "has employed tool": [
    "local:piv_cam_01",
    "local:piv_laser_01"
  ],
  "realizes method": [
    "local:piv_calibration",
    "local:piv_recording",
    "local:piv_background_computation"
  ]
},
}
}
```

Next, we define the methods, that were "realized" by the processing step. First the calibration. This method has an
output, namely the calibration image, which we reference with a file path:

```json
{
  "@context": {
    ...
  },
  "@graph": [
    ...,
    {
      "@id": "local:piv_measurement",
      ...
    },
    {
      "@id": "local:piv_calibration",
      "@type": [
        "method",
        "piv method"
      ],
      "description": "Calibration to determine optic magnification",
      "has output": {
        "@type": "dataset",
        "@id": "local:xrct_data_0001",
        "has file distribution": [
          {
            "media type": "image/tiff",
            "download url": "file://path/to/calibration.tiff"
          }
        ]
      }
    }
  ]
}
```

Next, we add the actual PIV recording step. It has multiple outputs. Here we can also define the tracer particles as
tools, that were used. This is technically not true, because it is a material. At the point of writing, the m4i does not
allow for such definition. It is work in progress to check, whether the tracer particles can be better semantically
described.

```json
{
  "@context": {
    ...
  },
  "@graph": [
    ...,
    {
      "@id": "local:piv_measurement",
      ...
    },
    {
      "@id": "local:piv_calibration",
      ...
    },
    {
      "@id": "local:piv_recording",
      "@type": [
        "method",
        "piv method"
      ],
      "piv dimensions": "2D2C",
      "piv evaluation type": "PIV",
      //could also be PTV or microPTV
      "description": "Standard planar 2D2C PIV measurement",
      "has parameter": [
        {
          "@id": "local:mean_particle_size",
          // specific variable, to distinctly identify th particle size
          "@type": "numerical variable",
          "label": "mean particle size",
          "standard name": "pivm:MeanSeedingParticleSize",
          "has kind of quantity": "http://qudt.org/vocab/quantitykind/Diameter",
          "has numerical value": "140",
          "has unit": "http://qudt.org/vocab/unit/MicroM",
          "description": "The mean tracer particle size as stated by the product specifications"
        },
        {
          "@id": "local:seeding_material",
          // specific variable, to distinctly identify th particle size
          "@type": [
            "text variable",
            "tracer material name"
          ],
          "label": "seeding material",
          "has string value": "DEHS",
          "description": "The seeding material used."
        }
      ]
    },
    {
      "@id": "local:piv_pre_processing",
      "@type": "pre processing step",
      "has participant": "orcid:0000-0001-8729-0482",
      "realizes method": "local:piv_calibration"
    }
  ]
}
```

### Standard names and tables

The concept of standard names allows to define numerical variables without creating a subclass or an individual within a
ontology. A variable can have a `standard name` which is defined by a `standard name table` as shown in the below
Figure. The concept is adopted from the [cf-conventions](https://cfconventions.org/).

<img src="./docs/figs/standardname_m4i_pivm.png">

In future this concept may go to a separate ontology and then being reused here. But for now, it is included in PIVMeta.
Depending on the use case it may be reasonable to define an individual of a *standard name* in an ontology. An example
for this is `piv:x_velocity`. It is the PIV velocity in horizontal direction, where "velocity" refers to the estimated
velocity based on the applied PIV algorithm and *not* the true velocity. This is an example for a standard name, which
will be used in any PIV measurement and is therefore a reasonable choice to publish in an ontology like PIVMta.

In other cases, you may want to define a variable within the scope of your project or application. E.g. you want to
define the static pressure difference across your pip test section, which you may choose to call "
difference_of_pressure_across_the_test_section". Together with a canonical unit and a comprehensive descriptions, others
will understand the variable and can reuse it, too. You can write define it as part of the metadata JSON file or in a
standard name table. The table is a document containing a table of all possible standard names with there canonical unit
and a description. Both options, using an individual from the ontology or defining it in a standard name table, are
shown in the following.

We will examine the scenarios *A* and *B* for the *mean seeding particle size*:

- A: The standard name `mean seeding particle size` is already defined in PIVMeta (We did this in the last section, so
  please hae a look there again).
- B: It is *not* yet defined in PIVMeta but in a standard name table. We define it in the following.

In scenario *B*, we set "standard name" to the local identifier `"@id": "local:mean_seeding_particle_size"` and define
it afterwards. If a standard name table (document) exists, it would be enough to add the entry "standard name table".
However, it is good practice to also list the other properties of the standard name
(it makes the JSON file more readable but also longer...).

```json
{
  "@context": {
    ...
  },
  "@graph": [
    ...,
    {
      ...,
      "has parameter": [
        {
          "@id": "local:mean_particle_size",
          "@type": "numerical variable",
          "label": "mean particle size",
          "standard name": "local:mean_seeding_particle_size",
          ...
        },
        ...
      ]
    },
    // standard name table:
    {
      "@id": "local:standard_name_table",
      "@type": "standard name table",
      "identifier": "https://doi.org/10.5281/zenodo.10428817",
      "downloadUrl": "https://zenodo.org/records/10428817/files/tutorial_standard_name_table.yaml?download=1",
      "standard name": [
        {
          // example standard name from the table:
          "@id": "local:mean_seeding_particle_size",
          "@type": "standard name",
          "long name": "mean seeding particle size",
          "canonical units": "m",
          "description": "The mean seeding particle size.",
          "definedByTable": "https://doi.org/10.5281/zenodo.10428817"
        },
        ...
      ]
    }
  ]
}
```

The full JSON-LD file can be found [here]().