"""Minimal ADMST cosmology module

This is a lightweight, runnable subset of the ADMST-SCBC module suitable for
quick verification. It implements a simplified matter power spectrum, sigma8
calculator, a GW spectrum, and plotting helpers. Keep this file small so it
runs in the dev container without heavy dependencies.
"""
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Cosmological constants (Planck-like baseline)
H0 = 67.4  # km/s/Mpc
sigma8_Planck = 0.811


class SCBCParameters:
    def __init__(self):
        self.h = H0 / 100.0
        self.Omega_m = 0.315
        self.Omega_b = 0.049
        # ADMST-specific (compact)
        self.k_J = 6.5  # Mpc^-1
        self.A_GW = 3.2e-12
        self.f_p = 2e-3
        self.f_s = 20e-3

    def mass_spectrum(self, generation=12):
        m4 = 1.2e3
        beta = 1.8
        return m4 * ((np.arange(1, generation + 1)) / 4.0) ** beta


class SCBCCosmology:
    def __init__(self, params=None):
        self.params = params if params is not None else SCBCParameters()
        self.masses = self.params.mass_spectrum()

    def transfer_function(self, k):
        x = k / self.params.k_J
        return np.cos(x**2) / np.sqrt(1 + x**8)

    def growth_function(self, z):
        a = 1.0 / (1.0 + z)
        Om = self.params.Omega_m
        Omega_m_z = Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + (1 - Om))
        # Approximate Carroll, Press & Turner fit
        return (
            2.5
            * Omega_m_z
            * a
            / (
                Omega_m_z ** (4 / 7)
                - (1 - Omega_m_z)
                + (1 + Omega_m_z / 2) * (1 + (1 - Omega_m_z) / 70)
            )
        )

    def matter_power_spectrum(self, z=0):
        k = np.logspace(-3, 1.5, 400)
        # Simple Eisenstein-Hu like shape (compact approximation)
        q = k / (self.params.Omega_m * self.params.h**2 + 1e-12)
        T = np.log(1 + 2.34 * q) / (2.34 * q)
        T *= (1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** (
            -0.25
        )
        A_s = 2.1e-9
        n_s = 0.965
        Pk_LCDM = A_s * (k / 0.05) ** (n_s - 1) * T**2 * (2 * np.pi**2) / k**3
        D_z = self.growth_function(z) / self.growth_function(0)
        Pk_ADMST = Pk_LCDM * D_z**2 * self.transfer_function(k) ** 2
        return k, Pk_LCDM, Pk_ADMST

    def compute_sigma8(self):
        k, _, Pk = self.matter_power_spectrum(z=0)
        R = 8.0 / self.params.h
        x = k * R
        W = 3 * (np.sin(x) - x * np.cos(x)) / (x**3 + 1e-30)
        integrand = k**2 * Pk * W**2 / (2 * np.pi**2)
        sigma2 = np.trapezoid(integrand, k)
        return np.sqrt(np.abs(sigma2))

    def gw_spectrum(self, f):
        term1 = (f / self.params.f_p) ** 3 / (1 + (f / self.params.f_p) ** 2)
        term2 = (f / self.params.f_s) ** 8 / (1 + (f / self.params.f_s) ** 10)
        return self.params.A_GW * (term1 + term2)

    def plot_predictions(self, out_png="ADMST_predictions_min.png"):
        k, P_LCDM, P_ADMST = self.matter_power_spectrum()
        sigma8 = self.compute_sigma8()

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        ax = axes[0]
        ax.loglog(k, P_LCDM, label="LCDM")
        ax.loglog(k, P_ADMST, label="ADMST")
        ax.axvline(
            self.params.k_J, color="gray", ls="--", label=f"k_J={self.params.k_J}"
        )
        ax.set_xlabel("k [Mpc^-1]")
        ax.set_ylabel("P(k)")
        ax.legend()
        ax.grid(True)

        f = np.logspace(-9, 0, 400)
        ax2 = axes[1]
        ax2.loglog(f, self.gw_spectrum(f))
        ax2.set_xlabel("f [Hz]")
        ax2.set_ylabel("h^2 Omega_GW")
        ax2.grid(True)

        plt.suptitle(f"ADMST Minimal Predictions (sigma8={sigma8:.3f})")
        plt.tight_layout()
        fig.savefig(out_png, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return out_png
