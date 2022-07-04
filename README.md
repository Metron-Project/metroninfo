# MetronInfo.xml

## What is it?

`MetronInfo.xml` is an attempt to create a new schema for digital comic books that fixes some of the problems with `ComicInfo.xml`.

## Rationale

The `ComicInfo.xml` schema was designed for the needs of ComicRack Application (which for all intents is a dead project), and supports a fairly limited amount of data. Some benefits of a new schema would include:

- Additional `Elements` for information. (eg. Price, Global Trade Item Numbers, Series Type, etc.)
- Better handling of data types. Instead of using delimited strings for list items, we can use Arrays of `Elements`. 
- Ability to identify where the data was obtained from. (eg. Comic Vine, Metron, Grand Comics Database, etc.)
- Add `ID` elements from the Information Source to resources (Characters, Creators, etc), so items with the same name are associated correctly if used in a Plex-like Comic Server.

Since Digital Comics are just are archive files (like .zip) this new XML schema can co-exist with any existing `ComicInfo.xml` if needed for backward compatibility.

## Where can I find the schemas?

Currently only a draft is available located in [drafts](./drafts)
