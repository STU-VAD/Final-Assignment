"""Load and reshape CO2 and zonal temperature data."""
from pathlib import Path

import pandas as pd


def load_co2(csv_path: str | Path) -> pd.DataFrame:
    """Load NOAA global annual CO2 mean.

    Returns a DataFrame with columns: year (int), co2_mean (float, ppm), co2_unc (float).
    Comment lines starting with '#' are skipped.
    """
    df = pd.read_csv(csv_path, comment="#", skip_blank_lines=True)
    df = df.rename(columns={"mean": "co2_mean", "unc": "co2_unc"})
    df["year"] = df["year"].astype(int)
    return df[["year", "co2_mean", "co2_unc"]].reset_index(drop=True)
