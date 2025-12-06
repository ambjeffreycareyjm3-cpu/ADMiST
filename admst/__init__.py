"""ADMST minimal package

This package provides a compact, runnable subset of the ADMST-SCBC cosmology
code for quick local verification and development. It is intentionally small and
meant as a scaffold you can extend.
"""

try:
	# Prefer full implementation if present
	from .cosmo import SCBCParameters, SCBCCosmology  # type: ignore
except Exception:
	from .cosmo_min import SCBCParameters, SCBCCosmology  # fallback

__all__ = ["SCBCParameters", "SCBCCosmology"]
