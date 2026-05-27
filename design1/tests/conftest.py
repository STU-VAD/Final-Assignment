"""Pytest fixtures for design1 tests."""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def co2_csv_path() -> Path:
    return REPO_ROOT / "co2_annmean_gl.csv"


@pytest.fixture(scope="session")
def temp_csv_path() -> Path:
    return REPO_ROOT / "ZonAnn.Ts+dSST.csv"
