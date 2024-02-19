import os
from pathlib import Path
import polars as pl
from aiondata import BindingDB

current_file_dir = Path(__file__).resolve().parent
mock_sdf_path = current_file_dir / "mock.sdf"


def test_sdf_to_generator():
    """Test that the generator yields records with expected structure."""
    records = list(BindingDB(mock_sdf_path).to_generator())
    assert len(records) > 0, "No records generated."
    for record in records:
        assert "SMILES" in record, "SMILES not found in record."


def test_numeric_conversion():
    """Test that numeric fields are correctly converted."""
    records = list(BindingDB(mock_sdf_path).to_generator())
    for record in records:
        for key, value in record.items():
            if key in BindingDB.float_fields:
                assert (
                    isinstance(value, float) or value is None
                ), f"Field {key} is not a float or None."


def test_dataframe_creation():
    """Test that a DataFrame is correctly created from the SDF file."""
    df = BindingDB(mock_sdf_path).to_df()
    assert isinstance(df, pl.DataFrame), "DataFrame not created."
    assert df.height > 0, "DataFrame is empty."
    assert "SMILES" in df.columns, "SMILES column missing in DataFrame."
