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


from load_data import load_temperature


def test_load_temperature_returns_dataframe(temp_csv_path):
    df = load_temperature(temp_csv_path)
    assert isinstance(df, pd.DataFrame)


def test_load_temperature_year_range(temp_csv_path):
    df = load_temperature(temp_csv_path)
    assert df["year"].min() == 1880
    assert df["year"].max() == 2025


def test_load_temperature_has_all_8_bands(temp_csv_path):
    df = load_temperature(temp_csv_path)
    expected = {"90S-64S", "64S-44S", "44S-24S", "24S-EQU",
                "EQU-24N", "24N-44N", "44N-64N", "64N-90N"}
    assert expected.issubset(set(df.columns))


def test_load_temperature_2025_north_pole_value(temp_csv_path):
    df = load_temperature(temp_csv_path)
    row = df[df["year"] == 2025].iloc[0]
    assert row["64N-90N"] == pytest.approx(3.01)


def test_load_temperature_146_rows(temp_csv_path):
    df = load_temperature(temp_csv_path)
    assert len(df) == 146  # 1880..2025 inclusive


import numpy as np

from load_data import build_long_df


def test_build_long_df_columns(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    assert set(df.columns) == {"year", "lat_band", "lat_mid",
                                "temp_anomaly", "co2_mean", "co2_unc"}


def test_build_long_df_row_count(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    # 8 bands × 146 years (1880..2025)
    assert len(df) == 8 * 146


def test_build_long_df_co2_nan_before_1979(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    pre1979 = df[df["year"] < 1979]
    assert pre1979["co2_mean"].isna().all()


def test_build_long_df_co2_not_nan_after_1979(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    post1979 = df[df["year"] >= 1979]
    assert not post1979["co2_mean"].isna().any()


def test_build_long_df_lat_mid_correct(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    row = df[(df["year"] == 2000) & (df["lat_band"] == "64N-90N")].iloc[0]
    assert row["lat_mid"] == 77


def test_build_long_df_temp_value_correct(co2_csv_path, temp_csv_path):
    df = build_long_df(co2_csv_path, temp_csv_path)
    row = df[(df["year"] == 2025) & (df["lat_band"] == "64N-90N")].iloc[0]
    assert row["temp_anomaly"] == pytest.approx(3.01)
