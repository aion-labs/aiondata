import os
from pathlib import Path
from unittest.mock import patch
import polars as pl
from aiondata import BindingDB
from aiondata import BindingAffinity

current_file_dir = Path(__file__).resolve().parent
mock_sdf_path = current_file_dir / "mock.sdf"


def test_sdf_to_generator():
    """Test that the generator yields records with expected structure."""
    bindingdb = BindingDB(BindingDB.from_uncompressed_file(mock_sdf_path))

    records = list(bindingdb.to_generator())
    assert len(records) > 0, "No records generated."
    for record in records:
        assert "SMILES" in record, "SMILES not found in record."


def test_numeric_conversion():
    """Test that numeric fields are correctly converted."""
    records = list(
        BindingDB(BindingDB.from_uncompressed_file(mock_sdf_path)).to_generator()
    )
    float_fields = {
        name
        for name, dtype in BindingDB.SCHEMA
        if isinstance(dtype, (pl.Float64, pl.Float32))
    }
    for record in records:
        for key, value in record.items():
            if key in float_fields:
                assert (
                    isinstance(value, float) or value is None
                ), f"Field {key} is not a float or None."


@patch("pathlib.Path.mkdir")
@patch("pathlib.Path.exists")
@patch("polars.DataFrame.write_parquet")
def test_dataframe_no_cache(mock_write_parquet, mock_exists, mock_mkdir):
    """Test that a DataFrame is created and cached."""
    mock_exists.return_value = False

    df = BindingDB(BindingDB.from_uncompressed_file(mock_sdf_path)).to_df()

    assert isinstance(df, pl.DataFrame), "DataFrame not created."
    assert df.height > 0, "DataFrame is empty."
    assert "SMILES" in df.columns, "SMILES column missing in DataFrame."
    mock_mkdir.assert_called_with(parents=True, exist_ok=True)
    mock_write_parquet.assert_called_once()


@patch("pathlib.Path.mkdir")
@patch("polars.DataFrame.write_parquet")
@patch("pathlib.Path.exists")
@patch("polars.read_parquet")
def test_dataframe_creation_from_cache(
    mock_read_parquet, mock_exists, mock_write_parquet, mock_mkdir
):
    """Test that a DataFrame is created from cache."""
    mock_exists.return_value = True
    mock_df = pl.DataFrame({"SMILES": ["C"], "Ki (nM)": [1.0]})
    mock_read_parquet.return_value = mock_df

    df = BindingDB(BindingDB.from_uncompressed_file(mock_sdf_path)).to_df()

    assert isinstance(df, pl.DataFrame), "DataFrame not created from cache."
    assert df.height > 0, "DataFrame is empty."
    assert "SMILES" in df.columns, "SMILES column missing in DataFrame."
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_write_parquet.assert_not_called()
    mock_read_parquet.assert_called_once()
    assert df.frame_equal(
        mock_df
    ), "DataFrame content does not match expected mock DataFrame."


@patch("pathlib.Path.mkdir")
@patch("polars.DataFrame.write_parquet")
@patch("pathlib.Path.exists")
def test_bindingaffinity(mock_exists, mock_write_parquet, mock_mkdir):
    """Test that the BindingAffinity dataset is correctly created."""
    mock_exists.return_value = False
    df = BindingAffinity(BindingDB.from_uncompressed_file(mock_sdf_path)).get_df()
    assert isinstance(df, pl.DataFrame), "DataFrame not created."
    assert df.height > 0, "DataFrame is empty."
    assert "SMILES" in df.columns, "SMILES column missing in DataFrame."
    assert "Sequence" in df.columns, "Sequence column missing in DataFrame."
