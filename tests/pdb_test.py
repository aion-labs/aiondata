# Import necessary modules
import pytest
from unittest.mock import patch
import pypdb
from aiondata import PDBHandler


@pytest.fixture
def pdb_handler():
    return PDBHandler()


def test_get_pdb(pdb_handler):
    """Test that the PDB files are retrieved."""
    pdb_ids = ["8IRB", "100D"]
    with patch.object(
        pdb_handler.pdb_list, "retrieve_pdb_file"
    ) as mock_retrieve_pdb_file:
        pdb_handler.get_pdb(pdb_ids)
        mock_retrieve_pdb_file.assert_any_call(
            pdb_ids[0], pdir=pdb_handler.save_dir, file_format="pdb"
        )
        mock_retrieve_pdb_file.assert_any_call(
            pdb_ids[1], pdir=pdb_handler.save_dir, file_format="pdb"
        )


def test_get_pdb_info(pdb_handler):
    """Test that the information about a PDB file is retrieved."""
    pdb_id = "4OS0"
    with patch.object(pypdb, "get_all_info") as mock_get_all_info:
        pdb_handler.get_pdb_info(pdb_id)
        mock_get_all_info.assert_called_with(pdb_id)


def test_searchpdb(pdb_handler):
    """Test that the PDB files are searched for."""
    title = "Solution"
    organism = "9606"
    Uniprot_accession = "P04637"
    fromdb = "UniProt"
    nonpolymer = 1
    ComparisonType = "Less"
    with patch(
        "aiondata.protein_structure.perform_search_with_graph"
    ) as mock_perform_search_with_graph:
        pdb_handler.searchpdb(
            title=title,
            organism=organism,
            Uniprot_accession=Uniprot_accession,
            fromdb=fromdb,
            nonpolymer=nonpolymer,
            ComparisonType=ComparisonType,
        )
        mock_perform_search_with_graph.assert_called()
