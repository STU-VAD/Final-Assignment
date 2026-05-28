# 3D CO₂×纬度×温度 联动可视化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 根据 `2026-05-27-co2-latitude-temperature-3d-viz-design.md`，用 Python + Plotly 构建一个单文件 `index.html` 互动仪表板，包含 3D 散点（动画）、温度热图、CO₂ 时序三个联动面板，并附 pytest 单元测试。

**Architecture:** 在 `design1/` 下建立独立 Python 项目（`pyproject.toml` + `pytest`），扁平模块布局（`load_data.py` / `lat_bands.py` / `build_figure.py` / `build.py`），各模块单一职责。CSV 数据共享于仓库根目录，代码通过 `../` 引用。最终产物 `design1/index.html` 部署到 GitHub Pages。

**Tech Stack:** Python 3.12 · plotly ≥ 5.18 · pandas ≥ 2.2 · numpy ≥ 1.26 · pytest ≥ 8 · uv（依赖管理）

**Spec reference:** `design1/2026-05-27-co2-latitude-temperature-3d-viz-design.md`

---

## 目录结构（最终）

```
Finel-Assignment/
├── co2_annmean_gl.csv         # 共享数据（不动）
├── ZonAnn.Ts+dSST.csv         # 共享数据（不动）
├── pyproject.toml             # 仓库根，不动
├── .python-version            # 不动
├── README.md                  # 不动
├── analysis.html              # 组员产物，不动
├── prototype.html             # 组员产物，不动
└── design1/
    ├── 2026-05-27-co2-latitude-temperature-3d-viz-design.md  ✓已有
    ├── 2026-05-27-co2-latitude-temperature-3d-viz-plan.md    ✓本文档
    ├── pyproject.toml         ★ 新建：design1 独立项目
    ├── .python-version        ★ 新建：3.12
    ├── load_data.py           ★ 新建
    ├── lat_bands.py           ★ 新建
    ├── build_figure.py        ★ 新建
    ├── build.py               ★ 新建
    ├── tests/
    │   ├── __init__.py        ★ 新建
    │   ├── conftest.py        ★ 新建
    │   ├── test_load_data.py  ★ 新建
    │   └── test_build_figure.py ★ 新建
    └── index.html             ★ 构建产物
```

---

## Task 1：项目初始化

**Files:**
- Create: `design1/pyproject.toml`
- Create: `design1/.python-version`
- Create: `design1/tests/__init__.py`
- Create: `design1/tests/conftest.py`

- [ ] **Step 1.1：确认或安装 uv**

Run: `uv --version`
Expected: 输出版本号；如显示 `command not found`，先 `pip install uv` 安装。

- [ ] **Step 1.2：创建 `design1/pyproject.toml`**

```toml
[project]
name = "finel-assignment-design1"
version = "0.1.0"
description = "Interactive 3D visualization of CO2, latitude, and temperature (design1)"
requires-python = ">=3.12"
dependencies = [
    "plotly>=5.18",
    "pandas>=2.2",
    "numpy>=1.26",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

- [ ] **Step 1.3：创建 `design1/.python-version`**

文件内容（一行）：
```
3.12
```

- [ ] **Step 1.4：创建 `design1/tests/__init__.py`**

文件内容（空文件）。

- [ ] **Step 1.5：创建 `design1/tests/conftest.py`**

```python
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
```

- [ ] **Step 1.6：安装依赖并验证**

Run（在 `design1/` 目录下）:
```bash
cd design1
uv sync
```
Expected: 输出包含 `Resolved N packages` 并下载 plotly/pandas/numpy/pytest 到 `.venv/`。

- [ ] **Step 1.7：运行空 pytest 确认环境通**

Run（仍在 `design1/`）:
```bash
uv run pytest -v
```
Expected: `no tests ran` —— 表示 pytest 能找到目录但还没测试。

- [ ] **Step 1.8：提交**

Run（在仓库根目录）:
```bash
git add design1/pyproject.toml design1/.python-version design1/tests/__init__.py design1/tests/conftest.py
git commit -m "design1: 初始化 Python 项目骨架"
```

---

## Task 2：纬度带常量模块

**Files:**
- Create: `design1/lat_bands.py`
- Create: `design1/tests/test_lat_bands.py`

- [ ] **Step 2.1：写失败测试 `design1/tests/test_lat_bands.py`**

```python
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
```

- [ ] **Step 2.2：运行测试确认失败**

Run（在 `design1/`）: `uv run pytest tests/test_lat_bands.py -v`
Expected: `ModuleNotFoundError: No module named 'lat_bands'`

- [ ] **Step 2.3：实现 `design1/lat_bands.py`**

```python
"""8 fine latitude bands (south→north) with CSV columns, mid-latitudes, and labels."""

