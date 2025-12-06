# CLASS Integration & ADMST Physics Patches

This directory contains the complete workflow to integrate ADMST soliton gas modifications into CLASS (Cosmic Linear Anisotropy Solving System) and run MCMC constraints with Planck likelihoods.

## Overview

The ADMST model modifies CLASS by adding:

1. **Background evolution** (`background.c`): Soliton energy density evolution with production/decay rates
2. **Perturbation equations** (`perturbations.c`): Soliton density contrast and velocity divergence with coupling to photons
3. **Thermodynamics** (`thermodynamics.c`): Soliton-photon scattering and enhanced optical depth

## Quick Start

### Option 1: Automated Build & Test (Recommended)

```bash
cd /workspaces/ADMiST

# Full workflow: clone CLASS, apply patches, run LCDM baseline and ADMST minimal test
./tools/build_test_admst.sh

# Or skip the build if you already have CLASS compiled
SKIP_BUILD=true ./tools/build_test_admst.sh
```

### Option 2: Manual Step-by-Step

```bash
# 1. Clone and patch CLASS
./tools/patch_class.sh

# 2. Build CLASS (inside external/class)
cd external/class
make -j4
cd ../..

# 3. Run LCDM baseline
./external/class/class output/test_lcdm.ini

# 4. Run ADMST minimal test
./external/class/class output/test_admst_minimal.ini
```

## Files

### Patch Files (`patches/`)

| File | Modifies | Purpose |
|------|----------|---------|
| `01_background_soliton_complete.patch` | `background.h`, `background.c` | Add soliton density parameters and evolution equations |
| `02_perturbations_soliton_complete.patch` | `perturbations.h`, `perturbations.c` | Add soliton perturbation hierarchy and photon coupling |
| `03_thermodynamics_soliton_complete.patch` | `thermodynamics.h`, `thermodynamics.c` | Enhanced optical depth from soliton-photon scattering |

### Tools (`tools/`)

| Script | Purpose |
|--------|---------|
| `patch_class.sh` | Clone CLASS v3.2.1 and attempt to apply patches |
| `build_test_admst.sh` | Full build, test, and analysis workflow (with logging) |
| `run_mcmc.py` | Run Cobaya MCMC with Planck likelihoods and ADMST parameters |

## Physics Implementation Details

### Background Evolution

The soliton energy density evolves as:

$$\frac{d\rho_s}{dt} + 3H\rho_s = \Gamma_s \rho_s \left(1 - \frac{\rho_s}{\rho_s^{\text{eq}}}\right)$$

where:
- $\Gamma_s$ is the production/decay rate
- $\rho_s^{\text{eq}} = \Omega_s^0 H_0^2 / a^3$ is the equilibrium density

**CLASS Implementation:**
```c
dy[pba->index_bi_rho_soliton] = -3.0 * H * rho_s + Gamma_eff * rho_s;
```

### Perturbation Equations

Soliton density contrast $\delta_s$ and velocity divergence $\theta_s$ obey:

$$\dot{\delta}_s + \theta_s = 0$$
$$\dot{\theta}_s + H\theta_s + c_s^2 k^2 \delta_s = 0$$

**Soliton-Photon Coupling:** Photon Boltzmann equation modified by source term:

$$S_s = \alpha F(k) (\delta_s + v_s)$$

where:
- $\alpha = \alpha_{\gamma\Phi}$ is the dimensionless coupling
- $F(k) = \frac{\cos((k/k_J)^2)}{\sqrt{1+(k/k_J)^8}}$ is the ADMST form factor

### Thermodynamics

Soliton-photon scattering enhances the optical depth:

