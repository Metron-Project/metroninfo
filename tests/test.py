from pathlib import Path

import pytest
from xmlschema import XMLSchema11, XMLSchemaValidationError

TEST_V10_XSD = Path(__file__).parent.parent / "schema" / "v1.0" / "MetronInfo.xsd"
TEST_V11_XSD = Path(__file__).parent.parent / "drafts" / "v1.1" / "MetronInfo.xsd"
TEST_FILES_PATH = Path(__file__).parent / "test_files" / "v1.0"


@pytest.mark.parametrize(
    ("xsd", "xml"),
    [
        (TEST_V10_XSD, TEST_FILES_PATH / "valid.xml"),
        (
                TEST_V10_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name></Series><Number /><PageCount>0</PageCount></MetronInfo>",
        ),
        (
                TEST_V10_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name><Volume>0</Volume></Series><Number /></MetronInfo>",
        ),
        (TEST_V11_XSD, TEST_FILES_PATH / "valid.xml"),
        (
                TEST_V10_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number /><PageCount>0</PageCount></MetronInfo>",
        ),
        (
                TEST_V10_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Volume>0</Volume></Series><Number /></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number>1</Number>"
                "<AlternativeNumber>1A</AlternativeNumber><PageCount>0</PageCount></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number>1</Number><PageCount>0</PageCount></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>4.5</AverageRating><RatingCount>1250</RatingCount></CommunityRating>"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>0</AverageRating></CommunityRating>"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>5.0</AverageRating></CommunityRating>"
                "</MetronInfo>",
        ),
    ],
    ids=[
        "valid_xml",
        "zero_page_count",
        "volume_zero",
        "v11_valid_xml",
        "v11_zero_page_count",
        "v11_volume_zero",
        "v11_alternative_number",
        "v11_alternative_number_absent",
        "v11_community_rating",
        "v11_community_rating_min",
        "v11_community_rating_max",
    ],
)
def test_valid(xsd: Path, xml: Path | str) -> None:
    schema = XMLSchema11(xsd)
    schema.validate(xml)


@pytest.mark.parametrize(
    ("xsd", "xml"),
    [
        (TEST_V10_XSD, TEST_FILES_PATH / "dup_primary_attr.xml"),
        (
                TEST_V10_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name></Series><Number /><PageCount>-1</PageCount></MetronInfo>",
        ),
        (
                TEST_V10_XSD,
            '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
            "<Series><Name>Foo</Name><Volume>-1</Volume></Series><Number /></MetronInfo>",
        ),
        (TEST_V11_XSD, TEST_FILES_PATH / "dup_primary_attr.xml"),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number /><PageCount>-1</PageCount></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Volume>-1</Volume></Series><Number /></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number>1</Number>"
                "<AlternativeNumber>1A</AlternativeNumber><AlternativeNumber>1B</AlternativeNumber></MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>5.1</AverageRating></CommunityRating>"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>-0.1</AverageRating></CommunityRating>"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><RatingCount>100</RatingCount></CommunityRating>"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name></Series><Number />"
                "<CommunityRating><AverageRating>4.5</AverageRating><RatingCount>0</RatingCount></CommunityRating>"
                "</MetronInfo>",
        ),
    ],
    ids=[
        "dup_primary_attr_xml",
        "negative_page_count",
        "negative_volume",
        "v11_dup_primary_attr_xml",
        "v11_negative_page_count",
        "v11_negative_volume",
        "v11_duplicate_alternative_number",
        "v11_community_rating_too_high",
        "v11_community_rating_negative",
        "v11_community_rating_missing_average",
        "v11_community_rating_zero_count",
    ],
)
def test_invalid(xsd: Path, xml: Path | str) -> None:
    schema = XMLSchema11(xsd)
    with pytest.raises(XMLSchemaValidationError):
        schema.validate(xml)