FINE_BANDS = [
    "90S-64S",  # 南极
    "64S-44S",  # 高纬南
    "44S-24S",  # 中纬南
    "24S-EQU",  # 赤南
    "EQU-24N",  # 赤北
    "24N-44N",  # 中纬北
    "44N-64N",  # 高纬北
    "64N-90N",  # 北极
]

BAND_MID = {
    "90S-64S": -77,
    "64S-44S": -54,
    "44S-24S": -34,
    "24S-EQU": -12,
    "EQU-24N": 12,
    "24N-44N": 34,
    "44N-64N": 54,
    "64N-90N": 77,
}

BAND_LABEL = {
    "90S-64S": "南极 (90S-64S)",
    "64S-44S": "高纬南 (64S-44S)",
    "44S-24S": "中纬南 (44S-24S)",
    "24S-EQU": "赤南 (24S-EQU)",
    "EQU-24N": "赤北 (EQU-24N)",
    "24N-44N": "中纬北 (24N-44N)",
    "44N-64N": "高纬北 (44N-64N)",
    "64N-90N": "北极 (64N-90N)",
}

BAND_COL = {b: b for b in FINE_BANDS}
```

- [ ] **Step 2.4：运行测试确认通过**

Run: `uv run pytest tests/test_lat_bands.py -v`
Expected: 5 passed

- [ ] **Step 2.5：提交**

```bash
git add design1/lat_bands.py design1/tests/test_lat_bands.py
git commit -m "design1: 添加 8 个纬度带配置 (lat_bands)"
```

---

## Task 3：CO₂ 数据加载

**Files:**
- Create: `design1/load_data.py`（部分内容）
- Create: `design1/tests/test_load_data.py`

- [ ] **Step 3.1：写失败测试**

在 `design1/tests/test_load_data.py`：

```python
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
```

- [ ] **Step 3.2：运行确认失败**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: `ModuleNotFoundError: No module named 'load_data'`

- [ ] **Step 3.3：实现 `design1/load_data.py`（初版只有 load_co2）**

```python
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
```

- [ ] **Step 3.4：运行确认通过**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: 5 passed

- [ ] **Step 3.5：提交**

```bash
git add design1/load_data.py design1/tests/test_load_data.py
git commit -m "design1: 添加 CO2 数据加载函数"
```

---

## Task 4：温度数据加载

**Files:**
- Modify: `design1/load_data.py`
- Modify: `design1/tests/test_load_data.py`

- [ ] **Step 4.1：在 `test_load_data.py` 追加测试**

在文件末尾追加：

```python
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
```

- [ ] **Step 4.2：运行确认失败**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: 已有 5 个 pass + 5 个新测试 `ImportError: cannot import name 'load_temperature'`

- [ ] **Step 4.3：在 `load_data.py` 追加 `load_temperature`**

```python
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
```

- [ ] **Step 4.4：运行确认全部通过**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: 10 passed

- [ ] **Step 4.5：提交**

```bash
git add design1/load_data.py design1/tests/test_load_data.py
git commit -m "design1: 添加温度数据加载函数"
```

---

## Task 5：合并长表

**Files:**
- Modify: `design1/load_data.py`
- Modify: `design1/tests/test_load_data.py`

- [ ] **Step 5.1：追加测试**

在 `test_load_data.py` 末尾：

```python
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
```

- [ ] **Step 5.2：运行确认失败**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: 6 个新测试都报 `ImportError: cannot import name 'build_long_df'`

- [ ] **Step 5.3：在 `load_data.py` 追加 `build_long_df`**

```python
from lat_bands import FINE_BANDS, BAND_MID


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
```

- [ ] **Step 5.4：运行确认通过**

Run: `uv run pytest tests/test_load_data.py -v`
Expected: 16 passed (10 旧 + 6 新)

- [ ] **Step 5.5：提交**

```bash
git add design1/load_data.py design1/tests/test_load_data.py
git commit -m "design1: 添加长表合并函数 build_long_df"
```

---

## Task 6：3D 散点轨迹（含尾迹）

**Files:**
- Create: `design1/build_figure.py`
- Create: `design1/tests/test_build_figure.py`

- [ ] **Step 6.1：写失败测试 `tests/test_build_figure.py`**

```python
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
```

- [ ] **Step 6.2：运行确认失败**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: `ModuleNotFoundError: No module named 'build_figure'`

- [ ] **Step 6.3：实现 `design1/build_figure.py`（初版只有 build_scatter_frames）**

```python
"""Construct the Plotly Figure for the design1 3D dashboard."""
from __future__ import annotations

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
```

- [ ] **Step 6.4：运行确认通过**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 5 passed

- [ ] **Step 6.5：提交**

```bash
git add design1/build_figure.py design1/tests/test_build_figure.py
git commit -m "design1: 添加 3D 散点帧构造（含 5 年尾迹）"
```

---

## Task 7：温度热图

**Files:**
- Modify: `design1/build_figure.py`
- Modify: `design1/tests/test_build_figure.py`

- [ ] **Step 7.1：追加测试**

```python
from build_figure import build_heatmap


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
    assert trace.colorscale is None or "RdBu" in str(trace.colorscale) or trace.colorscale == "RdBu_r"
