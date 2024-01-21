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

## 1. First lines of a JSON-LD metadata file

The context JSON-LD file can be found
[here](https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld). It should be added at the
beginning of the JSON-LD file to be validated. It contains the translation of keys to their IRIs and thereby giving *
context* to the JSON data written afterwards. Then, we will add multiple metadata elements. They will go into the "
@graph":

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
  },
  "@graph": [
  ]
}
```

## 2. General information

Adding general information about the PIV data is important. It allows users to understand the data and its origin, the
goal of the investigation, its funding or persons to contact. It nothing specific to *PIVMeta*. We will use
*m4i* for this. For the sake of completeness, we added it to this guide.

### 2.1 Add a persons

We will add "John Doe" as a contact person. He can be identified by an ORCID ID. The ID will be taken as a JSON-LD key (
@ID), too.

```json
{
  "@context": {
    "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld",
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
      "firstName": "John",
      "lastName": "Doe",
      "role": "contact person",
      "affiliation": {
        "@id": "local:myInstitution",
        "@type": "organization",
        "name": "John Doe's Institute of Technology"
      }
    }
  ]
}
```

### 2.2 Add project information

We can again reuse the m4i ontology and add information about the research project.

```json
{
  ...,
  "@graph": [
    ...,
    {
      "@id": "local:MyResearchProject",
      "@type": "m4i:ResearchProject",
      "keywords": [
        "2D2C",
        "PIV",
        "flow around a duck"
      ],
      "description": "Very important research project",
      "members": [
        "orcid:0000-0001-8729-0482"
      ]
    }
  ]
}
```

## 3. Adding PIV-specific information

## 3. Describe PIV processing steps

We can describe our PIV measurement by using the `m4i:ProcessingStep` class. Processing steps can have sub-steps. The
first step is indicated by using the `starts with` key. The last step is indicated by using the `ends with` key. Each
sub-processing step indicates its "parent" processing step by using the `part of` key.

PIV processing steps can be broken down into two main steps:

1. PIV recording
2. PIV evaluation


- PIV recording (`local:piv_measurement`) [outputs raw images and background images]
- PIV evaluation
    - PIV pre processing (`local:piv_pre_processing`)
    - PIV evaluation / processing (`local:piv_processing`)
    - PIV post processing (`local:outlier_detection`) [outputs the PIV result data]

### 3.1 PIV measurement steps

Main processing step (1) will be named `local:piv_measurement`. For this example, we will register the following
sub-processing steps:

- Calibration step (`local:piv_calibration`)
- Background recording (`local:piv_background_recording`)
- PIV recording (`local:piv_recording`)

Each processing step may employ a tool or realizes a method. All steps employ the tool `local:camera` and the recording
step also employs `local:laser` and `local:DEHS` (the seeding can be understood as a tool).

We first write the coarse structure and then go into the details:

```json
[
  {
    "@id": "local:piv_measurement",
    "@type": "processing step",
    "has participant": "orcid:0000-0001-8729-0482",
    "start time": "2024-09-01T08:14:31",
    "end time": "2024-09-01T10:30:04",
    "starts with": "local:piv_calibration",
    "ends with": "local:piv_recording"
  },
  {
    "@id": "local:piv_calibration",
    "@type": "processing step",
    "part of": "local:piv_measurement",
    "has employed tool": "local:camera"
  },
  {
    "@id": "local:piv_background_recording",
    "@type": "processing step",
    "part of": "local:piv_background_computation",
    "has employed tool": [
      "local:camera",
      "local:laser"
    ]
  },
  {
    "@id": "local:piv_recording",
    "@type": "processing step",
    "part of": "local:piv_measurement",
    "has employed tool": [
      "local:camera",
      "local:laser",
      "local:DEHS"
    ],
    "has output": {
      "@id": "local:piv_background_images",
      "@type": "dataset",
      "has piv file distribution": {
        "download url": "file://path/to/images",
        "http://www.w3.org/ns/shacl#pattern": "Cam1A*[0-9].b16"
      }
    }
  }
]
```

#### Specifying background recording

```json
{
  "@id": "local:piv_background_recording",
  "@type": "processing step",
  "description": "The background image is recorded with the laser but without tracer particles",
  "part of": "local:piv_background_computation",
  "has employed tool": [
    "local:camera",
    "local:laser"
  ],
  "has output": {
    "@id": "local:piv_background_images",
    "@type": "dataset",
    "has output": [
      {
        "@id": "local:bgA",
        "@type": "dcat:Dataset",
        "dcterms:title": "Background image for image B",
        "dcterms:type": "pivm:BackgroundImage",
        "dcterms:format": "https://www.iana.org/assignments/media-types/image/tiff",
        "description": "Background image is intended to be subtracted of all PIV images",
        "has distribution": {
          "@id": "local:bgA_distribution",
          "@type": "distribution",
          "download url": "file://path/to/bgA.tiff",
          "has media type": "image/tiff"
        }
      },
      {
        "@id": "local:bgA",
        "@type": "dcat:Dataset",
        "dcterms:title": "Background image for image B",
        "dcterms:type": "pivm:BackgroundImage",
        "dcterms:format": "https://www.iana.org/assignments/media-types/image/tiff",
        "dcterms:description": "Background image is intended to be subtracted of all PIV images",
        "has distribution": {
          "@id": "local:bgA_distribution",
          "@type": "distribution",
          "download url": "file://path/to/bgB.tiff",
          "has media type": "image/tiff"
        }
      },
      {
      }
    ]
  }
}
```

### 3.2 PIV evaluation steps

The PIV evaluation comprises the steps performed by the PIV software. It outputs the PIV data files (.csv file, .nc file
or whatever the output file format of your PIV software is).

Irrespective of the PIV software, the PIV evaluation can be broken down into three steps:

1. PIV pre-processing (`local:piv_pre_processing`)
2. PIV processing (`local:piv_processing`)
3. PIV post-processing (`local:piv_post_processing`)

```json
{
  "@context": {
    ...,
    "@graph": [
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
      {
        "@id": "local:piv_pre_processing",
        "@type": "processing step",
        "has participant": "orcid:0000-0001-8729-0482",
        "starts with": "local:image_transformation"
      },
      {
        "@id": "local:image_transformation",
        "@type": "processing step",
        "realizes method": [
          "pivm#SplitImage",
          // Individual defined in ontology!
          "local:image_rotation",
          "pivm#FlipLeftRight",
          // Individual defined in ontology!
          "local:min_max_filter"
        ],
        "part of": "local:piv_pre_processing"
      },
      {
        "@id": "local:piv_image_filtering",
        "@type": "processing step",
        "realizes method": [
          "local:median_filter",
          "local:min_max_filter"
        ],
        "part of": "local:piv_pre_processing"
      },
      {
        "@id": "local:piv_processing",
        "@type": "processing step",
        "realizes method": [
          "local:interrogation_method",
          // single, multi-pass, multi-grid, ..., n_passses, ...
          "local:peak_search"
          // sub-pixel peak find method
        ]
      },
      {
        "@id": "local:outlier_detection",
        "@type": "processing step",
        "realizes method": [
          "local:normalized_median_test",
          // pre-defined method
          "local:Dynamic_mean_test"
          // pre-defined method
        ]
      }
    ]
  }
}
```

# DEPRECATED

### 3.1 Add PIV setup

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
background images) to the computational steps like image pre processing, performing the piv algorithm and the outlier
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

## Final processing step

```json
{
  "@context": {
    ...,
    "@graph": [
      {
        "@id": "local:piv_measurement",
        "@type": "processing step",
        "label": "File conversion",
        "has participant": "orcid:0000-0001-8729-0482",
        "has employed tool": {
          "@id": "https://doi.org/DOI_OF_SOFTWARE",
          "@type": "tool",
          "label": "piv2hdf",
          "description": "Converts the processed PIV files into a HDF5 file."
        }
      }
    ]
  }
}
```

The full JSON-LD file can be found [here]().