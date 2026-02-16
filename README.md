# General Epistemic Geometry

Foundational research monograph and companion papers by **Oscar Riveros**.  
**Canonical final edition:** February 2026.

## Quick Links

- Canonical monograph PDF (root): [General_Epistemic_Geometry_Book.pdf](./General_Epistemic_Geometry_Book.pdf)
- Finite-Bank certification paper (root): [Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf](<./Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf>)
- Epistemic Geometry of Closure PDF (root): [Epistemic_Geometry_of_Closure - Riveros.pdf](<./Epistemic_Geometry_of_Closure - Riveros.pdf>)
- Epistemic Closure Net PDF (root): [Epistemic_Closure_Net - Riveros.pdf](<./Epistemic_Closure_Net - Riveros.pdf>)
- Foundational Papers repository: [maxtuno/EPISTEMIC-GEOMETRY](https://github.com/maxtuno/EPISTEMIC-GEOMETRY)
- Academia pages:
  - [General Epistemic Geometry](https://www.academia.edu/164594131/General_Epistemic_Geometry)
  - [Epistemic Geometry of Closure](https://www.academia.edu/164640745/Epistemic_Geometry_of_Closure_SCE_IM_Coherent_Flow_Stability_and_Operational_Completeness)

## Table of Contents

- [Document Abstracts](#document-abstracts)
- [Repository Layout](#repository-layout)
- [Quickstart (Reproduce)](#quickstart-reproduce)
- [Script CLI](#script-cli)
- [Data](#data)
- [Outputs](#outputs)
- [Supplementary Artifacts Directory](#supplementary-artifacts-directory)
- [Epistemic Closure Net Artifacts](#epistemic-closure-net-artifacts)
- [Scholarly Description](#scholarly-description)
- [How to Cite](#how-to-cite)
- [License](#license)

## Document Abstracts

### `General_Epistemic_Geometry_Book.pdf`

*General Epistemic Geometry* develops an operational theory of scientific knowledge under finite verification constraints. It formalizes continuous cGCNF semantics, geometric compilation, counting/volume semantics, complexity barriers, and epistemic curvature as a measurable syntax-semantics gap. The monograph then extends the framework to coherent-flow dynamics, differential-geometric and topological interfaces, and black-hole-relevant measurable phases, under the editorial rule: *Always extend, never reduce*.

### `Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf`

This paper introduces an auditable finite-bank methodology to certify BBH initial-data phase structure: common horizon, separate horizons, and finite-resource gray zones. It equips template space with an explicit metric, constructs epsilon-net banks, and proves transfer bounds from ideal semantics to finite certification through a modulus `omega(epsilon)`. It also provides Monte Carlo uncertainty quantification, an effective-Lipschitz estimation protocol, and a protocol-holonomy observable called the epistemic perihelion.

### `Epistemic_Geometry_of_Closure - Riveros.pdf`

This manuscript formalizes SCE-IM closure through three compatible layers: semantic (windowed volume / continuous `#SAT`), geometric-metric (curvature as an operational gap), and dynamic-thermodynamic (coherent flow via Lyapunov descent and Gibbs/MH exploration). It introduces zipper signatures as operational invariants and proves stability plus operational completeness with and without resource bounds. The closure regime is characterized in classes where the structure collapses to a merge tree.

### `Epistemic_Closure_Net - Riveros.pdf`

This work unifies SCE-IM closure with a closed epistemic kernel in a typed, expansive network formalism. The kernel layer integrates internal certification, theory atlases, holonomy obstructions, and meta-closure towers. Nodes and morphisms encode syntax, semantics, certificates, resources, refinements, and experimental harnesses under explicit compatibility constraints. Claims are evidence-typed (`[Proved]`, `[Model]`, `[Conjecture]`), non-closures are isolated as explicit conjectures, and experimental nodes are specified with auditable estimators, uncertainty quantification, and pre-registered falsification patterns.

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
|-- artifact/
|   `-- README.md
|-- figures/                       # generated outputs (created automatically)
|-- General_Epistemic_Geometry_Book.pdf
|-- Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf
|-- Epistemic_Geometry_of_Closure - Riveros.pdf
|-- Epistemic_Closure_Net - Riveros.pdf
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

These outputs are the reproducible computational artifacts associated with the closure-net analysis.

## Supplementary Artifacts Directory

The `artifact/` directory stores supplementary repository material not required for the core runtime pipeline (`code/`, `data/`, `figures/`) but relevant for auditability, reproducibility context, and extended technical support.

## Epistemic Closure Net Artifacts

`Epistemic_Closure_Net - Riveros.pdf` is accompanied by reproducible artifacts in this repository:

- `code/generate_figures.py` (produces `fig_dcrit_vs_q.png`, `fig_vgray_vs_tau.png`, `fig_vgray_vs_N.png`)
- `code/mercury_perihelion.py` (produces `mercury_perihelion.txt`)
- `data/jaramillo_lousto_table1.csv`
- `data/toy_boundary_error.csv`
- `figures/` (output directory for generated artifacts)
- `artifact/` (supplementary supporting material)

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
- Primary finite-bank paper: `Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf`
- Companion closure paper: `Epistemic_Geometry_of_Closure - Riveros.pdf`
- Companion closure-net paper: `Epistemic_Closure_Net - Riveros.pdf`

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

@misc{riveros2026finitebank,
  author       = {Riveros, Oscar},
  title        = {Finite-Bank Certification in Epistemic Geometry},
  year         = {2026},
  month        = feb,
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Finite-Bank_Certification_in_Epistemic_Geometry%20-%20Riveros.pdf}}
}

@misc{riveros2026closurenet,
  author       = {Riveros, Oscar},
  title        = {Epistemic Closure Net},
  year         = {2026},
  month        = feb,
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Epistemic_Closure_Net%20-%20Riveros.pdf}}
}
```

## License

Unless otherwise specified in individual files: **All rights reserved.**
