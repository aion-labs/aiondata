#set current directory to the parent directory

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append('..')

import pypdb 
from aiondata import PDBHandler
import unittest
from unittest import mock
from unittest.mock import patch
import pypdb.clients.search.search_client





class TestPDBHandler(unittest.TestCase):

    def setUp(self):
        self.pdb_handler = PDBHandler()

    def test_get_pdb(self):
        pdb_ids = ['8IRB', '100D']
        with patch.object(self.pdb_handler.pdb_list, 'retrieve_pdb_file') as mock_retrieve_pdb_file:
            self.pdb_handler.get_pdb(pdb_ids)
            mock_retrieve_pdb_file.assert_any_call(pdb_ids[0], pdir=self.pdb_handler.save_dir, file_format='pdb')
            mock_retrieve_pdb_file.assert_any_call(pdb_ids[1], pdir=self.pdb_handler.save_dir, file_format='pdb')


    def test_get_pdb_info(self):
        pdb_id = '4OS0'
        with patch.object(pypdb, 'get_all_info') as mock_get_all_info:
            self.pdb_handler.get_pdb_info(pdb_id)
            mock_get_all_info.assert_called_with(pdb_id)


    def test_searchpdb(self):
        title = 'Solution'
        organism = '9606'
        Uniprot_accession = "P04637"
        fromdb = "UniProt"
        nonpolymer = 1
        ComparisonType = "Less"

        with patch('pypdb.clients.search.search_client.perform_search_with_graph') as mock_perform_search_with_graph:
                self.pdb_handler.searchpdb(title=title,
                                        organism=organism,
                                        Uniprot_accession=Uniprot_accession,
                                        fromdb=fromdb,
                                        nonpolymer=nonpolymer,
                                        ComparisonType=ComparisonType
                                        )
                mock_perform_search_with_graph.assert_called()
                #self.assertTrue(mock_perform_search_with_graph.called, "The perform_search_with_graph function was not called")
                #mock_perform_search_with_graph.assert_called_with(query_object=mock.ANY, return_type=mock.ANY)



if __name__ == '__main__':
    unittest.main()

