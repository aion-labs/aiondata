import pytest
from unittest.mock import patch
import polars as pl
from aiondata import (
    Tox21,
    ToxCast,
    ESOL,
    FreeSolv,
    Lipophilicity,
    QM7,
    QM8,
    QM9,
    MUV,
    HIV,
    BACE,
    BBBP,
    SIDER,
    ClinTox,
    FoldswitchProteinsTableS1A,
    FoldswitchProteinsTableS1B,
    FoldswitchProteinsTableS1C,
    CodNas91,
    Weizmann3CA,
)

# List of dataset classes
datasets = [
    Tox21,
    ToxCast,
    ESOL,
    FreeSolv,
    Lipophilicity,
    QM7,
    QM8,
    QM9,
    MUV,
    HIV,
    BACE,
    BBBP,
    SIDER,
    ClinTox,
    FoldswitchProteinsTableS1A,
    FoldswitchProteinsTableS1B,
    FoldswitchProteinsTableS1C,
    CodNas91,
    Weizmann3CA,
]


@pytest.mark.parametrize("dataset_cls", datasets)
@patch("pathlib.Path.mkdir")
@patch("polars.DataFrame.write_parquet")
@patch("pathlib.Path.exists")
@patch("polars.read_csv")
@patch("polars.read_excel")
@patch("polars.read_parquet")
def test_dataframe_loading_without_cache(
    mock_read_parquet,
    mock_read_excel,
    mock_read_csv,
    mock_exists,
    mock_write_parquet,
    mock_mkdir,
    dataset_cls,
):
    """Test that the to_df method correctly loads a dataset into a DataFrame without using the cache."""
    mock_df = pl.DataFrame({"smiles": ["CCO", "NCCO"], "label": [0, 1]})
    mock_exists.return_value = False
    mock_read_csv.return_value = mock_df
    mock_read_excel.return_value = mock_df
    mock_read_parquet.return_value = mock_df

    dataset_instance = dataset_cls()
    df = dataset_instance.to_df()

    csv_called_correctly = (
        mock_read_csv.call_args is not None
        and mock_read_csv.call_args[0][0] == dataset_instance.SOURCE
    )
    excel_called_correctly = (
        mock_read_excel.call_args is not None
        and mock_read_excel.call_args[0][0] == dataset_instance.SOURCE
    )
    parquet_called_correctly = (
        mock_read_parquet.call_args is not None
        and mock_read_parquet.call_args[0][0] == dataset_instance.SOURCE
    )

    assert (
        csv_called_correctly or excel_called_correctly or parquet_called_correctly
    ), "Either CSV, Parquet or Excel read method should be called with the dataset source."

    assert isinstance(df, pl.DataFrame), "The method should return a Polars DataFrame."
    assert len(df) > 0, "DataFrame should not be empty."
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    dataset_name = dataset_cls.__name__.lower()
    assert (
        mock_write_parquet.called
    ), "The DataFrame should be written to a parquet file."
    assert str(mock_write_parquet.call_args.args[0]).endswith(
        f"{dataset_name}.parquet"
    ), f"The parquet file for {dataset_name} should be written to the cache directory with the correct name."
    assert dataset_name in str(
        mock_write_parquet.call_args.args[0]
    ), f"The parquet file for {dataset_name} should be written to the cache directory."
    assert (
        mock_read_parquet.call_args is not None
        and mock_read_parquet.call_args[0][0] == dataset_instance.SOURCE
        or not mock_read_parquet.called
    ), "The DataFrame should not be read from the cache file."


@pytest.mark.parametrize("dataset_cls", datasets)
@patch("pathlib.Path.mkdir")
@patch("polars.DataFrame.write_parquet")
@patch("pathlib.Path.exists")
@patch("polars.read_csv")
@patch("polars.read_parquet")
def test_dataframe_loading_with_cache(
    mock_read_parquet,
    mock_read_csv,
    mock_exists,
    mock_write_parquet,
    mock_mkdir,
    dataset_cls,
):
    """Test that the to_df method correctly loads a dataset into a DataFrame using the cache."""

    dataset_instance = dataset_cls()
    dataset_name = dataset_cls.__name__.lower()

    mock_exists.return_value = True
    mock_read_parquet.return_value = pl.DataFrame(
        {"smiles": ["CCO", "NCCO"], "label": [0, 1]}
    )

    df = dataset_instance.to_df()

    assert (
        not mock_read_csv.called
    ), "The method should not read the CSV file if the cache file exists."
    assert isinstance(df, pl.DataFrame), "The method should return a Polars DataFrame."
    assert len(df) > 0, "DataFrame should not be empty."
    assert (
        not mock_write_parquet.called
    ), "The DataFrame should not be written to a parquet file if the cache file exists."
    assert mock_read_parquet.called, "The DataFrame should be read from the cache file."
    assert str(mock_read_parquet.call_args.args[0]).endswith(
        f"{dataset_name}.parquet"
    ), f"The parquet file for {dataset_name} should be read from the cache directory with the correct name."
