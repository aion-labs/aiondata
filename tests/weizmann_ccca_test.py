from unittest.mock import patch

import polars as pl

from aiondata.weizmann_ccca import Weizmann3CA


@patch("polars.read_parquet")
def test_weizmann_3ca(read_parquet):
    read_parquet.return_value = pl.DataFrame(
        {"Study name": ["test_study"], "Data": ["https://test_link"]}
    )
    dataset = Weizmann3CA()
    try:
        dataset["foo"]
    except ValueError as e:
        assert "foo" in str(e)
