from pathlib import Path

import pytest
from xmlschema import XMLSchema11, XMLSchemaValidationError

TEST_XSD = Path(__file__).parent.parent / "schema" / "v1.0" / "MetronInfo.xsd"
TEST_FILES_PATH = Path(__file__).parent / "test_files" / "v1.0"


@pytest.mark.parametrize(
    ("xsd", "xml"),
    [
        (TEST_XSD, TEST_FILES_PATH / "valid.xml"),
        (
            TEST_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name></Series><Number /><PageCount>0</PageCount></MetronInfo>",
        ),
        (
            TEST_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name><Volume>0</Volume></Series><Number /></MetronInfo>",
        ),
    ],
    ids=["valid_xml", "zero_page_count", "volume_zero"],
)
def test_valid(xsd: Path, xml: Path | str) -> None:
    schema = XMLSchema11(xsd)
    schema.validate(xml)


@pytest.mark.parametrize(
    ("xsd", "xml"),
    [
        (TEST_XSD, TEST_FILES_PATH / "dup_primary_attr.xml"),
        (
            TEST_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name></Series><Number /><PageCount>-1</PageCount></MetronInfo>",
        ),
        (
            TEST_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name><Volume>-1</Volume></Series><Number /></MetronInfo>",
        ),
    ],
    ids=["dup_primary_attr_xml", "negative_page_count", "negative_volume"],
)
def test_invalid(xsd: Path, xml: Path | str) -> None:
    schema = XMLSchema11(xsd)
    with pytest.raises(XMLSchemaValidationError):
        schema.validate(xml)
