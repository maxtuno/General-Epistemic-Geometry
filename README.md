# General Epistemic Geometry

Foundational research monograph and companion papers by **Oscar Riveros**.  
**Canonical final edition:** February 2026.

## Quick Links

- Canonical monograph PDF (root): [General_Epistemic_Geometry_Book.pdf](./General_Epistemic_Geometry_Book.pdf)
- Epistemic Geometry of Closure PDF (root): [Epistemic_Geometry_of_Closure - Riveros.pdf](<./Epistemic_Geometry_of_Closure - Riveros.pdf>)
- Foundational Papers repository: [maxtuno/EPISTEMIC-GEOMETRY](https://github.com/maxtuno/EPISTEMIC-GEOMETRY)
- Academia pages:
  - [General Epistemic Geometry](https://www.academia.edu/164594131/General_Epistemic_Geometry)
  - [Epistemic Geometry of Closure](https://www.academia.edu/164640745/Epistemic_Geometry_of_Closure_SCE_IM_Coherent_Flow_Stability_and_Operational_Completeness)

## Table of Contents

- [Repository Layout](#repository-layout)
- [Quickstart (Reproduce)](#quickstart-reproduce)
- [Script CLI](#script-cli)
- [Data](#data)
- [Outputs](#outputs)
- [Scholarly Description](#scholarly-description)
- [How to Cite](#how-to-cite)
- [License](#license)

## Repository Layout

This repository keeps canonical PDFs in the repository root and reproducible scripts/data in dedicated folders.

```text
.
|-- code/
|   |-- generate_figures.py
|   |-- mercury_perihelion.py
|   `-- requirements.txt
|-- data/
|   |-- jaramillo_lousto_table1.csv
|   `-- toy_boundary_error.csv
|-- figures/                       # generated outputs (created automatically)
|-- General_Epistemic_Geometry_Book.pdf
|-- Epistemic_Geometry_of_Closure - Riveros.pdf
`-- README.md
```

## Quickstart (Reproduce)

Run from repository root.

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
python code/generate_figures.py
python code/mercury_perihelion.py
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r code/requirements.txt
python code/generate_figures.py
python code/mercury_perihelion.py
```

## Script CLI

### `python code/generate_figures.py --help`

- `--data-dir`: directory with CSV inputs (default: `data/`)
- `--input`: optional explicit main CSV path (default: `data/jaramillo_lousto_table1.csv`)
- `--boundary-error`: optional explicit boundary-error CSV path (default: `data/toy_boundary_error.csv`)
- `--out-dir`: output directory for figures (default: `figures/`)
- `--seed`: random seed for toy Monte Carlo
- `--mc`: number of Monte Carlo samples

Example:

```bash
python code/generate_figures.py --data-dir data --out-dir figures --seed 0
```

### `python code/mercury_perihelion.py --help`

- `--out-dir`: directory for output text file (default: `figures/`)
- `--output`: optional explicit output file path
- `--seed`: accepted for CLI consistency; the calculation is deterministic

Example:

```bash
python code/mercury_perihelion.py --out-dir figures
```

## Data

- `data/jaramillo_lousto_table1.csv`:
  - Critical separation table (`q_M2_over_M1`, `d_crit`, `d_crit_over_Mtot`).
  - Used by `code/generate_figures.py` for `fig_dcrit_vs_q.png` and interpolation in the toy gray-zone model.
- `data/toy_boundary_error.csv`:
  - Toy boundary bank size vs sup-norm error (`N_boundary_points`, `sup_norm_boundary_error`).
  - Used by `code/generate_figures.py` for `fig_vgray_vs_N.png`.

Both scripts resolve paths from repository structure (no hard-coded absolute paths required).

## Outputs

Generated artifacts are written to `figures/` (created automatically if absent):

- `figures/fig_dcrit_vs_q.png`
- `figures/fig_vgray_vs_tau.png`
- `figures/fig_vgray_vs_N.png`
- `figures/mercury_perihelion.txt`

## Scholarly Description

*General Epistemic Geometry* proposes a geometric framework for scientific knowledge under finite resources.  
Its core claim is that the syntax-semantics gap is measurable and certifiable as geometry.

Key concepts retained from the monograph:

1. Continuous Geometric CNF semantics through forbidden regions.
2. Geometric compilation mechanisms (`AddBox` / `AddCube`) with resource tracking.
3. Epistemic curvature as an invariant:

$$
\kappa(o) = \inf_{s \in \mathcal{S}_o} \mathrm{Err}(s,o)
$$

4. DRP (Derivational Refinement Principle) for convergence and realizability.
5. Complexity-theoretic obstructions interpreted as positive geometric curvature.
6. Differential lifting and Sobolev-regular certification in PDE-governed settings.
7. Operationally certified gray zones:

$$
\mathcal{G} = \Theta \setminus (\mathcal{A} \cup \mathcal{N})
$$

8. Topological robustness (braids, knots, configuration spaces).
9. Coherent flow of theories under invariant-preserving extension.

Editorial principle:

> Always extend, never reduce.

## How to Cite

For February 2026 references, cite the canonical root PDFs.

- Primary canonical monograph: `General_Epistemic_Geometry_Book.pdf`
- Companion closure paper: `Epistemic_Geometry_of_Closure - Riveros.pdf`

Minimal BibTeX:

```bibtex
@misc{riveros2026geg,
  author       = {Riveros, Oscar},
  title        = {General Epistemic Geometry},
  year         = {2026},
  month        = feb,
  note         = {Canonical Final Edition},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/General_Epistemic_Geometry_Book.pdf}}
}

@misc{riveros2026closure,
  author       = {Riveros, Oscar},
  title        = {Epistemic Geometry of Closure},
  year         = {2026},
  month        = feb,
  note         = {SCE-IM, Coherent Flow, Stability, and Operational Completeness},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Epistemic_Geometry_of_Closure%20-%20Riveros.pdf}}
}
```

## License

Unless otherwise specified in individual files: **All rights reserved.**
