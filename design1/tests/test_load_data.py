"""Tests for data loading functions."""
import pandas as pd
import pytest

from load_data import load_co2


def test_load_co2_returns_dataframe(co2_csv_path):
    df = load_co2(co2_csv_path)
    assert isinstance(df, pd.DataFrame)


def test_load_co2_columns(co2_csv_path):
    df = load_co2(co2_csv_path)
    assert list(df.columns) == ["year", "co2_mean", "co2_unc"]


def test_load_co2_year_range(co2_csv_path):
    df = load_co2(co2_csv_path)
    assert df["year"].min() == 1979
    assert df["year"].max() == 2025


def test_load_co2_value_1979(co2_csv_path):
    df = load_co2(co2_csv_path)
    row = df[df["year"] == 1979].iloc[0]
    assert row["co2_mean"] == pytest.approx(336.85)
    assert row["co2_unc"] == pytest.approx(0.10)


def test_load_co2_no_nan(co2_csv_path):
    df = load_co2(co2_csv_path)
    assert df.isna().sum().sum() == 0
