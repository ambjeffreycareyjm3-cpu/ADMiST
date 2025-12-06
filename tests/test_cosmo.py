import numpy as np

from admst import SCBCCosmology, SCBCParameters


def test_imports_and_params():
    params = SCBCParameters()
    cosmo = SCBCCosmology(params)
    assert hasattr(cosmo, "params")
    assert params.h > 0


def test_mass_spectrum_monotonic():
    params = SCBCParameters()
    masses = params.mass_spectrum(12)
    assert np.all(np.diff(masses) > 0)


def test_transfer_function_finite():
    cosmo = SCBCCosmology()
    k = np.array([0.01, 0.1, 1.0, 10.0])
    T = cosmo.transfer_function(k)
    assert np.all(np.isfinite(T))


def test_sigma8_reasonable_range():
    cosmo = SCBCCosmology()
    s8 = cosmo.compute_sigma8()
    # sanity check: sigma8 should be positive and not absurd
    assert s8 > 0
    assert s8 < 5


def test_gw_spectrum_nonnegative():
    cosmo = SCBCCosmology()
    f = np.array([1e-9, 1e-6, 1e-3, 1e-1])
    Omega = cosmo.gw_spectrum(f)
    assert np.all(Omega >= 0)


def test_lab_scaling_structure():
    cosmo = SCBCCosmology()
    lab = cosmo.lab_scaling_predictions()
    assert "f_cosmic_pred" in lab
    assert "lab_peaks" in lab and isinstance(lab["lab_peaks"], dict)


def test_cmb_modulation_amplitude():
    cosmo = SCBCCosmology()
    ell = np.array([100, 300, 1000, 2000])
    mod = cosmo.cmb_damping_modulation(ell)
    # Values should be positive and not exceed modest amplification
    assert np.all(mod > 0)
    assert np.all(mod < 1.05)
