import urllib.request
import zipfile
import io
import polars as pl
from scipy.io import mmread

from .datasets import ParquetDataset


class Weizmann3CA(ParquetDataset):
    """Curated Cancer Cell Atlas of collected, annotated and analyzed cancer scRNA-seq datasets from the Weizmann Institute of Science."""

    COLLECTION = "weizmann_ccca"
    SOURCE = "https://raw.githubusercontent.com/aion-labs/aiondata/main/data/3ca_links.parquet"

    def __getitem__(self, study_name_to_find: str):
        links = self.to_df()
        row = links.filter(pl.col("Study name") == study_name_to_find)
        if row.height == 0:
            raise ValueError(
                f"Study name {study_name_to_find} not found in the dataset."
            )
