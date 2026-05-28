"""Entry point: build the design1 dashboard HTML."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from load_data import build_long_df
from build_figure import build_figure


REPO_ROOT = Path(__file__).resolve().parent.parent

_UNICODE_ESCAPE_RE = re.compile(r"\\u([0-9a-fA-F]{4})")


def _decode_json_unicode_escapes(html: str) -> str:
    """Replace \\uXXXX escapes (Plotly JSON output) with raw UTF-8 characters.

    Plotly's json.dumps uses ensure_ascii=True, so Chinese characters get
    escaped. Decoding them produces a smaller HTML file with readable source.
    """
    def repl(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))
    return _UNICODE_ESCAPE_RE.sub(repl, html)


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
    html = fig.to_html(
        include_plotlyjs="cdn",
        full_html=True,
    )
    html = _decode_json_unicode_escapes(html)
    args.output.write_text(html, encoding="utf-8")
    size_kb = args.output.stat().st_size / 1024
    print(f"Done. {size_kb:.1f} KB.")


if __name__ == "__main__":
    main()

