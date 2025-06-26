import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0
from scipy.stats import ncx2
import os

# PDF function for SISO and MISO with MRT
def gamma_pdf_mrt(gamma, kappa, d, Nt=1, model_type='siso', c=1.0, alpha=2.0):
    """
    Computes the PDF of gamma under Rician fading with optional MISO MRT extension.

    Parameters:
    - gamma: array of gamma values
    - kappa: Rician K-factor
    - d: distance
    - Nt: number of transmit antennas (MISO if Nt > 1)
    - model_type: 'siso' or 'miso'
    - c, alpha: path loss parameters
    """
    if model_type == 'siso':
        dof = 2
        nc = 2 * kappa
    elif model_type == 'miso':
        dof = 2 * Nt
        nc = 2 * Nt * kappa
    else:
        raise ValueError("model_type must be 'siso' or 'miso'")

    # Scaling factor depending on path loss model
    beta = c / d ** alpha
    scale = beta  # Physical model: gain decreases with distance

    return ncx2.pdf(gamma / scale, df=dof, nc=nc) / scale

# CDF function using integration of the same ncx2 distribution
def gamma_cdf_mrt(gamma, kappa, d, Nt=1, model_type='siso', c=1.0, alpha=2.0):
    if model_type == 'siso':
        dof = 2
        nc = 2 * kappa
    elif model_type == 'miso':
        dof = 2 * Nt
        nc = 2 * Nt * kappa
    else:
        raise ValueError("model_type must be 'siso' or 'miso'")

    beta = c / d ** alpha
    scale = beta

    return ncx2.cdf(gamma / scale, df=dof, nc=nc)

# Plotting function
def plot_gamma_pdf_cdf(kappa_vals, d, Nt, x_max, save_dir, model_type='siso'):
    gamma_vals = np.linspace(0, x_max, 2000)
    os.makedirs(save_dir, exist_ok=True)

    # PDF plot
    plt.figure(dpi=600)
    for kappa in kappa_vals:
        pdf_vals = gamma_pdf_mrt(gamma_vals, kappa, d, Nt=Nt, model_type=model_type)
        label = fr"$\kappa={kappa}$"
        plt.plot(gamma_vals, pdf_vals, label=label, linewidth=2)
    plt.xlabel(r'$\gamma$ (Channel Gain)', fontsize=14, fontweight='bold')
    plt.ylabel('PDF', fontsize=14, fontweight='bold')
    plt.title(f'PDF of $\gamma$ with d={d}, Nt={Nt} ({model_type.upper()})', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'gamma_pdf_d{d}_Nt{Nt}_{model_type}.pdf'))
    plt.show()

    # CDF plot
    plt.figure(dpi=600)
    for kappa in kappa_vals:
        cdf_vals = gamma_cdf_mrt(gamma_vals, kappa, d, Nt=Nt, model_type=model_type)
        label = fr"$\kappa={kappa}$"
        plt.plot(gamma_vals, cdf_vals, label=label, linewidth=2)
    plt.xlabel(r'$\gamma$ (Channel Gain)', fontsize=14, fontweight='bold')
    plt.ylabel('CDF', fontsize=14, fontweight='bold')
    plt.title(f'CDF of $\gamma$ with d={d}, Nt={Nt} ({model_type.upper()})', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'gamma_cdf_d{d}_Nt{Nt}_{model_type}.pdf'))
    plt.show()

# Run the example for comparison between SISO and MISO
kappa_vals = [3, 6, 9, 12]
d = 2.0
Nt_siso = 1
Nt_miso = 4
x_max = 10.0
save_dir = "plot_MRT/rician_miso_siso_comparison"

# Generate plots
plot_gamma_pdf_cdf(kappa_vals, d, Nt_siso, x_max, save_dir, model_type='siso')
plot_gamma_pdf_cdf(kappa_vals, d, Nt_miso, x_max, save_dir, model_type='miso')
