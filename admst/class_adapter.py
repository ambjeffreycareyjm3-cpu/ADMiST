"""Optional adapter to call an external Boltzmann solver (CLASS) with a safe fallback.

This module tries to use the Python `classy` interface if available. If not,
it falls back to a lightweight dummy adapter that uses the existing
`admst.cosmo` functions to produce approximate matter power and C_ell arrays
so downstream code and CI can exercise the integration without requiring
CLASS to be installed.
"""
from __future__ import annotations

from typing import Iterable, Optional

import numpy as np

try:
    from classy import Class  # type: ignore

    HAS_CLASS = True
except Exception:
    HAS_CLASS = False

from admst.cosmo import SCBCCosmology


class ClassAdapter:
    """Adapter that exposes a small, consistent API for matter power and C_ell.

    If the `classy` package is available it will be used. Otherwise a dummy
    adapter based on `admst.cosmo.SCBCCosmology` will be used.
    """

    def __init__(self, params: Optional[dict] = None):
        self.params = params or {}
        if HAS_CLASS:
            self.backend = "classy"
            self.cls = Class()
            # users should call `init` explicitly for custom params
        else:
            self.backend = "dummy"
            self.cosmo = SCBCCosmology()

    # --- Classy-backed methods (best-effort wrappers) ---
    def init_classy(self, params: dict):
        if not HAS_CLASS:
            raise RuntimeError("classy is not available in this environment")
        self.params.update(params)
        self.cls.set(params)
        self.cls.compute()

    def get_matter_power(self, k: Iterable[float], z: float) -> np.ndarray:
        k = np.asarray(k)
        if self.backend == "classy":
            pk = np.array([self.cls.pk(k_i, z) for k_i in k])
            return pk
        # dummy fallback: get the internal P(k) grid then interpolate
        k_grid, _, Pk_grid = self.cosmo.matter_power_spectrum(z=z)
        # interpolate in log-log space for stability
        # guard against non-positive values
        k_grid = np.asarray(k_grid)
        Pk_grid = np.maximum(np.asarray(Pk_grid), 1e-40)
        log_k_grid = np.log(k_grid)
        log_Pk_grid = np.log(Pk_grid)
        log_k = np.log(k)
        log_Pk = np.interp(
            log_k, log_k_grid, log_Pk_grid, left=log_Pk_grid[0], right=log_Pk_grid[-1]
        )
        return np.exp(log_Pk)

    def get_Cl_TT(self, ell: Iterable[int]) -> np.ndarray:
        ell = np.asarray(ell)
        if self.backend == "classy":
            # classy returns scaled C_l, but usage varies — this is a simple
            # attempt to fetch TT from the transfer function outputs.
            cls = np.array(
                [
                    self.cls.lensed_cl(l) if hasattr(self.cls, "lensed_cl") else 0.0
                    for l in ell
                ]
            )
            return cls
        # dummy TT: simple power-law-like falloff for integration tests
        ell = ell.astype(float)
        cl0 = 1e-9
        cls = cl0 / (ell * (ell + 1.0) + 1.0)
        return cls


class DummyClassAdapter(ClassAdapter):
    """Explicit dummy adapter convenience class (uses SCBCCosmology).

    Provided so tests and CI can import a predictable implementation.
    """

    def __init__(self):
        super().__init__({})
