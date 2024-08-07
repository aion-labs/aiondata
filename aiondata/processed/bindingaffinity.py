import io
from typing import Optional

import polars as pl

from ..datasets import CachedDataset
from ..raw.bindingdb import BindingDB


class BindingAffinity(CachedDataset):
    COLLECTION = "processed"

    def __init__(self, fd: Optional[io.BufferedReader] = None):
        """
        Initializes a BindingAffinity instance.

        Args:
            fd (Optional[io.BufferedReader]): The file-like object containing the BindingDB content.
                If `fd` is not provided, the dataset content will be fetched from the default source.
        """
        self.bindingdb = BindingDB(fd)

    def get_df(self) -> pl.DataFrame:
        bindingdb = self.bindingdb.to_df()

        ba_df = bindingdb.select(
            [
                "SMILES",
                "BindingDB Target Chain Sequence",
                "Ki (nM)",
                "IC50 (nM)",
                "Kd (nM)",
                "EC50 (nM)",
                "pH",
                "Temp C",
                "Target Source Organism According to Curator or DataSource",
                "Curation/DataSource",
            ]
        )
        ba_df = ba_df.rename(
            {
                "BindingDB Target Chain Sequence": "Sequence",
                "Target Source Organism According to Curator or DataSource": "Organism",
                "Curation/DataSource": "Source",
            }
        )

        # Filter out rows with Sequences that are not valid
        ba_df = ba_df.filter(
            pl.col("Sequence").str.contains("^[ACDEFGHIKLMNPQRSTVWY]+$")
        )

        # Remove spaces from BindingDB Target Chain Sequence column
        ba_df = ba_df.with_columns(pl.col("Sequence").str.replace_all(" ", ""))

        return ba_df
