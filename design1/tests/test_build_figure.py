"""Tests for figure construction."""
import subprocess
import sys
from pathlib import Path

import pytest
import plotly.graph_objects as go

from load_data import build_long_df
from build_figure import build_scatter_frames
from build_figure import build_heatmap
from build_figure import build_co2_trace, build_co2_uncertainty_traces
from build_figure import build_figure


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


def test_heatmap_returns_trace(long_df):
    temp_wide = long_df.pivot(index="lat_band", columns="year",
                               values="temp_anomaly")
    trace = build_heatmap(temp_wide)
    assert trace.type == "heatmap"


def test_heatmap_z_shape(long_df):
    temp_wide = long_df.pivot(index="lat_band", columns="year",
                               values="temp_anomaly")
    trace = build_heatmap(temp_wide)
    # 8 rows × 146 cols
    assert len(trace.z) == 8
    assert len(trace.z[0]) == 146


def test_heatmap_uses_rdbu_colorscale(long_df):
    temp_wide = long_df.pivot(index="lat_band", columns="year",
                               values="temp_anomaly")
    trace = build_heatmap(temp_wide)
    cs_str = str(trace.colorscale)
    # Plotly may store the string "RdBu_r" verbatim or normalize it to RGB tuples.
    # RdBu_r endpoints: rgb(5,48,97) deep blue ↔ rgb(103,0,31) deep red.
    assert (
        "RdBu" in cs_str
        or "rgb(5,48,97)" in cs_str
        or "rgb(103,0,31)" in cs_str
    ), f"unexpected colorscale: {cs_str[:200]}"


def test_co2_trace_type(long_df):
    co2_only = long_df[["year", "co2_mean", "co2_unc"]].drop_duplicates()
    trace = build_co2_trace(co2_only)
    assert trace.type == "scatter"
    assert trace.mode == "lines"


def test_co2_trace_x_covers_full_range(long_df):
    co2_only = long_df[["year", "co2_mean", "co2_unc"]].drop_duplicates()
    trace = build_co2_trace(co2_only)
    assert min(trace.x) == 1880
    assert max(trace.x) == 2025


def test_co2_trace_y_nan_before_1979(long_df):
    co2_only = long_df[["year", "co2_mean", "co2_unc"]].drop_duplicates()
    trace = build_co2_trace(co2_only)
    # Find index for year 1900
    idx_1900 = list(trace.x).index(1900)
    y_1900 = trace.y[idx_1900]
    # pandas NaN serializes to None in plotly trace.y tuple
    assert y_1900 is None or (isinstance(y_1900, float) and y_1900 != y_1900)


def test_uncertainty_band_returns_two_traces(long_df):
    co2_only = long_df[["year", "co2_mean", "co2_unc"]].drop_duplicates()
    upper, lower = build_co2_uncertainty_traces(co2_only)
    assert upper.type == "scatter"
    assert lower.type == "scatter"
    assert lower.fill == "tonexty"


def test_build_figure_returns_figure(long_df):
    fig = build_figure(long_df)
    assert isinstance(fig, go.Figure)


def test_build_figure_has_47_frames(long_df):
    fig = build_figure(long_df)
    assert len(fig.frames) == 47


def test_build_figure_has_slider(long_df):
    fig = build_figure(long_df)
    assert fig.layout.sliders is not None
    assert len(fig.layout.sliders) == 1
    # 47 slider steps (one per year)
    assert len(fig.layout.sliders[0].steps) == 47


def test_build_figure_has_play_pause_buttons(long_df):
    fig = build_figure(long_df)
    assert fig.layout.updatemenus is not None
    buttons = fig.layout.updatemenus[0].buttons
    labels = [b.label for b in buttons]
    assert "▶ 播放" in labels
    assert "⏸ 暂停" in labels


def test_build_figure_chinese_title(long_df):
    fig = build_figure(long_df)
    assert "三维探索" in fig.layout.title.text


def test_build_figure_dark_theme(long_df):
    fig = build_figure(long_df)
    assert fig.layout.template.layout.paper_bgcolor in {"#0f1419", "rgb(15,20,25)"} \
        or "plotly_dark" in str(fig.layout.template)


def test_build_entry_produces_index_html(tmp_path, monkeypatch):
    """End-to-end: running build.py creates a non-empty index.html."""
    design_dir = Path(__file__).resolve().parents[1]
    output = tmp_path / "index.html"
    cmd = [sys.executable, str(design_dir / "build.py"), "--output", str(output)]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=design_dir)
    assert result.returncode == 0, f"build failed: {result.stderr}"
    assert output.exists()
    assert output.stat().st_size > 100_000  # ≥ 100 KB
    text = output.read_text(encoding="utf-8")
    assert "三维探索" in text
    assert "Plotly" in text
