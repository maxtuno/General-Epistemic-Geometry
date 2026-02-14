"""Compute GR perihelion precession for Mercury.

Run from repository root:
    python code/mercury_perihelion.py
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

AU = 149_597_870_700.0  # m (IAU 2012, exact)
C = 299_792_458.0  # m/s (exact)
MU_SUN = 1.32712440018e20  # m^3/s^2 (standard value)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = REPO_ROOT / "figures"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute Mercury's GR perihelion precession benchmark."
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Directory where mercury_perihelion.txt is written (default: <repo>/figures).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional explicit output file path (overrides --out-dir filename).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Accepted for CLI consistency; not used by this deterministic calculation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output.resolve() if args.output else out_dir / "mercury_perihelion.txt"

    a_au = 0.38709927
    eccentricity = 0.20563593
    semi_major_axis = a_au * AU

    delta_rad = 6 * math.pi * MU_SUN / (semi_major_axis * (1 - eccentricity**2) * C**2)
    delta_arcsec_orbit = delta_rad * (180 / math.pi) * 3600

    period_days = 87.9691
    orbits_century = 36525.0 / period_days
    delta_arcsec_century = delta_arcsec_orbit * orbits_century

    lines = [
        f"delta_phi_arcsec_per_orbit: {delta_arcsec_orbit:.12f}",
        f"delta_phi_arcsec_per_century: {delta_arcsec_century:.12f}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(lines[0])
    print(lines[1])
    print(f"Wrote benchmark output to {output_path}")


if __name__ == "__main__":
    main()
