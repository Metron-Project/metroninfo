# MetronInfo.xml

## What is it?

`MetronInfo.xml` is an attempt to create a new schema for digital comic books that fixes some of the deficiencies that
exist with the `ComicInfo.xml` schema.

## Rationale

The `ComicInfo.xml` schema was designed for the needs of ComicRack Application (which for all intents is a dead
project), and supports a fairly limited amount of data. Some benefits of a new schema would include:

- Additional `Elements` for information. (e.g. Price, Global Trade Item Numbers, Series Type, etc.)
- Better handling of data types. Instead of using delimited strings for list items, we can use Arrays of `Elements`.
- Ability to identify where the data was obtained from. (e.g. Comic Vine, Metron, Grand Comics Database, etc.)
- Add `ID` elements from the Information Source to resources (Characters, Creators, etc.), so items with the same name
  are associated correctly if used in a Plex-like Comic Server.

Since Digital Comics are just are archive files (like .zip) this new XML schema can co-exist with any existing
`ComicInfo.xml` if needed for backward compatibility.

## Is the schema only for the Metron Database?

No, the schema only has *Metron* in the name since almost every other format has *Comic* in the name, and the
originating author hates naming projects, so he went with the simplest choice. 😄 It was designed to be used for any of
the comic resources (Comic Vine, AniList, etc.)

## Where can I find the schemas?

Version 1.0 of the schema is located in [schema](./schema) directory

## Is there documentation for it?

Yes, there is [documentation](https://metron-project.github.io/docs/category/metroninfo) describing the elements usage
and also a Matrix to help with age rating mapping.

## How can I validate my XML?

It's recommended that any software that writes the XML make use of the schema to validate, so consumers of the XML
document can be sure of its data. The schema use XSD 1.1, so you need to make sure your validation code uses that
instead of XSD 1.0.

For example to validate the XML in python:

```python
from pathlib import Path
from xmlschema import XMLSchema11, XMLSchemaValidationError

xsd = Path("/home/user/MetronInfo.xsd")
xml = Path("/home/user/MetronInfo.xml")

schema = XMLSchema11(xsd)
try:
    schema.validate(xml)
except XMLSchemaValidationError as e:
    print(f"Failed to validate XML: {e!r}")
    exit(1)

# Code to write / read the xml file
```

## What software currently supports it?

Currently, the following software does:

- [Metron-Tagger](https://github.com/Metron-Project/metron-tagger) - Commandline tool to tag comic with metadata from
  Metron Comic Book Database.

If you are a developer that has added support for MetronInfo.xml to your software, please create a PR to update the
README
or [contact me](mailto:bpepple@metron.cloud?subject=MetronInfo%20Support&body=Please%20add%20the%20following%20software%20to%the%20README:%20).