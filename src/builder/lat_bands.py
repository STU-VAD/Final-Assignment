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
