import io
from typing import Optional
import urllib.request
from rdkit import Chem
from rdkit import RDLogger
from tqdm.auto import tqdm
import zipfile

from .datasets import GeneratedDataset


class BindingDB(GeneratedDataset):
    SOURCE = "https://www.bindingdb.org/bind/downloads/BindingDB_All_3D_202402_sdf.zip"

    float_fields = {
        "Ki (nM)",
        "IC50 (nM)",
        "Kd (nM)",
        "EC50 (nM)",
        "kon (M-1-s-1)",
        "koff (s-1)",
    }

    def __init__(self, fd: Optional[io.BytesIO] = None):
        if fd is None:
            self.fd = self.from_url(self.SOURCE)
        else:
            self.fd = fd

    @staticmethod
    def _convert_to_numeric(prop_name: str, value: str):
        if prop_name in BindingDB.float_fields:
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
    def from_url(url: str) -> "BindingDB":
        with urllib.request.urlopen(url) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                sdf_name = z.namelist()[0]
                with z.open(sdf_name) as sdf_file:
                    sdf_content = io.BytesIO(sdf_file.read())
        return BindingDB(sdf_content)

    @staticmethod
    def from_uncompressed_file(file_path: str) -> "BindingDB":
        with open(file_path, "rb") as f:
            file_content = io.BytesIO(f.read())
        return BindingDB(file_content)

    def to_generator(self, progress_bar: bool = True):
        RDLogger.DisableLog("rdApp.*")  # Suppress RDKit warnings and errors

        sd = Chem.ForwardSDMolSupplier(self.fd, sanitize=False, removeHs=False)

        if progress_bar:
            pb = tqdm
        else:

            def pb(x, **kwargs):
                return x

        for mol in pb(sd, desc="Parsing BindingDB", unit=" molecule"):
            if mol is not None:
                record = {
                    prop: self._convert_to_numeric(prop, mol.GetProp(prop))
                    for prop in mol.GetPropNames()
                    if mol.HasProp(prop)
                }
                record["SMILES"] = Chem.MolToSmiles(mol)
                yield record

        # Re-enable logging
        RDLogger.EnableLog("rdApp.error")
        RDLogger.EnableLog("rdApp.warning")
