import urllib.request
import zipfile
import io
import polars as pl
from scipy.io import mmread

from .datasets import ParquetDataset


class Weizman3CA(ParquetDataset):
    COLLECTION = "weizmann_ccca"
    SOURCE = "https://raw.githubusercontent.com/aion-labs/aiondata/main/data/3ca_links.parquet"