$$\tau_s = \int_0^z \frac{d\tau}{dz'} dz' = \int_0^z n_s(z') \sigma_s(z') \frac{c}{H(z')} dz'$$

where:
- $n_s = \Omega_s^0 H_0^2 a^{-3} e^{-\Gamma_s t}$
- $\sigma_s = \alpha^2 \sigma_T F_T(T)$ is an enhanced Thomson-like cross-section
- $F_T$ is a temperature-dependent form factor

## Patch Application Issues

If patches don't apply cleanly:

1. **CLASS version mismatch:** Patches target CLASS v3.2.1. If a newer/older version is used, manual edits are needed.

2. **Manual application:**
   - Review the `.patch` file content
   - Locate corresponding functions in CLASS source
   - Add new struct members and function bodies as shown in patch comments

3. **Typical locations:**
   - `include/background.h` — add struct members after line ~200
   - `include/perturbations.h` — add struct members after line ~300
   - `include/thermodynamics.h` — add struct members after line ~100
   - `source/background.c` — add evolution code in `background_derivs()` function
   - `source/perturbations.c` — add coupling in `perturbations_sources()` and perturbation derivs
   - `source/thermodynamics.c` — add optical depth in `thermodynamics_ionization()` function

## MCMC Constraints

### Prerequisites

```bash
# Install dependencies
pip install cobaya camb classy pymultinest
# Download Planck 2018 likelihood data (requires clik/PLC)
# See: https://github.com/Cobaya/cobaya/wiki/Likelihoods-and-external-codes
```

### Run Short Test Chain

```bash
python tools/run_mcmc.py examples/cobaya_admst_planck.yaml
```

### Analyze Results

```python
import numpy as np
from getdist import plots, MCSamples

# Load chains (adjust path to your output)
samples = np.loadtxt("chains/admst_planck_1.txt")
names = ['Omega_b', 'Omega_cdm', 'h', 'n_s', 'A_s', 'tau_reio',
         'Omega_soliton', 'Gamma_soliton', 'cs2_soliton']

gd = MCSamples(samples=samples[:, :-1], names=names)

# Corner plot
g = plots.get_subplot_plotter()
g.triangle_plot(gd, filled=True)
g.export('results/corner.pdf')

# Compute Δχ² relative to ΛCDM
# (requires running both ΛCDM and ADMST with same likelihood)
```

## Expected Outputs

After running `build_test_admst.sh`:

```
output/
├── test_lcdm.ini                  # ΛCDM parameter file
├── test_admst_minimal.ini         # ADMST parameter file
├── test_lcdm_scalCls.dat          # LCDM TT/EE/TE spectra
├── test_lcdm_tensors.dat          # LCDM tensor perturbations
├── test_admst_minimal_scalCls.dat # ADMST spectra
└── test_admst_minimal_tensors.dat # ADMST tensors
```

**Comparisons:**
- Relative differences in TT spectrum should be <1% for minimal ADMST parameters
- Larger differences expected at high-ℓ if soliton-photon coupling is significant
- Physics predictions can be validated by comparing analytical expectations

## Next Steps

1. **Validate against observational constraints:**
   - Compare predicted vs Planck 2018 C_ℓ values
   - Run MCMC to compute Δχ² and parameter constraints

2. **Explore parameter space:**
   - Vary Ω_soliton, Γ_s, c_s², α_{γΦ}
   - Identify degenerate directions with standard CDM parameters

3. **Prepare publication:**
   - Document physics modifications (equations, indices)
   - Include example chains and corner plots
   - Publish code on GitHub + Zenodo

## References

- CLASS: http://class-code.net/
- Cobaya: https://cobaya.readthedocs.io/
- Planck 2018 likelihood: https://wiki.cosmos.esa.int/planckpla2018/index.php
- ADMST Paper: [arxiv reference]

## Troubleshooting

**Q: Patches don't apply**
A: CLASS structure may differ. See "Patch Application Issues" section above.

**Q: Build fails with "undefined reference"**
A: Check that all patch changes were applied. Review `make` output for missing symbols.

**Q: MCMC doesn't start**
A: Verify Planck likelihood data is installed. Run `python -c "from cobaya import likelihoods"` to check.

**Q: Parameter file error in CLASS**
A: Ensure parameter names match CLASS input parsing (e.g., `Omega_soliton` vs `omega_soliton`).
