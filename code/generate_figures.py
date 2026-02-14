"""Generate reproducible figures from CSV inputs.

Run from repository root:
    python code/generate_figures.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = REPO_ROOT / "data"
DEFAULT_OUT_DIR = REPO_ROOT / "figures"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate paper figures from CSV inputs."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Directory containing CSV inputs (default: <repo>/data).",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to main boundary CSV (defaults to <data-dir>/jaramillo_lousto_table1.csv).",
    )
    parser.add_argument(
        "--boundary-error",
        type=Path,
        default=None,
        help="Path to boundary error CSV (defaults to <data-dir>/toy_boundary_error.csv).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for generated figures (default: <repo>/figures).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for the Monte Carlo toy model.",
    )
    parser.add_argument(
        "--mc",
        type=int,
        default=250000,
        help="Monte Carlo samples for the gray-zone estimate.",
    )
    # Backward-compatible aliases.
    parser.add_argument("--data", dest="legacy_data", type=Path, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--outdir", dest="legacy_outdir", type=Path, default=None, help=argparse.SUPPRESS)
    return parser.parse_args()


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    input_csv = args.input or args.legacy_data or (args.data_dir / "jaramillo_lousto_table1.csv")
    boundary_error_csv = args.boundary_error or (args.data_dir / "toy_boundary_error.csv")
    out_dir = args.legacy_outdir or args.out_dir
    return input_csv.resolve(), boundary_error_csv.resolve(), out_dir.resolve()


def read_required_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required CSV: {path}")
    return pd.read_csv(path)


def main() -> None:
    args = parse_args()
    input_csv, boundary_error_csv, out_dir = resolve_paths(args)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = read_required_csv(input_csv).sort_values("q_M2_over_M1")
    q = df["q_M2_over_M1"].to_numpy()
    dnorm = df["d_crit_over_Mtot"].to_numpy()

    boundary_df = read_required_csv(boundary_error_csv).sort_values("N_boundary_points")
    ns = boundary_df["N_boundary_points"].to_numpy()
    errs = boundary_df["sup_norm_boundary_error"].to_numpy()

    # Figure 1: critical separation versus mass ratio.
    plt.figure(figsize=(6.6, 4.2))
    plt.plot(q, dnorm, marker="o")
    plt.xlabel("q = M2/M1 (M1 fixed)")
    plt.ylabel("d_crit / (M1+M2)")
    plt.title("Critical separation for common apparent horizon (normalized)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "fig_dcrit_vs_q.png", dpi=200)
    plt.close()

    # Figure 2: toy gray fraction versus tau.
    dmin, dmax = 0.60, 0.80
    rng = np.random.default_rng(args.seed)

    def dcrit_interp(qv: np.ndarray) -> np.ndarray:
        return np.interp(qv, q, dnorm)

    def gray_fraction(tau: float) -> float:
        qs = rng.uniform(q.min(), q.max(), size=args.mc)
        ds = rng.uniform(dmin, dmax, size=args.mc)
        boundary = dcrit_interp(qs)
        return (np.abs(ds - boundary) <= tau).mean()

    taus = np.array([0.002, 0.004, 0.006, 0.008, 0.010, 0.015, 0.020])
    vals = np.array([gray_fraction(t) for t in taus])

    plt.figure(figsize=(6.6, 4.2))
    plt.plot(taus, vals, marker="o")
    plt.xlabel(r"margin $\tau$ (in $d/(M_1+M_2)$ units)")
    plt.ylabel("gray-zone fraction in K")
    plt.title(r"Toy prediction: $V_{\mathrm{gray}}(\tau)$ grows ~ linearly in $\tau$")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "fig_vgray_vs_tau.png", dpi=200)
    plt.close()

    # Figure 3: toy gray fraction versus boundary-bank size N.
    delta_d = dmax - dmin
    taus_sel = [0.005, 0.01, 0.02]

    plt.figure(figsize=(6.6, 4.2))
    for tau in taus_sel:
        frac = np.clip(2 * (tau + errs) / delta_d, 0, 1)
        plt.plot(ns, frac, marker="o", label=fr"$\tau={tau}$")
    plt.xlabel("bank size N (boundary samples in q)")
    plt.ylabel("predicted gray-zone fraction in K")
    plt.title("Gray-zone vs bank density (toy): floor + bank error")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "fig_vgray_vs_N.png", dpi=200)
    plt.close()

    print(f"Wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
