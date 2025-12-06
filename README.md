# ADMiST

**ADMST-SCBC Cosmological Module**: Soliton gas model for dark matter, modified CMB, and lab-scale tests.

[![CI](https://github.com/ambjeffreycareyjm3-cpu/ADMiST/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ambjeffreycareyjm3-cpu/ADMiST/actions/workflows/ci.yml)

## Quick Start

### Using Docker (Recommended)

Reproducible environment with CLASS, Cobaya, and all dependencies:

```bash
# Automated setup (builds Docker image, ~5-10 min first run)
./tools/docker_build_and_test.sh

# Or manual setup
docker-compose up -d admst-class
docker-compose exec admst-class bash
```

See [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) for detailed instructions.

### Local Installation

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest  # Run tests
```

## Workflows

### Test ADMST Physics Module

```bash
python -c "from admst.cosmo import SCBCCosmology; c = SCBCCosmology(); print(f'σ8 = {c.compute_sigma8():.3f}')"
python run_analysis.py  # Generates plots
pytest tests/test_cosmo.py
```

### Integrate with CLASS & Planck

```bash
# Inside Docker container:
./tools/build_test_admst.sh        # Clone CLASS, apply patches, test
python tools/run_mcmc.py examples/cobaya_admst_planck.yaml  # Run MCMC
```

See [CLASS_INTEGRATION_README.md](CLASS_INTEGRATION_README.md) for physics details.

## Repository Structure

```
admst/
├── __init__.py
├── cosmo.py                    # Consolidated ADMST module (transfer functions, power spectra, etc.)
├── cosmo_min.py                # Minimal runner
└── class_adapter.py            # Python interface to CLASS (with dummy fallback)

tests/
├── test_cosmo.py               # Unit tests for physics calculations
├── test_class_adapter.py       # Tests for CLASS integration
└── conftest.py

tools/
├── build_test_admst.sh         # Clone, patch, build CLASS
├── patch_class.sh              # Patch helper
├── docker_build_and_test.sh    # Docker setup automation
├── run_mcmc.py                 # Cobaya MCMC runner
└── check_deprecated_numpy.py   # Linter for deprecated NumPy APIs

patches/
├── 01_background_soliton_complete.patch      # Soliton background evolution
├── 02_perturbations_soliton_complete.patch   # Soliton-photon coupling
└── 03_thermodynamics_soliton_complete.patch  # Enhanced optical depth

examples/
└── cobaya_admst_planck.yaml    # MCMC configuration with Planck likelihoods

.github/workflows/
└── ci.yml                      # GitHub Actions CI (tests + linting + pre-commit)

.pre-commit-config.yaml        # Local code quality checks
.githooks/pre-commit           # Pre-commit hooks repository

Dockerfile                     # Reproducible environment
docker-compose.yml             # Multi-service orchestration
```

## Features

- ✓ **Consolidated ADMST module** (`admst/cosmo.py`): Matter power, sigma8, GW spectrum, CMB damping, lab predictions
- ✓ **Unit tests & CI**: 9 tests, GitHub Actions, pre-commit hooks
- ✓ **CLASS integration**: Physics patches for soliton gas + CLASS adapter
- ✓ **MCMC ready**: Cobaya config with Planck likelihoods (requires data)
- ✓ **Docker reproducibility**: Build once, run anywhere
- ✓ **Deprecated-API checker**: Automated linting for NumPy changes

## Key Results

**Matter Power Spectrum:**
- Transfer function: $T(k) = \frac{\cos((k/k_J)^2)}{\sqrt{1+(k/k_J)^8}}$
- Growth function includes modified expansion history
- σ₈^ADMST vs σ₈^Planck: predictions testable against CMB

**CMB Modulation:**
- Visibility function: $g(\eta) = -\dot{\kappa} e^{-\kappa}$ with soliton coupling
- Damping modulation: $e^{-(ℓ/ℓ_D)^{1.7}} (1 + \beta_{\text{CMB}} \cos(2\pi ℓ/ℓ_{\text{osc}}))$

**Lab Scaling:**
- Predicts peak frequencies in kHz range for tabletop experiments
- Testable with ultracold atoms or superfluid helium

## Installation & Testing

### Requirements

- Python 3.10+
- NumPy, SciPy, Matplotlib
- pytest (for tests)
- CLASS v3.2.1 (for Boltzmann solver integration)
- Cobaya 3.3.1 (for MCMC)
- Docker (optional but recommended)

### Install ADMST Package

```bash
pip install -e .
```

### Run Tests Locally

```bash
pytest -v
```

### Run Pre-commit Checks

```bash
# Initial setup (one-time)
git config core.hooksPath .githooks
pre-commit install-hooks

# Run checks
pre-commit run --all-files
```

## Documentation

- **[CLASS_INTEGRATION_README.md](CLASS_INTEGRATION_README.md)** — Physics implementation, patch details, MCMC workflow
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** — Docker setup, troubleshooting
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Developer setup

## Physics Overview

**ADMST Model:**
- Early-universe soliton gas with production rate $\Gamma_s$
- Modified sound speed $c_s^2$ affects matter clustering
- Soliton-photon coupling $\alpha_{\gamma\Phi}$ leaves CMB imprint

**Observable Signatures:**
1. Matter power spectrum suppression on small scales (k > k_J)
2. Enhanced baryon acoustic oscillation phase shift
3. CMB temperature spectrum modulation with periodic features
4. Gravitational wave background from soliton dynamics
5. Lab-scale predictions: kHz-MHz frequencies, tabletop-scale wavelengths

**Testable Falsifications:**
- CMB-S4: High-ℓ constraints on modulation amplitude
- LISA: GW spectrum comparison
- Tabletop experiments: Direct searches for soliton signatures

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and workflow.

## License

[Specify your license - e.g., MIT, GPL-3.0]

## References

- CLASS: http://class-code.net/ (Blas et al., JCAP 2011)
- Cobaya: https://arxiv.org/abs/2101.04154
- ADMST paper: [arXiv reference] (submitted/preprint)
- Planck 2018: https://arxiv.org/abs/1807.06209

## Support & Issues

- GitHub Issues: [Report bugs and feature requests]
- Discussions: [Ask questions and share ideas]

```
# ADMiST
ADMST Validation Calculations
