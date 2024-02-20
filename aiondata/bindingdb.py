import os
from pathlib import Path
from typing import Iterable, Union
from rdkit import Chem
import polars as pl
from tqdm.auto import tqdm


class BindingDB:
    """BindingDB

    A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein considered to be drug-targets with small, drug-like molecules.
    """

    CACHE_DIR = (
        Path(os.environ.get("AIONDATA_CACHE", Path("~/.aiondata"))).expanduser()
        / "bindingdb"
    )

    float_fields = {
        "Ki (nM)",
        "IC50 (nM)",
        "Kd (nM)",
        "EC50 (nM)",
        "kon (M-1-s-1)",
        "koff (s-1)",
    }

    def __init__(self, sdf_file_path: os.PathLike):
        """Initializes a BindingDB object.

        Args:
            sdf_file_path (os.PathLike): The file path to the BindingDB SDF file.
        """
        self.sdf_file_path = sdf_file_path

    @staticmethod
    def _convert_to_numeric(prop_name: str, value: str) -> Union[int, float, None]:
        """Converts a string value to a numeric type if appropriate, or None for conversion failures.

        Args:
            prop_name (str): The name of the property.
            value (str): The string value to be converted.

        Returns:
            Union[int, float, None]: The converted numeric value or None if conversion fails.
        """
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

    def to_generator(self, progress_bar: bool = True) -> Iterable[dict]:
        """
        Returns a generator for the records in BindingDB.

        Args:
            progress_bar (bool, optional): Whether to display a progress bar. Defaults to True.

        Yields:
            dict: A dictionary representing a BindingDB record.
        """
        if progress_bar:
            pb = tqdm
        else:
            pb = lambda x, **kwargs: x
        suppl = Chem.SDMolSupplier(self.sdf_file_path)
        for mol in pb(suppl, desc="Parsing BindingDB", unit=" molecule"):
            if mol is not None:
                record = {
                    prop: BindingDB._convert_to_numeric(prop, mol.GetProp(prop))
                    for prop in mol.GetPropNames()
                }
                record["SMILES"] = Chem.MolToSmiles(mol)
                yield record

    def to_df(self) -> pl.DataFrame:
        """Converts an SDF file from BindingDB into a Polars DataFrame.

        Returns:
            polars.DataFrame: A DataFrame containing BindingDB data.
        """
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = self.CACHE_DIR / f"{Path(self.sdf_file_path).stem}.parquet"
        if cache_path.exists():
            return pl.read_parquet(cache_path)
        else:
            df = pl.DataFrame(self.to_generator(self.sdf_file_path))
            df.write_parquet(cache_path)
            return df
