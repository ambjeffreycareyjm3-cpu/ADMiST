import numpy as np

from admst.class_adapter import DummyClassAdapter, ClassAdapter


def test_dummy_adapter_matter_power_shape():
    adapter = DummyClassAdapter()
    k = np.logspace(-3, 1, 16)
    p = adapter.get_matter_power(k, z=0.0)
    assert p.shape == k.shape
    assert np.all(p >= 0)


def test_class_adapter_interface_fallback():
    adapter = ClassAdapter()
    # in environments without classy this should be the dummy backend
    k = np.linspace(0.001, 10.0, 8)
    p = adapter.get_matter_power(k, z=0.0)
    assert p.shape == k.shape

    ell = np.arange(2, 60)
    cl = adapter.get_Cl_TT(ell)
    assert cl.shape == ell.shape
    assert np.all(cl >= 0)
