"""Full ADMST-SCBC cosmology module (consolidated)

This file consolidates the ADMST-SCBC module into a single, runnable Python
module. It implements parameter definitions, matter power spectrum, sigma8
calculation, GW spectrum, CMB damping modulation, BBN Neff estimate, lab
scaling, plotting utilities, and a top-level runner `run_corrected_analysis()`.

This is intended for development and verification. For production workflows you
should split functionality into tests and smaller modules.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Basic physical constants / Planck baseline
Mpc = 3.086e22  # meters
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 2.99792458e8  # m/s
H0 = 67.4  # km/s/Mpc (Planck 2018)
Omega_m = 0.315
Omega_b = 0.049
sigma8_Planck = 0.811


class SCBCParameters:
    def __init__(self):
        # Core ADMST parameters (compact)
        self.N_dim = 2
        self.R_curv = 1e-6  # m
        self.Lambda_b = 1e3  # GeV
        self.g_star_extra = 28.0
        self.theta_mix = 0.1

        # Derived / phenomenological
        self.m_DM = 8.7e-9  # GeV
        self.T_star = 1.24  # GeV
        self.m4 = 1.2e3  # GeV (4th generation)
        self.A_GW = 3.2e-12
        self.f_p = 2e-3  # Hz
        self.f_s = 20e-3  # Hz

        # SCBC parameters
        self.beta_CMB = 0.01
        self.ell_osc = 300
        self.k_J = 6.5  # Mpc^-1

        # Cosmology
        self.h = H0 / 100.0
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.sigma8_Planck = sigma8_Planck

    def mass_spectrum(self, generation=12):
        beta = 1.8
        return self.m4 * ((np.arange(1, generation+1)) / 4.0) ** beta


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
        return 2.5 * Omega_m_z * a / (
            Omega_m_z ** (4.0 / 7.0)
            - (1 - Omega_m_z)
            + (1 + Omega_m_z / 2.0) * (1 + (1 - Omega_m_z) / 70.0)
        )

    def matter_power_spectrum(self, z=0, nk=500):
        k = np.logspace(-3, 1.5, nk)  # Mpc^-1

        # Eisenstein & Hu style fit (compact)
        q = k / (self.params.Omega_m * self.params.h ** 2 + 1e-12)
        T = np.log(1 + 2.34 * q) / (2.34 * q)
        T *= (1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** (-0.25)

        # Primordial normalization (approx)
        A_s = 2.1e-9
        n_s = 0.965
        Pk_LCDM = A_s * (k / 0.05) ** (n_s - 1) * T ** 2 * (2 * np.pi ** 2) / k ** 3

        D_z = self.growth_function(z) / self.growth_function(0)
        Pk_ADMST = Pk_LCDM * D_z ** 2 * self.transfer_function(k) ** 2

        return k, Pk_LCDM, Pk_ADMST

    def compute_sigma8(self):
        k, _, Pk = self.matter_power_spectrum(z=0)
        R = 8.0 / self.params.h
        x = k * R
        W = 3 * (np.sin(x) - x * np.cos(x)) / (x ** 3 + 1e-30)
        integrand = k ** 2 * Pk * W ** 2 / (2 * np.pi ** 2)
        sigma2 = np.trapezoid(integrand, k)
        return float(np.sqrt(np.abs(sigma2)))

    def gw_spectrum(self, f):
        term1 = (f / self.params.f_p) ** 3 / (1 + (f / self.params.f_p) ** 2)
        term2 = (f / self.params.f_s) ** 8 / (1 + (f / self.params.f_s) ** 10)
        return self.params.A_GW * (term1 + term2)

    def cmb_damping_modulation(self, ell):
        ell_D = 2000.0
        eps = self.params.beta_CMB
        return np.exp(- (ell / ell_D) ** 1.7) * (1 + eps * np.cos(2 * np.pi * ell / self.params.ell_osc))

    def compute_hubble(self):
        # Simple scaling due to reduced sound horizon
        r_d_LCDM = 147.0
        r_d_ADMST = r_d_LCDM * 0.96
        H0_ADMST = H0 * (r_d_LCDM / r_d_ADMST)
        return H0_ADMST

    def bbn_neff(self):
        delta_g = self.params.g_star_extra
        T_nu = 1.95  # MeV
        delta_Neff = (4.0 / 7.0) * (delta_g / 2.0) * (self.params.T_star * 1000.0 / T_nu) ** 4 * np.exp(-4.0)
        return 3.046 + min(delta_Neff, 0.12)

    def lab_scaling_predictions(self):
        f_lab = 1e3
        L_lab = 1.0
        T_lab = 300.0
        m_lab = 0.931

        R_bubble = 9.461e15
        T_star_K = self.params.T_star * 1.16e13
        m_cosmic = self.params.m4

        L_ratio = L_lab / R_bubble
        T_ratio = np.sqrt(T_lab / T_star_K)
        m_ratio = np.sqrt(m_lab / m_cosmic)

        f_cosmic_pred = f_lab * L_ratio * T_ratio * m_ratio

        return {
            'f_cosmic_pred': f_cosmic_pred,
            'f_cosmic_ADMST': self.params.f_p,
            'scaling_accuracy': f_cosmic_pred / self.params.f_p,
            'lab_peaks': {'primary': f_lab, 'secondary': f_lab * 10, 'tertiary': f_lab * 100},
        }

    def plot_predictions(self, out_png='ADMST_corrected_predictions.png'):
        k, P_LCDM, P_ADMST = self.matter_power_spectrum()
        sigma8_ADMST = self.compute_sigma8()

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        ax1 = axes[0, 0]
        ax1.loglog(k, P_LCDM, 'b-', label=r'$\Lambda$CDM', alpha=0.7)
        ax1.loglog(k, P_ADMST, 'r-', label='ADMST', linewidth=2)
        ax1.axvline(self.params.k_J, color='g', ls='--', alpha=0.5, label=f'k_J={self.params.k_J}')
        ax1.set_xlabel('k [Mpc$^{-1}$]')
        ax1.set_ylabel('P(k)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_title(f'Matter Power Spectrum ($\\sigma_8^{{ADMST}}={sigma8_ADMST:.3f}$)')

        ax2 = axes[0, 1]
        ell = np.arange(2, 3000)
        C_ell_mod = self.cmb_damping_modulation(ell)
        ax2.semilogx(ell, C_ell_mod, 'purple', linewidth=2)
        ax2.axhline(1.0, color='k', alpha=0.3)
        ax2.axvline(self.params.ell_osc, color='b', ls='--', alpha=0.5, label=f'ell_osc={self.params.ell_osc}')
        ax2.set_xlabel('Multipole l')
        ax2.set_ylabel('Modulation')
        ax2.set_ylim(0.99, 1.01)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_title('CMB Damping Tail Modulation')

        ax3 = axes[1, 0]
        f = np.logspace(-9, 0, 1000)
        Omega_GW = self.gw_spectrum(f)
        ax3.loglog(f, Omega_GW, 'darkorange', linewidth=2)
        ax3.axvline(self.params.f_p, color='b', ls='--', label=f'{self.params.f_p*1e3:.1f} mHz')
        ax3.axvline(self.params.f_s, color='r', ls='--', label=f'{self.params.f_s*1e3:.1f} mHz')
        ax3.fill_between([1e-9, 1e-7], 1e-15, 1e-8, alpha=0.2, label='NANOGrav')
        ax3.fill_between([1e-4, 1e-1], 1e-15, 1e-10, alpha=0.1, label='LISA')
        ax3.set_xlabel('f [Hz]')
        ax3.set_ylabel(r'$h^2\Omega_{GW}$')
        ax3.set_xlim(1e-9, 1)
        ax3.set_ylim(1e-16, 1e-8)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_title('Gravitational Wave Spectrum')

        ax4 = axes[1, 1]
        gens = np.arange(1, 13)
        masses = self.masses
        ax4.plot(gens[:3], masses[:3] / 1000.0, 'go', markersize=10, label='Known')
        ax4.plot(gens[3:], masses[3:] / 1000.0, 'ro', markersize=8, label='Predicted')
        ax4.plot(gens, masses / 1000.0, 'k-', alpha=0.3)
        ax4.axhline(0.8, color='gray', ls='--', alpha=0.5, label='LHC excluded')
        ax4.set_xlabel('Generation')
        ax4.set_ylabel('Mass [TeV]')
        ax4.set_yscale('log')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_title('12-Generation Mass Spectrum')

        plt.tight_layout()
        fig.savefig(out_png, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return out_png


def run_corrected_analysis():
    scbc = SCBCCosmology()

    k, Pk_LCDM, Pk_ADMST = scbc.matter_power_spectrum()
    sigma8_ADMST = scbc.compute_sigma8()

    ell = np.arange(2, 3000)
    C_ell_mod = scbc.cmb_damping_modulation(ell)

    f = np.logspace(-9, 0, 1000)
    Omega_GW = scbc.gw_spectrum(f)

    lab_pred = scbc.lab_scaling_predictions()

    out_png = scbc.plot_predictions()

    # Print a compact summary
    print('\n' + '=' * 60)
    print('CORRECTED ADMST PREDICTIONS (minimal run)')
    print('=' * 60)
    print(f'  sigma8 (Planck):  {sigma8_Planck:.3f}')
    print(f'  sigma8 (ADMST):   {sigma8_ADMST:.3f}')
    print(f'  H0 (Planck):      {H0:.1f} km/s/Mpc')
    print(f'  H0 (ADMST):       {scbc.compute_hubble():.1f} km/s/Mpc')
    print(f'  Delta Neff (BBN): {scbc.bbn_neff()-3.046:.3f}')
    print(f"  Lab f_cosmic_pred: {lab_pred['f_cosmic_pred']:.2e} Hz")
    print(f'  Plot saved to:     {out_png}')
    print('=' * 60)

    return scbc


if __name__ == '__main__':
    print('\nADMST-SCBC Cosmological Module (consolidated)')
    print('Running a quick verification and saving plots...')
    cosmology = run_corrected_analysis()
