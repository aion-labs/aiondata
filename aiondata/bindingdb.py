from collections import OrderedDict
import io
from typing import Optional, Generator, Union, Tuple
import urllib.request
from rdkit import Chem
from rdkit import RDLogger
from tqdm.auto import tqdm
import zipfile

from .datasets import GeneratedDataset
import polars as pl


class BindingDB(GeneratedDataset):
    """BindingDB

    A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein considered to be drug-targets with small, drug-like molecules.
    """

    SOURCE = "https://www.bindingdb.org/bind/downloads/BindingDB_All_3D_202402_sdf.zip"
    COLLECTION = "bindingdb"
    SCHEMA = [
        # Primary Identifiers
        ("BindingDB Reactant_set_id", pl.Float64),
        ("BindingDB MonomerID", pl.Float64),
        ("BindingDB Entry DOI", pl.Utf8),
        # Target-related Fields
        ("Target Name", pl.Utf8),
        ("UniProt (SwissProt) Primary ID of Target Chain", pl.Utf8),
        ("UniProt (SwissProt) Secondary ID(s) of Target Chain", pl.Utf8),
        ("UniProt (SwissProt) Alternative ID(s) of Target Chain", pl.Utf8),
        ("UniProt (SwissProt) Recommended Name of Target Chain", pl.Utf8),
        ("UniProt (SwissProt) Entry Name of Target Chain", pl.Utf8),
        ("UniProt (TrEMBL) Primary ID of Target Chain", pl.Utf8),
        ("UniProt (TrEMBL) Secondary ID(s) of Target Chain", pl.Utf8),
        ("UniProt (TrEMBL) Alternative ID(s) of Target Chain", pl.Utf8),
        ("UniProt (TrEMBL) Submitted Name of Target Chain", pl.Utf8),
        ("UniProt (TrEMBL) Entry Name of Target Chain", pl.Utf8),
        ("Target Source Organism According to Curator or DataSource", pl.Utf8),
        ("BindingDB Target Chain Sequence", pl.Utf8),
        # Ligand-related Fields
        ("Ligand InChI", pl.Utf8),
        ("Ligand InChI Key", pl.Utf8),
        ("BindingDB Ligand Name", pl.Utf8),
        ("SMILES", pl.Utf8),
        ("PubChem CID of Ligand", pl.Float64),
        ("PubChem SID of Ligand", pl.Float64),
        ("ChEBI ID of Ligand", pl.Utf8),
        ("ChEMBL ID of Ligand", pl.Utf8),
        ("DrugBank ID of Ligand", pl.Utf8),
        ("IUPHAR_GRAC ID of Ligand", pl.Utf8),
        ("KEGG ID of Ligand", pl.Utf8),
        ("ZINC ID of Ligand", pl.Utf8),
        ("Ligand HET ID in PDB", pl.Utf8),
        ("PDB ID(s) for Ligand-Target Complex", pl.Utf8),
        ("PDB ID(s) of Target Chain", pl.Utf8),
        # Interaction and Binding Affinity Measurements
        ("Ki (nM)", pl.Float64),
        ("IC50 (nM)", pl.Float64),
        ("Kd (nM)", pl.Float64),
        ("EC50 (nM)", pl.Float64),
        ("kon (M-1-s-1)", pl.Float64),
        ("koff (s-1)", pl.Float64),
        # Experimental Conditions
        ("pH", pl.Float64),
        ("Temp C", pl.Float64),
        # Miscellaneous
        (
            "Number of Protein Chains in Target (bigger than 1 implies a multichain complex)",
            pl.Float64,
        ),
        # Links and References
        ("Link to Ligand in BindingDB", pl.Utf8),
        ("Link to Ligand-Target Pair in BindingDB", pl.Utf8),
        ("From", pl.Utf8),
        ("Curation/DataSource", pl.Utf8),
        ("Article DOI", pl.Utf8),
        ("PMID", pl.Utf8),
        ("PubChem AID", pl.Utf8),
        ("Patent Number", pl.Utf8),
        ("Authors", pl.Utf8),
        ("Institution", pl.Utf8),
    ]

    def __init__(self, fd: Optional[io.BufferedReader] = None):
        """
        Initializes a BindingDB instance.

        Args:
            fd (Optional[io.BufferedReader]): The file-like object containing the dataset content.
                If `fd` is not provided, the dataset content will be fetched from the default source.
        """
        if fd is None:
            cached_sdf = self.get_cache_path().parent / "BindingDB.sdf.zip"
            if cached_sdf.exists():
                self.outer_fd, self.fd = self.from_compressed_file(cached_sdf)
            else:
                self.outer_fd, self.fd = self.from_url(self.SOURCE)
        else:
            self.outer_fd, self.fd = fd

    def _convert_to_numeric(
        self, prop_name: str, value: str
    ) -> Union[int, float, str, None]:
        """
        Converts a property value to numeric type.

        Args:
            prop_name (str): The name of the property.
            value (str): The value of the property.

        Returns:
            The converted numeric value, or None if conversion fails.
        """

        float_fields = {
            name
            for name, dtype in self.SCHEMA
            if isinstance(dtype, (pl.Float64, pl.Float32))
        }
        if value == "":
            return None
        # Fudge numbers that are greater or less than a value
        if value[0] == ">":
            return float(value[1:]) * 1.01
        if value[0] == "<":
            return float(value[1:]) * 0.99
        if "NV" in value:
            return None
        if prop_name in float_fields:
            try:
                return float(value)
            except ValueError:
                return None
        else:
            try:
                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                else:
                    return float_value
            except ValueError:
                return value

    @staticmethod
    def from_url(url: str) -> Tuple[zipfile.ZipFile, io.BufferedReader]:
        """
        Creates a BindingDB instance from a URL containing a compressed SDF file, using streaming.

        Args:
            url (str): The URL of the dataset.

        Returns:
            A tuple containing the ZipFile instance and a BufferedReader instance containing the content of the SDF file.
        """
        response = urllib.request.urlopen(url)
        return BindingDB.from_compressed_file(io.BytesIO(response.read()))

    @staticmethod
    def from_compressed_file(
        file_path: str,
    ) -> Tuple[zipfile.ZipFile, io.BufferedReader]:
        """
        Creates a BindingDB instance from a compressed SDF file.

        Args:
            file_path (str): The path to the compressed file.

        Returns:
            A tuple containing the ZipFile instance and a BufferedReader instance containing the content of the SDF file.
        """
        zip_file = zipfile.ZipFile(file_path)
        sdf_name = zip_file.namelist()[0]
        sdf_file = zip_file.open(sdf_name)
        sdf_content = io.BufferedReader(sdf_file)
        return zip_file, sdf_content

    @staticmethod
    def from_uncompressed_file(file_path: str) -> io.BufferedReader:
        """
        Creates a BindingDB instance from an uncompressed SDF file.

        Args:
            file_path (str): The path to the uncompressed file.

        Returns:
            A BufferedReader instance containing the content of the SDF file.
        """
        return None, open(file_path, "rb")

    def to_generator(self, progress_bar: bool = True) -> Generator[dict, None, None]:
        """
        Converts the dataset to a generator.

        Args:
            progress_bar (bool): Whether to display a progress bar.

        Yields:
            dict: A dictionary representing a record in the dataset.
        """
        RDLogger.DisableLog("rdApp.*")  # Suppress RDKit warnings and errors

        if progress_bar:
            pb = tqdm
        else:

            def pb(x, **kwargs):
                return x

        with Chem.ForwardSDMolSupplier(self.fd, sanitize=True, removeHs=False) as sd:
            for mol in pb(sd, desc="Parsing BindingDB", unit=" molecules"):
                if mol is not None:
                    record = {
                        prop: self._convert_to_numeric(prop, mol.GetProp(prop))
                        for prop in mol.GetPropNames()
                        if mol.HasProp(prop)
                    }

                    # Normalize PubChem SID and CID fields that are sometimes present in the SDF
                    if "PubChem SID" in record:
                        record["PubChem SID of Ligand"] = record.pop("PubChem SID")
                    if "PubChem CID" in record:
                        record["PubChem CID of Ligand"] = record.pop("PubChem CID")

                    record["SMILES"] = Chem.MolToSmiles(mol)
                    yield record

        self.fd.close()
        if self.outer_fd is not None:
            self.outer_fd.close()

        # Re-enable logging
        RDLogger.EnableLog("rdApp.error")
        RDLogger.EnableLog("rdApp.warning")
