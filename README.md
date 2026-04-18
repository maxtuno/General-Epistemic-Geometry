# General Epistemic Geometry

Canonical repository for the *General Epistemic Geometry* research corpus by **Oscar Riveros**.

This repository serves two complementary purposes:

1. It is the archival home of the canonical PDFs that define the framework and its companion extensions.
2. It provides the reproducible computational bundle for the scripts, data tables, and generated figures associated with the repository's quantitative artifacts.

Core canonical edition: **February 2026**.
Repository extensions included here: companion documents and root manuscripts, including [`Fisica-Riveriana.pdf`](./Fisica-Riveriana.pdf), [`Autorreferencia Segura - Riveros.pdf`](<./Autorreferencia Segura - Riveros.pdf>), and [`Meta-Algoritmos - Riveros.pdf`](<./Meta-Algoritmos - Riveros.pdf>).

## Quick Links

- Canonical monograph: [General_Epistemic_Geometry_Book.pdf](./General_Epistemic_Geometry_Book.pdf)
- Finite-bank certification paper: [Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf](<./Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf>)
- Closure paper: [Epistemic_Geometry_of_Closure - Riveros.pdf](<./Epistemic_Geometry_of_Closure - Riveros.pdf>)
- Closure-net paper: [Epistemic_Closure_Net - Riveros.pdf](<./Epistemic_Closure_Net - Riveros.pdf>)
- Observer geometry and holonomy paper: [Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions - Riveros.pdf](<./Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions - Riveros.pdf>)
- Diagrammatic language paper: [egdl_epistemic_geometry - Riveros.pdf](<./egdl_epistemic_geometry - Riveros.pdf>)
- *Fisica Riveriana* treatise (Spanish): [Fisica-Riveriana.pdf](./Fisica-Riveriana.pdf)
- Safe self-reference paper (Spanish): [Autorreferencia Segura - Riveros.pdf](<./Autorreferencia Segura - Riveros.pdf>)
- Meta-algorithms formalization paper (Spanish): [Meta-Algoritmos - Riveros.pdf](<./Meta-Algoritmos - Riveros.pdf>)
- TCOC formalization paper (Spanish): [tcoc - Riveros.pdf](<./tcoc - Riveros.pdf>)
- Citation metadata: [CITATION.cff](./CITATION.cff)
- Supplementary artifacts note: [artifact/README.md](./artifact/README.md)
- Foundational papers repository: [maxtuno/EPISTEMIC-GEOMETRY](https://github.com/maxtuno/EPISTEMIC-GEOMETRY)
- Academia page: [General Epistemic Geometry](https://www.academia.edu/164594131/General_Epistemic_Geometry)
- Academia page: [Epistemic Geometry of Closure](https://www.academia.edu/164640745/Epistemic_Geometry_of_Closure_SCE_IM_Coherent_Flow_Stability_and_Operational_Completeness)

## Table of Contents

- [Repository Scope](#repository-scope)
- [Research Corpus](#research-corpus)
- [Repository Layout](#repository-layout)
- [Reproduce the Computational Artifacts](#reproduce-the-computational-artifacts)
- [Script Reference](#script-reference)
- [Data Assets](#data-assets)
- [Generated Outputs](#generated-outputs)
- [Supplementary Material](#supplementary-material)
- [Scholarly Description](#scholarly-description)
- [How to Cite](#how-to-cite)
- [License](#license)

## Repository Scope

This repository is not only a document archive. Its structure is intentionally split between canonical scholarship and reproducible support material.

- The repository root stores the canonical PDFs that define the framework, its closure theory, finite-bank certification machinery, observer-geometry extensions, diagrammatic formalism, the later *Fisica Riveriana* synthesis, the safe-self-reference extension for dynamic state families, the meta-algorithmic manuscript on executable recursive branching, hierarchical compilation, and protocol-indexed hardness, and the TCOC formalization manuscript on exact optimization-preserving representations and complexity transport.
- [`code/`](./code) contains the scripts used to regenerate the repository's computational figures and benchmark text output.
- [`data/`](./data) contains the CSV inputs consumed by the reproducibility scripts.
- [`figures/`](./figures) is the output directory for regenerated figures and benchmark files; it is tracked with a placeholder so the path exists in a clean checkout.
- [`artifact/`](./artifact) stores supplementary material that supports traceability and auditability without being part of the minimal runtime pipeline.
- [`CITATION.cff`](./CITATION.cff) and [`LICENSE.md`](./LICENSE.md) provide repository-level metadata.

The current computational pipeline directly supports the closure-net / finite-bank artifact set. The root PDFs, however, represent the full scholarly corpus hosted by the repository.

## Research Corpus

### `General_Epistemic_Geometry_Book.pdf`

*General Epistemic Geometry* is the canonical monograph of the program. It develops an operational theory of scientific knowledge under finite verification constraints, formalizing continuous cGCNF semantics, geometric compilation, counting and volume semantics, complexity barriers, and epistemic curvature as a measurable syntax-semantics gap. The monograph then extends the framework toward coherent-flow dynamics, differential-geometric and topological interfaces, and black-hole-relevant measurable phases under the editorial rule: *Always extend, never reduce*.

### `Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf`

This paper introduces an auditable finite-bank methodology for certifying BBH initial-data phase structure: common horizon, separate horizons, and finite-resource gray zones. It equips template space with an explicit metric, constructs epsilon-net banks, and proves transfer bounds from ideal semantics to finite certification through a modulus `omega(epsilon)`. It also supplies Monte Carlo uncertainty quantification, an effective-Lipschitz estimation protocol, and a protocol-holonomy observable called the epistemic perihelion.

### `Epistemic_Geometry_of_Closure - Riveros.pdf`

This manuscript formalizes SCE-IM closure through three compatible layers: semantic (windowed volume / continuous `#SAT`), geometric-metric (curvature as an operational gap), and dynamic-thermodynamic (coherent flow via Lyapunov descent and Gibbs / MH exploration). It introduces zipper signatures as operational invariants and proves stability plus operational completeness with and without resource bounds. The closure regime is characterized in classes where the structure collapses to a merge tree.

### `Epistemic_Closure_Net - Riveros.pdf`

This work unifies SCE-IM closure with a closed epistemic kernel in a typed, expansive network formalism. The kernel layer integrates internal certification, theory atlases, holonomy obstructions, and meta-closure towers. Nodes and morphisms encode syntax, semantics, certificates, resources, refinements, and experimental harnesses under explicit compatibility constraints, while claims are evidence-typed (`[Proved]`, `[Model]`, `[Conjecture]`) and non-closures are isolated as explicit conjectures.

### `Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions - Riveros.pdf`

This companion paper develops a categorical and probabilistic formalism for observer-state geometry and protocol dependence. It defines exact semantic identity relative to separating query families, introduces agreement radii and agreement moduli, formalizes abstract and realized protocol holonomy, derives finite-bank convergence under transfer moduli, and presents a conditional Yang-Mills reduction in which the mass-gap problem is recast as a spectral persistence question for UV/IR closure obstructions.

### `egdl_epistemic_geometry - Riveros.pdf`

*A Diagrammatic Language for Epistemic Geometry* specifies EGDL, a visual formalism for expressing metric interfaces between syntax and semantics, curvature as a representation gap, refinement dynamics, closure nets, finite-bank certification, coherent flows, and holonomy obstructions. The document is organized as definitions, axioms, lemmas and theorem schemas, invariants, and structural predictions, and it includes a compact TikZ micro-library for publication-ready diagrams.

### `Fisica-Riveriana.pdf`

*Fisica Riveriana* is a Spanish-language extension that fuses the operator, variational, and spectral line with the phenomenological, inferential, and multichannel line into a single architecture. It pushes the framework into renormalization, interface scattering, anomalies, non-equilibrium dynamics, fermionic localization, phase cosmology, finite-bank certification, and precision falsification protocols. In the language of the text itself, the treatise is built around a double closure: partial mathematical closure and partial phenomenological closure under finite resources.

### `Autorreferencia Segura - Riveros.pdf`

*Autorreferencia segura en familias dinámicas de estados* is a Spanish-language March 2026 companion paper on safe self-reference in time-varying state spaces. It introduces an effective load `L_eff` that combines self-reference speed and constitutive drift against an integration capacity `Gamma`, and proves local critical velocities, a uniformity theorem for class-wide safe bounds, reachable-divergence criteria, invariance of moving safe tubes through Lyapunov-ISS control across fibers, no-return horizons, and finite-radius bounds under minimal protocol holonomy.

### `Meta-Algoritmos - Riveros.pdf`

*Meta-Algoritmos* is a Spanish-language formal manuscript on executable meta-algorithms, certified branching, hierarchical compilation, and complexity transport across levels. It develops a rigorous core with existence/uniqueness and global-correctness results for detector-guided recursive procedures, distinguishes pointwise from uniform hierarchical complexity, and then adds a compatible protocol-process extension in which hardness is indexed by regime, agency, and protocol rather than treated as absolute.

### `tcoc - Riveros.pdf`

*Teoría de Conservación de Óptimos y Complejidad* is the Spanish-language formal TCOC manuscript treated in this repository as a canonical root paper. It axiomatizes exact optimization-preserving representations, correct optimal support, strong exactness, affine equivalence, typed transport between representations, linear existence criteria, and formal obstruction principles for representation-based complexity transfer. Its final sections isolate sufficient conditions under which a polynomial optimization bridge on the relaxed side would transfer to the original combinatorial family, yielding a clean internal scheme toward a `P = NP` consequence when coupled to an NP-complete decision companion.

## Repository Layout

```text
.
|-- artifact/
|   `-- README.md
|-- code/
|   |-- generate_figures.py
|   |-- mercury_perihelion.py
|   `-- requirements.txt
|-- data/
|   |-- jaramillo_lousto_table1.csv
|   `-- toy_boundary_error.csv
|-- figures/
|   `-- .gitkeep
|-- CITATION.cff
|-- Autorreferencia Segura - Riveros.pdf
|-- Epistemic_Closure_Net - Riveros.pdf
|-- Epistemic_Geometry_of_Closure - Riveros.pdf
|-- Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf
|-- Fisica-Riveriana.pdf
|-- General_Epistemic_Geometry_Book.pdf
|-- LICENSE.md
|-- Meta-Algoritmos - Riveros.pdf
|-- Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions - Riveros.pdf
|-- egdl_epistemic_geometry - Riveros.pdf
|-- tcoc - Riveros.pdf
`-- README.md
````

## Reproduce the Computational Artifacts

Run from the repository root. A recent Python 3 environment is recommended.

Dependencies listed in [`code/requirements.txt`](./code/requirements.txt):

* `numpy`
* `pandas`
* `matplotlib`

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
python code/generate_figures.py --data-dir data --out-dir figures
python code/mercury_perihelion.py --out-dir figures
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r code/requirements.txt
python code/generate_figures.py --data-dir data --out-dir figures
python code/mercury_perihelion.py --out-dir figures
```

## Script Reference

### `python code/generate_figures.py --help`

Reads the CSV inputs in [`data/`](./data), regenerates the repository's figure set, and writes PNG outputs to [`figures/`](./figures).

* `--data-dir`: directory containing the repository CSV inputs
* `--input`: optional explicit main CSV path; defaults to `data/jaramillo_lousto_table1.csv`
* `--boundary-error`: optional explicit boundary-error CSV path; defaults to `data/toy_boundary_error.csv`
* `--out-dir`: output directory for generated figures
* `--seed`: random seed for the toy Monte Carlo model
* `--mc`: number of Monte Carlo samples used in the gray-zone estimate
* `--data`: legacy alias for the main CSV path
* `--outdir`: legacy alias for the output directory

Example:

```bash
python code/generate_figures.py --data-dir data --out-dir figures --seed 0
```

### `python code/mercury_perihelion.py --help`

Computes a deterministic GR perihelion-precession benchmark for Mercury and writes a text artifact to [`figures/`](./figures).

* `--out-dir`: directory where `mercury_perihelion.txt` is written
* `--output`: optional explicit output path
* `--seed`: accepted for CLI consistency; not used in the calculation

Example:

```bash
python code/mercury_perihelion.py --out-dir figures
```

## Data Assets

### `data/jaramillo_lousto_table1.csv`

Critical-separation table with fields `q_M2_over_M1`, `d_crit`, and `d_crit_over_Mtot`. The figure-generation script uses this file for `fig_dcrit_vs_q.png` and for interpolation in the toy gray-zone model.

### `data/toy_boundary_error.csv`

Toy boundary-bank size versus sup-norm error table with fields `N_boundary_points` and `sup_norm_boundary_error`. The figure-generation script uses this file for `fig_vgray_vs_N.png`.

Both scripts resolve their defaults from repository-relative paths, so no hard-coded absolute paths are required.

## Generated Outputs

When the reproducibility scripts are executed, the following artifacts are written to [`figures/`](./figures):

* `figures/fig_dcrit_vs_q.png`
* `figures/fig_vgray_vs_tau.png`
* `figures/fig_vgray_vs_N.png`
* `figures/mercury_perihelion.txt`

These outputs are the repository's reproducible computational companions to the closure-net / finite-bank materials.

## Supplementary Material

The [`artifact/`](./artifact) directory stores supporting material that is relevant for auditability, reproducibility context, and extended technical support, but is not required for the minimal runtime path defined by [`code/`](./code), [`data/`](./data), and [`figures/`](./figures). See [`artifact/README.md`](./artifact/README.md) for the directory note.

## Scholarly Description

Across the monograph and companion papers, the corpus advances a unified program in which the syntax-semantics gap is treated as measurable geometry under finite verification resources.

Its recurrent structural themes are:

1. continuous geometric semantics for expressive scientific descriptions;
2. refinement operators and coherent flows that improve or stabilize representational fit;
3. epistemic curvature as a measurable gap between syntactic constructions and semantic targets;
4. closure, gray zones, and finite-bank transfer as operational notions of partial certification;
5. atlas, protocol, and observer geometry as higher-order sources of obstruction and holonomy;
6. safe self-reference, viability horizons, and moving safe tubes in dynamically varying state families;
7. physical and phenomenological extensions in which interface structure, spectrum, fermionic localization, and multichannel inference become part of one continuous research architecture;
8. exact optimization-preserving representations and typed complexity transport, culminating in the TCOC formalization of when relaxation-side polynomial solvability can and cannot be transferred back to the original discrete family;
9. executable meta-algorithms, certified branching, hierarchical compilation by levels, and regime/protocol-indexed hardness in recursive problem solving.

Editorial principle retained across the corpus:

> Always extend, never reduce.

## How to Cite

For repository-level citation, use [`CITATION.cff`](./CITATION.cff). For document-level citation, cite the PDF most directly used.

Primary canonical references in this repository:

* `General_Epistemic_Geometry_Book.pdf`
* `Finite-Bank_Certification_in_Epistemic_Geometry - Riveros.pdf`
* `Epistemic_Geometry_of_Closure - Riveros.pdf`
* `Epistemic_Closure_Net - Riveros.pdf`
* `Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions - Riveros.pdf`
* `egdl_epistemic_geometry - Riveros.pdf`
* `Fisica-Riveriana.pdf`
* `Autorreferencia Segura - Riveros.pdf`
* `Meta-Algoritmos - Riveros.pdf`
* `tcoc - Riveros.pdf`

Minimal BibTeX:

```bibtex
@misc{riveros2026geg,
  author       = {Riveros, Oscar},
  title        = {General Epistemic Geometry},
  year         = {2026},
  note         = {Canonical monograph PDF in repository root},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/General_Epistemic_Geometry_Book.pdf}}
}

@misc{riveros2026finitebank,
  author       = {Riveros, Oscar},
  title        = {Finite-Bank Certification in Epistemic Geometry},
  year         = {2026},
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Finite-Bank_Certification_in_Epistemic_Geometry%20-%20Riveros.pdf}}
}

@misc{riveros2026closure,
  author       = {Riveros, Oscar},
  title        = {Epistemic Geometry of Closure},
  year         = {2026},
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Epistemic_Geometry_of_Closure%20-%20Riveros.pdf}}
}

@misc{riveros2026closurenet,
  author       = {Riveros, Oscar},
  title        = {Epistemic Closure Net},
  year         = {2026},
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Epistemic_Closure_Net%20-%20Riveros.pdf}}
}

@misc{riveros2026observergeometry,
  author       = {Riveros, Oscar},
  title        = {Physical Observer Geometry, Protocol Holonomy, Order by Non-Closure, and Spectral Obstructions},
  year         = {2026},
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Physical_Observer_Geometry__Protocol_Holonomy__Order_by_Non-Closure__and_Spectral_Obstructions%20-%20Riveros.pdf}}
}

@misc{riveros2026egdl,
  author       = {Riveros, Oscar},
  title        = {A Diagrammatic Language for Epistemic Geometry},
  year         = {2026},
  note         = {Canonical root PDF},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/egdl_epistemic_geometry%20-%20Riveros.pdf}}
}

@misc{riveros2026fisicariveriana,
  author       = {Riveros, Oscar},
  title        = {Fisica Riveriana: geometria, espectro, fermiones, cosmologia, renormalizacion y fenomenologia de precision},
  year         = {2026},
  note         = {Canonical root PDF; Spanish-language extension dated March 20, 2026},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Fisica-Riveriana.pdf}}
}

@misc{riveros2026autorreferenciasegura,
  author       = {Riveros, Oscar},
  title        = {Autorreferencia segura en familias dinámicas de estados},
  year         = {2026},
  note         = {Canonical root PDF; Spanish-language companion dated March 2026},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Autorreferencia%20Segura%20-%20Riveros.pdf}}
}

@misc{riveros2026metaalgoritmos,
  author       = {Riveros, Oscar},
  title        = {Meta-Algoritmos},
  year         = {2026},
  note         = {Canonical root PDF; Spanish-language formalization of executable meta-algorithms, certified branching, hierarchical compilation, and protocol-indexed hardness},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/Meta-Algoritmos%20-%20Riveros.pdf}}
}

@misc{riveros2026tcoc,
  author       = {Riveros, Oscar},
  title        = {Teoría de Conservación de Óptimos y Complejidad},
  year         = {2026},
  note         = {Canonical root PDF; Spanish-language formalization of TCOC},
  howpublished = {\url{https://github.com/maxtuno/General-Epistemic-Geometry/blob/main/tcoc%20-%20Riveros.pdf}}
}
```

## License

Unless otherwise specified in individual files: **All rights reserved.**
