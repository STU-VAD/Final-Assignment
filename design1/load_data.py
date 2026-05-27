"""Load and reshape CO2 and zonal temperature data."""
from pathlib import Path

import pandas as pd

from lat_bands import FINE_BANDS, BAND_MID


def load_co2(csv_path: str | Path) -> pd.DataFrame:
    """Load NOAA global annual CO2 mean.

    Returns a DataFrame with columns: year (int), co2_mean (float, ppm), co2_unc (float).
    Comment lines starting with '#' are skipped.
    """
    df = pd.read_csv(csv_path, comment="#", skip_blank_lines=True)
    df = df.rename(columns={"mean": "co2_mean", "unc": "co2_unc"})
    df["year"] = df["year"].astype(int)
    return df[["year", "co2_mean", "co2_unc"]].reset_index(drop=True)


def load_temperature(csv_path: str | Path) -> pd.DataFrame:
    """Load NASA GISTEMP zonal annual temperature anomalies.

    Returns a DataFrame indexed implicitly with columns:
    - year (int)
    - 8 fine band columns: 90S-64S, 64S-44S, 44S-24S, 24S-EQU,
      EQU-24N, 24N-44N, 44N-64N, 64N-90N (each float, °C anomaly)
    """
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Year": "year"})
    df["year"] = df["year"].astype(int)
    fine_bands = ["90S-64S", "64S-44S", "44S-24S", "24S-EQU",
                  "EQU-24N", "24N-44N", "44N-64N", "64N-90N"]
    return df[["year"] + fine_bands].reset_index(drop=True)


def build_long_df(co2_csv_path: str | Path,
                  temp_csv_path: str | Path) -> pd.DataFrame:
    """Merge CO2 + temperature into a long-form DataFrame.

    Returns columns: year, lat_band, lat_mid, temp_anomaly, co2_mean, co2_unc.
    CO2 columns are NaN for years before 1979.
    """
    co2 = load_co2(co2_csv_path)
    temp = load_temperature(temp_csv_path)

    long = temp.melt(
        id_vars="year",
        value_vars=FINE_BANDS,
        var_name="lat_band",
        value_name="temp_anomaly",
    )
    long["lat_mid"] = long["lat_band"].map(BAND_MID)
    long = long.merge(co2, on="year", how="left")
    return long.sort_values(["year", "lat_mid"]).reset_index(drop=True)
