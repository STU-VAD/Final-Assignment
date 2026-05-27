"""Tests for latitude band definitions."""
from lat_bands import BAND_COL, BAND_LABEL, BAND_MID, FINE_BANDS


def test_eight_fine_bands_defined():
    assert len(FINE_BANDS) == 8


def test_bands_ordered_south_to_north():
    mids = [BAND_MID[b] for b in FINE_BANDS]
    assert mids == sorted(mids), f"bands not south-to-north: {mids}"


def test_first_band_is_south_pole():
    assert FINE_BANDS[0] == "90S-64S"
    assert BAND_LABEL["90S-64S"] == "南极 (90S-64S)"
    assert BAND_MID["90S-64S"] == -77


def test_last_band_is_north_pole():
    assert FINE_BANDS[-1] == "64N-90N"
    assert BAND_LABEL["64N-90N"] == "北极 (64N-90N)"
    assert BAND_MID["64N-90N"] == 77


def test_band_columns_match_csv_headers():
    expected_cols = {
        "64N-90N", "44N-64N", "24N-44N", "EQU-24N",
        "24S-EQU", "44S-24S", "64S-44S", "90S-64S",
    }
    assert set(BAND_COL.values()) == expected_cols
