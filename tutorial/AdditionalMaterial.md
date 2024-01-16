# Additional Material

## File Formats

Datasets are specified using [dcat:Distribution](https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution). If possible,
the file format should be selected from
the [IANA Media Type Registry](https://www.iana.org/assignments/media-types/media-types.xhtml) and specified
by [dcat:mediaType](https://www.w3.org/TR/vocab-dcat-2/#Property:distribution_media_type). If the file type is not
listed in the registry, the file format can be specified
using [m4i:format](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#format) with a string value.

Here are typical PIV file formats:

```json
{
  "@context": {
    "iana": "https://www.iana.org/assignments/media-types/"
  },
  "b16": "iana:image/vnd.pco.b16",
  "tiff": "iana:image/tiff",
  "bmp": "iana:image/bmp",
  "csv": "iana:text/csv",
  "zip": "iana:application/zip"
}
```