```

- [ ] **Step 7.2：运行确认失败**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 3 new `ImportError: cannot import name 'build_heatmap'`

- [ ] **Step 7.3：在 `build_figure.py` 追加 `build_heatmap`**

```python
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
```

- [ ] **Step 7.4：运行确认通过**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 8 passed

- [ ] **Step 7.5：提交**

```bash
git add design1/build_figure.py design1/tests/test_build_figure.py
git commit -m "design1: 添加温度热图 trace"
```

---

## Task 8：CO₂ 时序

**Files:**
- Modify: `design1/build_figure.py`
- Modify: `design1/tests/test_build_figure.py`

- [ ] **Step 8.1：追加测试**

```python
from build_figure import build_co2_trace, build_co2_uncertainty_traces


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
```

- [ ] **Step 8.2：运行确认失败**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 4 new `ImportError`

- [ ] **Step 8.3：在 `build_figure.py` 追加两个函数**

```python
import numpy as np


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
```

- [ ] **Step 8.4：运行确认通过**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 12 passed

- [ ] **Step 8.5：提交**

```bash
git add design1/build_figure.py design1/tests/test_build_figure.py
git commit -m "design1: 添加 CO2 时序及不确定度带 traces"
```

---

## Task 9：组装总图 + 子图布局 + 滑块

**Files:**
- Modify: `design1/build_figure.py`
- Modify: `design1/tests/test_build_figure.py`

- [ ] **Step 9.1：追加测试**

```python
from build_figure import build_figure


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
```

- [ ] **Step 9.2：运行确认失败**

Run: `uv run pytest tests/test_build_figure.py::test_build_figure_returns_figure -v`
Expected: `ImportError: cannot import name 'build_figure'`

- [ ] **Step 9.3：实现 `build_figure` 主组装函数**

在 `build_figure.py` 末尾追加：

```python
from plotly.subplots import make_subplots


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
    fig.update_layout(
        title=dict(
            text="全球气候演变三维探索：CO₂、纬度与温度异常 (1880–2025)",
            x=0.5, xanchor="center",
        ),
        template="plotly_dark",
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
```

- [ ] **Step 9.4：运行所有图测试确认通过**

Run: `uv run pytest tests/test_build_figure.py -v`
Expected: 18 passed

- [ ] **Step 9.5：提交**

```bash
git add design1/build_figure.py design1/tests/test_build_figure.py
git commit -m "design1: 组装总图（子图布局 + 滑块 + 播放按钮）"
```

---

## Task 10：构建入口与 index.html 生成

**Files:**
- Create: `design1/build.py`
- Modify: `design1/tests/test_build_figure.py`

- [ ] **Step 10.1：追加冒烟测试**

```python
import subprocess
import sys
from pathlib import Path


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
```

- [ ] **Step 10.2：运行确认失败**

Run: `uv run pytest tests/test_build_figure.py::test_build_entry_produces_index_html -v`
Expected: `build failed: ... No such file: build.py`

- [ ] **Step 10.3：创建 `design1/build.py`**

```python
"""Entry point: build the design1 dashboard HTML."""
from __future__ import annotations

import argparse
from pathlib import Path

from load_data import build_long_df
from build_figure import build_figure


REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Build design1 index.html")
    parser.add_argument("--co2", type=Path,
                        default=REPO_ROOT / "co2_annmean_gl.csv",
                        help="Path to NOAA CO2 CSV")
    parser.add_argument("--temp", type=Path,
                        default=REPO_ROOT / "ZonAnn.Ts+dSST.csv",
                        help="Path to NASA GISTEMP zonal CSV")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "index.html",
                        help="Output HTML path")
    args = parser.parse_args()

    print(f"Loading data:\n  CO2:  {args.co2}\n  TEMP: {args.temp}")
    long_df = build_long_df(args.co2, args.temp)
    print(f"Loaded {len(long_df)} rows.")

    print("Building figure...")
    fig = build_figure(long_df)

    print(f"Writing {args.output}...")
    fig.write_html(
        args.output,
        include_plotlyjs="cdn",
        full_html=True,
    )
    size_kb = args.output.stat().st_size / 1024
    print(f"Done. {size_kb:.1f} KB.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 10.4：运行确认通过**

Run: `uv run pytest tests/test_build_figure.py::test_build_entry_produces_index_html -v`
Expected: PASS

- [ ] **Step 10.5：实际生成 index.html**

Run（在 `design1/`）:
```bash
uv run python build.py
```
Expected:
```
Loading data:
  CO2:  C:\Users\...\co2_annmean_gl.csv
  TEMP: C:\Users\...\ZonAnn.Ts+dSST.csv
Loaded 1168 rows.
Building figure...
Writing C:\Users\...\design1\index.html...
Done. NNN.N KB.
```

- [ ] **Step 10.6：运行完整测试套件**

Run: `uv run pytest -v`
Expected: 全部通过（25+ 测试）

- [ ] **Step 10.7：提交**

```bash
git add design1/build.py design1/tests/test_build_figure.py design1/index.html
git commit -m "design1: 添加构建入口并生成 index.html"
```

---

## Task 11：人工视觉验收

**Files:**
- None（仅手工检查 + 截图）

- [ ] **Step 11.1：浏览器打开 index.html**

Run（Windows）:
```bash
start design1/index.html
```
或在浏览器输入：`file:///C:/Users/a2545/Desktop/Finel-Assignment/design1/index.html`

- [ ] **Step 11.2：检查初始渲染**

确认：
- 标题"全球气候演变三维探索"显示在顶部
- 3D 散点图左上角，8 个彩色球点排列在 Y 轴
- 热图右上角，从冷色（左侧 1880s）渐变到红色（右侧 2020s）
- CO₂ 曲线占据底部，1979 前虚线/空白，1979 后实线上升
- 所有标签均为中文
- 暗色主题（黑/深蓝背景）

- [ ] **Step 11.3：检查交互**

确认：
- 拖动时间滑块 → 3D 点位移
- 点击 ▶ 播放 → 自动 1979→2025 滚动
- 点击 ⏸ 暂停 → 停止
- 鼠标拖拽 3D 主图 → 视角旋转
- 滚轮 → 3D 缩放
- 悬停某 3D 点 → 弹出 (年份/纬度/温度/CO₂) tooltip
- 悬停热图格子 → 弹出 (年份/纬度/温度) tooltip

- [ ] **Step 11.4：核对关键数据点**

- 2024 年北极（64N-90N）应显示温度异常 ≈ +2.92 °C
- 2025 年北极应显示 ≈ +3.01 °C
- 2025 年 CO₂ ≈ 425.65 ppm
- 1979 帧的 8 个点温度异常普遍较低（约 -0.6 ~ +0.3）

- [ ] **Step 11.5：截图存档**

截 3 张：1979 帧、2000 帧、2025 帧，命名 `design1/screenshots/frame_<year>.png`。
（仅用于 README 与课程报告，非必需）

- [ ] **Step 11.6：在 README 顶部追加 design1 入口段落**

修改 `README.md`，在第一行前插入：

```markdown
## design1 · 3D CO₂ × 纬度 × 温度 联动可视化

- 设计文档：[design1/2026-05-27-co2-latitude-temperature-3d-viz-design.md](design1/2026-05-27-co2-latitude-temperature-3d-viz-design.md)
- 实施计划：[design1/2026-05-27-co2-latitude-temperature-3d-viz-plan.md](design1/2026-05-27-co2-latitude-temperature-3d-viz-plan.md)
- 公开访问：（部署后填 GitHub Pages URL）
- 本地预览：`cd design1&& uv run python build.py && start index.html`

---
```

- [ ] **Step 11.7：提交 + 推送**

```bash
git add README.md design1/screenshots/  # screenshots 可选
git commit -m "design1: 验收完成；README 添加 design1 入口"
git pull --rebase origin main
git push origin main
```

---

## Task 12：GitHub Pages 部署

**Files:**
- 在 GitHub 网页操作；本地仅最终核对

- [ ] **Step 12.1：开启 Pages**

到 https://github.com/STU-VAD/Finel-Assignment/settings/pages

设置：
- Source: `Deploy from a branch`
- Branch: `main` / `/ (root)`
- 保存

- [ ] **Step 12.2：等待第一次部署**

通常 ≈ 30 秒。检查 https://stu-vad.github.io/Finel-Assignment/design1/ 能否打开。

- [ ] **Step 12.3：把 URL 填回 README**

在 design1 入口段的"公开访问"行填写：
`https://stu-vad.github.io/Finel-Assignment/design1/`

- [ ] **Step 12.4：提交最终 README**

```bash
git add README.md
git commit -m "design1: 在 README 写明 GitHub Pages URL"
git pull --rebase origin main
git push origin main
```

---

## Task 13：拓展功能（Stretch · 时间允许时再做）

设计 spec 第 6 节列了两项需要 JS 回调或额外数据变体的高级交互，**不属于 MVP 必交付项**。MVP 通过 Task 1–12 已经可运行、可演示。先把基本盘交出去再回来加。

### 13.A 纬度粒度切换下拉框（8 细带 ↔ 3 粗带 ↔ 半球）

**思路**：在 `load_data.py` 增加 `load_temperature_coarse()` 和 `load_temperature_hemispheres()`，预生成 3 套 frames，用 Plotly `updatemenus`（dropdown 类型）切换 `visible` + `relayout` Y 轴刻度。

**预估代价**：100 ~ 150 行新代码 + 6 个新测试。

**当不应做**：MVP 已经满足课程"interactive visualization"要求；此功能锦上添花。

### 13.B 点击热图格子跳到对应年份

**思路**：用 Plotly 内置事件无法在静态 HTML 中跨子图驱动滑块。需要在 `fig.write_html()` 时注入自定义 `<script>`，监听 `plotly_click` 然后调用 `Plotly.animate(gd, ['<year>'])`。

**预估代价**：约 30 行内联 JS。

**当不应做**：若 Task 11 验收时滑块/播放/旋转都已让评审满意。

---

## 范围外（YAGNI 提醒）

设计文档第 9 节已明确不做：3D 曲面/飘带变体、冰芯 CO₂ 拼接、月度数据、反向交互、登录/分享/移动响应式。计划期间如果想加这些功能，**不要做**——拉到下个迭代（design2）。

## 完成条件

所有 11 个任务的 checkbox 都打钩，并且：
- `uv run pytest` 全绿
- 浏览器打开 `design1/index.html` 三个面板都正常渲染、滑块/播放/旋转/悬停四类交互都生效
- `https://stu-vad.github.io/Finel-Assignment/design1/` 公网可访问
- README 包含 design1 入口段
