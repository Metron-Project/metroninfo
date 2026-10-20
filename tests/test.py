from pathlib import Path

import pytest
from xmlschema import XMLSchema11, XMLSchemaValidationError

TEST_V10_XSD = Path(__file__).parent.parent / "schema" / "v1.0" / "MetronInfo.xsd"
TEST_V11_XSD = Path(__file__).parent.parent / "schema" / "v1.1" / "MetronInfo.xsd"
TEST_V12_XSD = Path(__file__).parent.parent / "drafts" / "v1.2" / "MetronInfo.xsd"
TEST_FILES_PATH = Path(__file__).parent / "test_files" / "v1.0"


def _lang_xml(lang: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
        f'<Series lang="{lang}"><Name>Foo</Name></Series><Number /></MetronInfo>'
    )


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
        (TEST_V12_XSD, TEST_FILES_PATH / "valid.xml"),
        (TEST_V12_XSD, _lang_xml("en")),
        (TEST_V12_XSD, _lang_xml("fil")),
        (TEST_V12_XSD, _lang_xml("pt-br")),
        (TEST_V12_XSD, _lang_xml("pt-BR")),
        (TEST_V12_XSD, _lang_xml("zh-Hant")),
        (TEST_V12_XSD, _lang_xml("sr-latn")),
        (TEST_V12_XSD, _lang_xml("es-419")),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><StartYear>1970</StartYear><EndYear>1975</EndYear>"
                "<Status>Completed</Status><Summary>Foo series summary.</Summary></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><StartYear>2020</StartYear><Status>Ongoing</Status></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Status>Cancelled</Status></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Status>Hiatus</Status></Series><Number />"
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
        "v12_valid_xml",
        "v12_lang_en",
        "v12_lang_fil",
        "v12_lang_pt_br",
        "v12_lang_pt_BR",
        "v12_lang_zh_Hant",
        "v12_lang_sr_latn",
        "v12_lang_es_419",
        "v12_series_end_year_status_summary",
        "v12_series_status_ongoing",
        "v12_series_status_cancelled",
        "v12_series_status_hiatus",
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
        (TEST_V11_XSD, _lang_xml("pt-br")),
        (TEST_V12_XSD, _lang_xml("e")),
        (TEST_V12_XSD, _lang_xml("english")),
        (TEST_V12_XSD, _lang_xml("en_US")),
        (TEST_V12_XSD, _lang_xml("en-")),
        (TEST_V12_XSD, _lang_xml("pt--br")),
        (TEST_V12_XSD, TEST_FILES_PATH / "dup_primary_attr.xml"),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Status>Unknown</Status></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Status>ongoing</Status></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><EndYear>75</EndYear></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V12_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><Summary>Foo</Summary><Summary>Bar</Summary></Series><Number />"
                "</MetronInfo>",
        ),
        (
                TEST_V11_XSD,
                '<?xml version="1.0" encoding="UTF-8"?><MetronInfo>'
                "<Series><Name>Foo</Name><EndYear>1975</EndYear></Series><Number />"
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
        "v11_lang_region_rejected",
        "v12_lang_e",
        "v12_lang_english",
        "v12_lang_underscore",
        "v12_lang_trailing_dash",
        "v12_lang_empty_subtag",
        "v12_dup_primary_attr_xml",
        "v12_series_status_unknown",
        "v12_series_status_lowercase",
        "v12_series_end_year_two_digit",
        "v12_series_duplicate_summary",
        "v11_series_end_year_not_in_v11",
    ],
)
def test_invalid(xsd: Path, xml: Path | str) -> None:
    schema = XMLSchema11(xsd)
    with pytest.raises(XMLSchemaValidationError):
        schema.validate(xml)
