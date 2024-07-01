import pytest
from unittest.mock import MagicMock
import gzip

from aiondata import UniProt

# Example data for the tests
example_gzip_data = """\
ID   Example_ID     STANDARD;      PRT;   123 AA.
AC   P12345;
DT   01-JAN-2000, integrated into UniProtKB/Swiss-Prot.
DE   RecName: Full=Example protein;
GN   Name=Gene;
OS   Homo sapiens (Human);
OX   NCBI_TaxID=9606;
OH   NCBI_TaxID=12345;
CC   -!- FUNCTION: [Includes]: Function 1.
DR   Database1; P12345; Entry1.
PE   1: Evidence at protein level;
KW   Keyword1; Keyword2;
FT   CHAIN         1    123       Example chain.
//
ID   Example_ID2    STANDARD;      PRT;   234 AA.
AC   P67890;
DT   02-FEB-2001, integrated into UniProtKB/Swiss-Prot.
DE   RecName: Full=Another Example protein;
GN   Name=AnotherGene;
OS   Mus musculus (Mouse);
OX   NCBI_TaxID=10090;
OH   NCBI_TaxID=67890;
CC   -!- FUNCTION: [Includes]: Function 2.
DR   Database2; P67890; Entry2.
PE   1: Evidence at protein level;
KW   Keyword3; Keyword4;
FT   CHAIN         1    234       Another Example chain.
//"""


@pytest.fixture
def mock_urlopen(mocker):
    # Create a mock object for urllib.request.urlopen
    mock = mocker.patch("urllib.request.urlopen")
    mock_response = MagicMock()
    mock_response.read.return_value = gzip.compress(example_gzip_data.encode("utf-8"))
    mock.return_value.__enter__.return_value = mock_response
    return mock


def test_to_generator_successful(mock_urlopen):
    uni_prot = UniProt()
    results = list(uni_prot.to_generator())

    assert len(results) == 2
    assert (
        results[0]["Entry Identifier"] == "Example_ID     STANDARD;      PRT;   123 AA."
    )


def test_to_generator_network_failure(mocker):
    mocker.patch("urllib.request.urlopen", side_effect=Exception("Network failure"))

    uni_prot = UniProt()

    with pytest.raises(Exception) as exc_info:
        list(uni_prot.to_generator())

    assert "Network failure" in str(exc_info.value)
