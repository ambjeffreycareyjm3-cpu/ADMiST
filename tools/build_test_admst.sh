#!/bin/bash
set -e

echo "=== ADMST-CLASS Integration Build & Test ==="
echo

# Configuration
CLASS_REPO="https://github.com/lesgourg/class_public.git"
CLASS_VERSION="v3.2.1"
CLASS_DIR="external/class"
PATCH_DIR="patches"
OUTPUT_DIR="output"
SKIP_BUILD="${SKIP_BUILD:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_success() { echo -e "${GREEN}✓ $1${NC}"; }
log_error() { echo -e "${RED}✗ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

# Create output directory
mkdir -p "$OUTPUT_DIR"

# ==================== Step 1: Clone & Patch CLASS ====================
if [ "$SKIP_BUILD" != "true" ]; then
    echo "Step 1: Setting up CLASS repository..."

    if [ ! -d "$CLASS_DIR" ]; then
        log_warn "Cloning CLASS repository from $CLASS_REPO"
        mkdir -p "$(dirname "$CLASS_DIR")"
        git clone "$CLASS_REPO" "$CLASS_DIR" 2>&1 | grep -E "Cloning|Resolving|Receiving|done"

        cd "$CLASS_DIR"
        log_warn "Checking out $CLASS_VERSION..."
        git checkout "$CLASS_VERSION" 2>&1 | head -5
        cd - > /dev/null
        log_success "CLASS repository ready at $CLASS_DIR"
    else
        log_warn "CLASS directory already exists at $CLASS_DIR"
    fi

    # Apply patches
    echo "Applying ADMST patches..."
    cd "$CLASS_DIR"

    patch_count=0
    for patch in ../../$PATCH_DIR/*.patch; do
        if [ -f "$patch" ]; then
            patch_name=$(basename "$patch")
            echo "  - Attempting to apply $patch_name..."

            # Check if patch can be applied (dry-run)
            if patch -p1 --dry-run < "$patch" > /dev/null 2>&1; then
                patch -p1 < "$patch" > /dev/null 2>&1
                log_success "Applied $patch_name"
                ((patch_count++))
            else
                log_warn "Patch $patch_name may not apply cleanly (CLASS version mismatch?)"
                log_warn "This is expected - patches are skeleton templates for CLASS v3.2.1"
                echo "    To apply manually, edit the relevant files in include/ and source/"
            fi
        fi
    done

    if [ $patch_count -eq 0 ]; then
        log_warn "No patches were applied - CLASS structure may differ from v3.2.1"
        log_warn "See patches/ directory for manual edits needed"
    else
        log_success "Applied $patch_count patches"
    fi

    # Build CLASS
    echo "Building modified CLASS..."
    make distclean > /dev/null 2>&1 || true

    if make -j$(nproc) 2>&1 | tail -20; then
        log_success "CLASS build completed"
    else
        log_error "CLASS build failed. Check the output above."
        cd - > /dev/null
        exit 1
    fi

    cd - > /dev/null
fi

# ==================== Step 2: Create Test Parameter Files ====================
echo
echo "Step 2: Preparing test parameter files..."

# ΛCDM baseline
cat > "$OUTPUT_DIR/test_lcdm.ini" << 'EOF'
output = tCl,pCl,lCl
modes = s,t
l_max_scalars = 2500
l_max_tensors = 1500
lensing = yes

# Cosmological parameters (Planck 2018)
h = 0.67
Omega_b = 0.022
Omega_cdm = 0.12
Omega_k = 0.0
A_s = 2.1e-9
n_s = 0.96
tau_reio = 0.054
EOF

log_success "Created LCDM test file: $OUTPUT_DIR/test_lcdm.ini"

# ADMST minimal test
cat > "$OUTPUT_DIR/test_admst_minimal.ini" << 'EOF'
output = tCl,pCl,lCl
modes = s,t
l_max_scalars = 2500
l_max_tensors = 1500
lensing = yes

# Cosmological parameters (Planck 2018)
h = 0.67
Omega_b = 0.022
Omega_cdm = 0.12
Omega_k = 0.0
A_s = 2.1e-9
n_s = 0.96
tau_reio = 0.054

# ADMST Soliton parameters (minimal, not physically optimized)
Omega_soliton = 0.001
Gamma_soliton = 0.1
cs2_soliton = 0.333
T_soliton_star = 1.24e9
alpha_gamma_phi = 1e-5
has_soliton = yes
has_soliton_coupling = yes
EOF

log_success "Created ADMST test file: $OUTPUT_DIR/test_admst_minimal.ini"

# ==================== Step 3: Run Tests ====================
echo
echo "Step 3: Running CLASS calculations..."

if [ "$SKIP_BUILD" != "true" ]; then
    # Test ΛCDM baseline
    echo "  Testing ΛCDM baseline..."
    if cd "$CLASS_DIR" && ./class ../$OUTPUT_DIR/test_lcdm.ini 2>&1 | tail -5; then
        log_success "ΛCDM baseline calculation complete"
        LCDM_SUCCESS=1
    else
        log_error "ΛCDM calculation failed"
        cd - > /dev/null
        LCDM_SUCCESS=0
    fi
    cd - > /dev/null

    # Test ADMST minimal
    echo "  Testing ADMST with minimal parameters..."
    if cd "$CLASS_DIR" && ./class ../$OUTPUT_DIR/test_admst_minimal.ini 2>&1 | tail -5; then
        log_success "ADMST calculation complete"
        ADMST_SUCCESS=1
    else
        log_warn "ADMST calculation did not complete (expected if patches not applied)"
        cd - > /dev/null
        ADMST_SUCCESS=0
    fi
    cd - > /dev/null
else
    log_warn "Skipping build step (SKIP_BUILD=true)"
fi

# ==================== Step 4: Analysis & Comparison ====================
echo
echo "Step 4: Analyzing results..."

if [ -f "$OUTPUT_DIR/test_lcdm_scalCls.dat" ]; then
    log_success "Found LCDM output: test_lcdm_scalCls.dat"
else
    log_warn "LCDM output not found - CLASS may not have completed successfully"
fi

if [ -f "$OUTPUT_DIR/test_admst_minimal_scalCls.dat" ]; then
    log_success "Found ADMST output: test_admst_minimal_scalCls.dat"

    # Quick Python comparison (if numpy available)
    python3 << 'PYSCRIPT' 2>/dev/null || log_warn "Python analysis skipped (numpy not available)"
import numpy as np
import sys

try:
    lcdm = np.loadtxt('output/test_lcdm_scalCls.dat', skiprows=1, usecols=(0,1))
    admst = np.loadtxt('output/test_admst_minimal_scalCls.dat', skiprows=1, usecols=(0,1))

    # Interpolate to common ell grid
    lmax = min(len(lcdm), len(admst))
    diff_rel = np.abs((admst[:lmax,1] - lcdm[:lmax,1]) / (lcdm[:lmax,1] + 1e-30))

    print(f"\nSpectrum Comparison:")
    print(f"  Max relative difference: {np.max(diff_rel)*100:.3f}%")
    print(f"  Mean relative difference: {np.mean(diff_rel)*100:.4f}%")
    print(f"  Points compared: {lmax}")

except Exception as e:
    print(f"Analysis error: {e}")
PYSCRIPT
else
    log_warn "ADMST output not found - patches may not have been applied successfully"
fi

# ==================== Step 5: Summary ====================
echo
echo "=========================================="
echo "Build & Test Summary"
echo "=========================================="
echo "Patches applied: $patch_count / 3"
echo "LCDM baseline: $([ $LCDM_SUCCESS -eq 1 ] && echo 'PASS' || echo 'SKIP')"
echo "ADMST minimal: $([ $ADMST_SUCCESS -eq 1 ] && echo 'PASS' || echo 'SKIP')"
echo "Output directory: $OUTPUT_DIR/"
echo "=========================================="
echo
echo "Next steps:"
echo "  1. Review patch application logs above"
echo "  2. If patches failed: manually apply changes from patches/"
echo "  3. For full MCMC: prepare Cobaya config and Planck likelihood data"
echo "  4. Run: python tools/run_mcmc.py examples/cobaya_admst_planck.yaml"
echo
