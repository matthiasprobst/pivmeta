# Describe a PIV dataset

The following describes one of the datasets from the PIV Challenge.

We use

- `dcat:Dataset` to describe the dataset
- `dcat:Distribution` to describe the files of the dataset
- `prov:Person` to describe the contact person

```json
{
    "@context": {
        "@import": "https://raw.githubusercontent.com/matthiasprobst/pivmeta/main/pivmeta_context.jsonld"
    },
    "@graph": [
        {
            "@id": "https://local-domain.org/dcac9b6b-6c06-4519-becd-3a9bfea4724a",
            "@type": "distribution",
            "dct:title": "ReadMe file",
            "download URL": "https://www.pivchallenge.org/pub/E/readmeE.txt"
        },
        {
            "@id": "https://local-domain.org/1f7f6b25-efaf-48ae-82c4-913b3d564594",
            "@type": "piv mask distribution",
            "dct:title": "mask data",
            "download URL": "https://www.pivchallenge.org/pub/C/C.zip",
            "filenamePattern": "^Cmask_1.tif$",
            "media type": "https://www.iana.org/assignments/media-types/application/zip"
        },
        {
            "@id": "https://local-domain.org/ec5ba6c6-cb77-4a48-a42b-c247c646d444",
            "@type": "person",
            "foaf:lastName": "Okamoto",
            "foaf:mbox": "okamoto@tokai.t.u-tokyo.ac.jp"
        },
        {
            "@id": "https://local-domain.org/e51651a9-3a72-4c78-8789-c821d7efccb4",
            "@type": "dataset",
            "dcat:landingPage": "https://www.pivchallenge.org/pub/index.html#c",
            "dct:creator": {
                "@id": "https://local-domain.org/ec5ba6c6-cb77-4a48-a42b-c247c646d444"
            },
            "dct:description": "Different velocity gradients with spatially varying image quality (provided by Okamoto) < synthetic > [256 x 128]",
            "dct:modified": "2000-10-28T00:00:00",
            "dct:title": "piv-challenge-1-C",
            "hat Verteilung": [
                {
                    "@id": "https://local-domain.org/08bf37d1-6b0a-4ce8-aafb-b7510d06c052"
                },
                {
                    "@id": "https://local-domain.org/1f7f6b25-efaf-48ae-82c4-913b3d564594"
                },
                {
                    "@id": "https://local-domain.org/dcac9b6b-6c06-4519-becd-3a9bfea4724a"
                }
            ]
        },
        {
            "@id": "https://local-domain.org/08bf37d1-6b0a-4ce8-aafb-b7510d06c052",
            "@type": "piv image distribution",
            "dct:title": "raw piv image data",
            "download URL": "https://www.pivchallenge.org/pub/C/C.zip",
            "filenamePattern": "^C\\d{3}_\\d.tif$",
            "imageBitDepth": "8",
            "media type": "https://www.iana.org/assignments/media-types/application/zip",
            "numberOfRecords": "1",
            "pivImageType": "https://matthiasprobst.github.io/pivmeta#SyntheticImage"
        }
    ]
}
```