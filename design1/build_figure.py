"""Construct the Plotly Figure for the design1 3D dashboard."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from lat_bands import FINE_BANDS, BAND_LABEL


TEMP_RANGE = (-3.0, 3.0)
COLORSCALE = "RdBu_r"


def _make_scatter3d(df: pd.DataFrame, opacity: float, size: int,
                    name: str, showlegend: bool = False) -> go.Scatter3d:
    """Internal: build one Scatter3d trace from a long-form subset."""
    return go.Scatter3d(
        x=df["co2_mean"].tolist(),
        y=df["lat_mid"].tolist(),
        z=df["temp_anomaly"].tolist(),
        mode="markers",
        marker=dict(
            size=size,
            color=df["temp_anomaly"].tolist(),
            colorscale=COLORSCALE,
            cmin=TEMP_RANGE[0],
            cmax=TEMP_RANGE[1],
            opacity=opacity,
            showscale=False,
        ),
        name=name,
        showlegend=showlegend,
        customdata=df[["year", "lat_band"]].to_numpy(),
        hovertemplate=(
            "年份 %{customdata[0]}<br>"
            "纬度带 %{customdata[1]}<br>"
            "CO₂ %{x:.2f} ppm<br>"
            "温度异常 %{z:+.2f} °C<extra></extra>"
        ),
    )


def build_scatter_frames(long_df: pd.DataFrame,
                         animation_start: int = 1979,
                         animation_end: int = 2025,
                         trail_years: int = 5) -> list[go.Frame]:
    """Build one Plotly Frame per year in [animation_start, animation_end].

    Each Frame contains two traces:
    - Index 0: current-year scatter (8 high-opacity points)
    - Index 1: trailing scatter (up to trail_years * 8 semi-transparent points)
    """
    years = list(range(animation_start, animation_end + 1))
    frames: list[go.Frame] = []
    for year in years:
        current_df = long_df[long_df["year"] == year].dropna(subset=["co2_mean"])
        trail_start = max(year - trail_years, animation_start)
        trail_df = long_df[
            (long_df["year"] >= trail_start)
            & (long_df["year"] < year)
        ].dropna(subset=["co2_mean"])
        frames.append(go.Frame(
            name=str(year),
            data=[
                _make_scatter3d(current_df, opacity=0.9, size=7,
                                name=f"{year}", showlegend=False),
                _make_scatter3d(trail_df, opacity=0.25, size=4,
                                name="历史轨迹", showlegend=False),
            ],
        ))
    return frames


def build_heatmap(temp_wide: pd.DataFrame) -> go.Heatmap:
    """Build the year × latitude temperature heatmap trace.

    `temp_wide`: lat_band index × year columns, values = temp anomaly.
    Returns a Heatmap trace ready to drop into a subplot.
    """
    # Reorder rows south→north so they align with 3D Y axis
    temp_wide = temp_wide.reindex(FINE_BANDS)
    y_labels = [BAND_LABEL[b] for b in temp_wide.index]
    return go.Heatmap(
        z=temp_wide.values.tolist(),
        x=temp_wide.columns.tolist(),
        y=y_labels,
        colorscale=COLORSCALE,
        zmin=TEMP_RANGE[0],
        zmax=TEMP_RANGE[1],
        colorbar=dict(title="温度异常 °C", thickness=10),
        hovertemplate="年份 %{x}<br>纬度带 %{y}<br>温度异常 %{z:+.2f} °C<extra></extra>",
    )


def build_co2_trace(co2_df: pd.DataFrame) -> go.Scatter:
    """Build the central CO2 line trace (1880-2025; pre-1979 has NaN y)."""
    co2_df = co2_df.sort_values("year").reset_index(drop=True)
    return go.Scatter(
        x=co2_df["year"].tolist(),
        y=co2_df["co2_mean"].tolist(),
        mode="lines",
        line=dict(color="#66c2ff", width=2),
        connectgaps=False,
        name="CO₂ 年均",
        hovertemplate="年份 %{x}<br>CO₂ %{y:.2f} ppm<extra></extra>",
        showlegend=False,
    )


def build_co2_uncertainty_traces(co2_df: pd.DataFrame) -> tuple[go.Scatter, go.Scatter]:
    """Build (upper, lower) traces for the ±unc ribbon below the CO2 line."""
    co2_df = co2_df.sort_values("year").reset_index(drop=True)
    upper_y = (co2_df["co2_mean"] + co2_df["co2_unc"]).tolist()
    lower_y = (co2_df["co2_mean"] - co2_df["co2_unc"]).tolist()
    upper = go.Scatter(
        x=co2_df["year"].tolist(),
        y=upper_y,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    )
    lower = go.Scatter(
        x=co2_df["year"].tolist(),
        y=lower_y,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(102,194,255,0.18)",
        showlegend=False,
        hoverinfo="skip",
    )
    return upper, lower
