"""Tests for figure construction."""
import pytest

from load_data import build_long_df
from build_figure import build_scatter_frames


@pytest.fixture(scope="module")
def long_df(co2_csv_path, temp_csv_path):
    return build_long_df(co2_csv_path, temp_csv_path)


def test_scatter_frames_count(long_df):
    frames = build_scatter_frames(long_df, animation_start=1979,
                                   animation_end=2025, trail_years=5)
    # 47 frames (1979..2025)
    assert len(frames) == 47


def test_scatter_frames_first_is_1979(long_df):
    frames = build_scatter_frames(long_df, animation_start=1979,
                                   animation_end=2025, trail_years=5)
    assert frames[0].name == "1979"


def test_scatter_frame_has_two_traces(long_df):
    """Each frame contains: current year (8 points) + trail (up to 8*trail_years)."""
    frames = build_scatter_frames(long_df, animation_start=1979,
                                   animation_end=2025, trail_years=5)
    f = frames[0]
    assert len(f.data) == 2  # current + trail


def test_current_year_trace_has_8_points(long_df):
    frames = build_scatter_frames(long_df, animation_start=1979,
                                   animation_end=2025, trail_years=5)
    current = frames[10].data[0]  # frame for year 1989
    assert len(current.x) == 8


def test_trail_size_bounded(long_df):
    frames = build_scatter_frames(long_df, animation_start=1979,
                                   animation_end=2025, trail_years=5)
    # frame index 0 = year 1979, no preceding years → trail empty
    assert len(frames[0].data[1].x) == 0
    # frame index 10 = year 1989, 5 preceding years × 8 bands
    assert len(frames[10].data[1].x) == 5 * 8
