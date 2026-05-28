"""Construct the Plotly Figure for the design1 3D dashboard."""
from __future__ import annotations

import copy

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

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


def _slider_step(year: int) -> dict:
    return dict(
        method="animate",
        label=str(year),
        args=[[str(year)], dict(
            mode="immediate",
            frame=dict(duration=200, redraw=True),
            transition=dict(duration=0),
        )],
    )


def build_figure(long_df: pd.DataFrame) -> go.Figure:
    """Compose the full linked-multiview dashboard figure."""
    # Wide-form temp for heatmap
    temp_wide = long_df.pivot(index="lat_band", columns="year",
                               values="temp_anomaly")
    co2_only = long_df[["year", "co2_mean", "co2_unc"]].drop_duplicates()

    # Subplot layout: 3D (top-left) + heatmap (top-right) + CO2 line (bottom)
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "scene"}, {"type": "xy"}],
            [{"type": "xy", "colspan": 2}, None],
        ],
        column_widths=[0.6, 0.4],
        row_heights=[0.65, 0.35],
        subplot_titles=("3D 散点：CO₂ × 纬度 × 温度",
                        "热图：年 × 纬度",
                        "CO₂ 年均浓度时序"),
        horizontal_spacing=0.06,
        vertical_spacing=0.10,
    )

    # Initial frame: year animation_start (1979); no trail
    init_year = 1979
    init_df = long_df[long_df["year"] == init_year].dropna(subset=["co2_mean"])
    init_trail = long_df.iloc[0:0]  # empty with same columns
    fig.add_trace(_make_scatter3d(init_df, opacity=0.9, size=7,
                                   name=str(init_year)), row=1, col=1)
    fig.add_trace(_make_scatter3d(init_trail, opacity=0.25, size=4,
                                   name="历史轨迹"), row=1, col=1)

    # Heatmap (top-right)
    fig.add_trace(build_heatmap(temp_wide), row=1, col=2)

    # CO2 uncertainty band + line (bottom, spanning)
    upper, lower = build_co2_uncertainty_traces(co2_only)
    fig.add_trace(upper, row=2, col=1)
    fig.add_trace(lower, row=2, col=1)
    fig.add_trace(build_co2_trace(co2_only), row=2, col=1)

    # Animation frames (only update the two scatter3d traces by index)
    raw_frames = build_scatter_frames(long_df)
    frames = []
    for f in raw_frames:
        frames.append(go.Frame(
            name=f.name,
            data=list(f.data),
            traces=[0, 1],  # update first two traces only
        ))
    fig.frames = frames

    # Axes
    fig.update_scenes(
        xaxis_title="CO₂ (ppm)",
        yaxis_title="纬度",
        zaxis_title="温度异常 (°C)",
        zaxis=dict(range=list(TEMP_RANGE)),
        yaxis=dict(tickmode="array",
                   tickvals=[-77, -54, -34, -12, 12, 34, 54, 77],
                   ticktext=[BAND_LABEL[b] for b in FINE_BANDS]),
        camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8)),
    )
    fig.update_xaxes(title_text="年份", row=1, col=2)
    fig.update_yaxes(title_text="纬度带", row=1, col=2)
    fig.update_xaxes(title_text="年份", row=2, col=1)
    fig.update_yaxes(title_text="CO₂ (ppm)", row=2, col=1)

    # Slider + play/pause
    years = list(range(1979, 2026))
    # Build a custom template based on plotly_dark with a darker, blue-tinged
    # background. Deep-copy so we don't mutate the global plotly template.
    dark_template = copy.deepcopy(pio.templates["plotly_dark"])
    dark_template.layout.paper_bgcolor = "#0f1419"
    dark_template.layout.plot_bgcolor = "#0f1419"
    fig.update_layout(
        title=dict(
            text="全球气候演变三维探索：CO₂、纬度与温度异常 (1880–2025)",
            x=0.5, xanchor="center",
        ),
        template=dark_template,
        height=820,
        margin=dict(l=20, r=20, t=80, b=20),
        sliders=[dict(
            active=0,
            x=0.08, len=0.78, y=-0.02,
            currentvalue=dict(prefix="年份 ", font=dict(size=14, color="#fbbf24")),
            steps=[_slider_step(y) for y in years],
        )],
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.0, y=-0.04,
            buttons=[
                dict(label="▶ 播放", method="animate",
                     args=[None, dict(frame=dict(duration=200, redraw=True),
                                       fromcurrent=True, mode="immediate")]),
                dict(label="⏸ 暂停", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                         mode="immediate")]),
            ],
        )],
    )
    return fig
