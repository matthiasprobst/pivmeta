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
    ...
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
      "@type": "person",
      "has ORCID Id": "0000-0001-8729-0482",
      "firstName": "John",
      "lastName": "Doe",
      "role": "contact person",
      "affiliation": {
        "@id": "local:myInstitution",
        "@type": "Organization",
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


## Defining Flag-Schemes

Below, a canonical flag scheme for PIV results is defined. It uses a bitwise scheme where flags are combined via bitwise
OR and individual flags can be recovered via bitwise AND with each flag's mask.

This is a common scheme in PIV post-processing to indicate the status of individual vectors in a PIV result field.

```Turtle
@prefix piv: <http://purl.org/pivmeta/ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .


piv:DefaultBitwiseFlagScheme
  a piv:FlagScheme ;
  skos:prefLabel "Default PIV bitwise flag scheme"@en ;
  skos:definition "Canonical PIV bitmask scheme: flags combine via bitwise OR; atoms recovered via bitwise AND with each mask."@en ;
  piv:usesFlagSchemeType piv:BitwiseFlagScheme ;

  # declare the allowed atomic flags
  piv:allowedFlag
    piv:FlagInactive,
    piv:FlagActive,
    piv:FlagMasked,
    piv:FlagNoResult,
    piv:FlagDisabled,
    piv:FlagFiltered,
    piv:FlagInterpolated,
    piv:FlagReplaced,
    piv:FlagManualEdit ;

  # explicit value→atom mappings (handy for simple lookups / enumerated readers)
  piv:hasFlagMapping
    [ a piv:FlagMapping ; piv:value 0   ; piv:mapsToFlag piv:FlagInactive     ],
    [ a piv:FlagMapping ; piv:value 1   ; piv:mapsToFlag piv:FlagActive       ],
    [ a piv:FlagMapping ; piv:value 2   ; piv:mapsToFlag piv:FlagMasked       ],
    [ a piv:FlagMapping ; piv:value 4   ; piv:mapsToFlag piv:FlagNoResult     ],
    [ a piv:FlagMapping ; piv:value 8   ; piv:mapsToFlag piv:FlagDisabled     ],
    [ a piv:FlagMapping ; piv:value 16  ; piv:mapsToFlag piv:FlagFiltered     ],
    [ a piv:FlagMapping ; piv:value 32  ; piv:mapsToFlag piv:FlagInterpolated ],
    [ a piv:FlagMapping ; piv:value 64  ; piv:mapsToFlag piv:FlagReplaced     ],
    [ a piv:FlagMapping ; piv:value 128 ; piv:mapsToFlag piv:FlagManualEdit   ] .
```
