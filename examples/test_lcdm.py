#!/usr/bin/env python3
"""Test ΛCDM baseline with CLASS via classy interface"""
import numpy as np
from classy import Class


def test_lcdm_baseline():
    """Verify CLASS can compute ΛCDM predictions"""
    print("Testing ΛCDM baseline with CLASS...")

    try:
        cosmo = Class()
        cosmo.set(
            {
                "output": "tCl,pCl,lCl",
                "l_max": 2500,
                "h": 0.67,
                "Omega_b": 0.022,
                "Omega_cdm": 0.12,
                "A_s": 2.1e-9,
                "n_s": 0.96,
                "tau_reio": 0.054,
            }
        )

        print("  Computing CLASS predictions...")
        cosmo.compute()

        # Get C_l values
        cls = cosmo.raw_cl(2500)
        l = cls["ell"][2:]  # Skip monopole and dipole
        tt = cls["tt"][2:]

        print(f"  ✓ Retrieved {len(l)} multipoles")
        print(f"  C_ℓ^TT at ℓ=100: {tt[98]:.3e}")
        print(f"  C_ℓ^TT at ℓ=1000: {tt[998]:.3e}")

        # Sanity checks
        assert tt[98] > 0, "C_ℓ at ℓ=100 is not positive"
        assert tt[998] > 0, "C_ℓ at ℓ=1000 is not positive"
        assert tt[98] > tt[998], "Peak not at expected location"

        print("  ✓ ΛCDM baseline test PASSED")

        cosmo.struct_cleanup()
        cosmo.empty()
        return True

    except Exception as e:
        print(f"  ✗ ΛCDM test FAILED: {e}")
        return False


if __name__ == "__main__":
    import sys

    success = test_lcdm_baseline()
    sys.exit(0 if success else 1)
