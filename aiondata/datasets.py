import os
from pathlib import Path
import polars as pl


class CachedDataset:
    """A base class for datasets that are cached locally."""

    CACHE_DIR = (
        Path(os.environ.get("AIONDATA_CACHE", Path("~/.aiondata"))).expanduser()
        / "moleculenet"
    )

    def to_df(self) -> pl.DataFrame:
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        dataset_name = self.__class__.__name__.lower()
        cache_path = self.CACHE_DIR / f"{dataset_name}.parquet"
        if cache_path.exists():
            return pl.read_parquet(cache_path)
        else:
            df = self.get_df()
            df.write_parquet(cache_path)
            return df


class CsvDataset(CachedDataset):
    """A base class for datasets that are stored in CSV format."""

    def get_df(self) -> pl.DataFrame:
        return pl.read_csv(self.SOURCE)


class ExcelData(CachedDataset):
    """A base class for datasets that are stored in Excel format."""

    def get_df(self) -> pl.DataFrame:
        return pl.read_excel(self.SOURCE)
