import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0
#from numpy import cumtrapz  # This is available in NumPy from version 1.20+
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.special import i0

# === Manual trapezoidal cumulative integration ===
def safe_cumtrapz(y, x):
    dx = np.diff(x)
    avg_y = (y[:-1] + y[1:]) / 2
    return np.concatenate([[0], np.cumsum(dx * avg_y)])


# PDF function (same as earlier)
def gamma_pdf(gamma, kappa, d, model_type='scaled', c=1.0, alpha=2.0):
    if model_type == 'scaled':
        beta_inv = (1 / c) * d ** alpha
        mu = gamma / beta_inv
        factor = (1 + kappa) / beta_inv
    elif model_type == 'attenuation':
        beta = c / d ** alpha
        mu = gamma / beta
        factor = (1 + kappa) / beta
    else:
        raise ValueError("model_type must be either 'scaled' or 'attenuation'")

    exponent = np.exp(-kappa - (1 + kappa) * mu)
    bessel = i0(2 * np.sqrt(kappa * (1 + kappa) * mu))
    return factor * exponent * bessel

# CDF plotting function
def plot_gamma_cdf(kappa_vals, distance, save_dir, x_max=3.0, model_type='scaled'):
    gamma_vals = np.linspace(0, x_max, 2000)
    colors = ['blue', 'green', 'orange', 'red', 'black', 'purple']
    c = 1.0
    alpha = 2.0

    os.makedirs(save_dir, exist_ok=True)
    plt.figure(dpi=600)

    for kappa, color in zip(kappa_vals, colors):
        pdf_vals = gamma_pdf(gamma_vals, kappa, distance, model_type=model_type, c=c, alpha=alpha)
        cdf_vals = safe_cumtrapz(pdf_vals, gamma_vals)  # CDF by cumulative integration
        plt.plot(gamma_vals, cdf_vals, label=fr'$\kappa$ = {kappa}', linewidth=2.5, color=color)

    model_label = 'atten' if model_type == 'attenuation' else 'scaled'
    plt.xlabel(r'$\gamma$ (Channel Gain)', fontsize=14, fontweight='bold')
    plt.ylabel(r'$F(\gamma)$', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.xlim([0, x_max])
    plt.ylim([0, 1])
    plt.legend(fontsize=10)
    plt.title(fr'CDF of $\gamma$ with $d={distance}$ ({model_label})', fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Save
    pdf_path = os.path.join(save_dir, f'gamma_cdf_d{distance}_{model_label}_xmax{x_max}.pdf')
    png_path = os.path.join(save_dir, f'gamma_cdf_d{distance}_{model_label}_xmax{x_max}.png')
    plt.savefig(pdf_path, format='pdf')
    plt.savefig(png_path, format='png')
    plt.show()

    print(f"✅ CDF plot saved to:\n📄 {pdf_path}\n🖼️ {png_path}")

# === Interactive use ===
if __name__ == "__main__":
    kappa_input = input("Enter comma-separated κ values (e.g. 0,3,6,9): ")
    kappa_vals = [int(k) for k in kappa_input.split(",")]

    d = float(input("Enter distance d (e.g. 2.0): "))
    x_max = float(input("Enter x-axis max value (e.g. 3 or 10): "))
    save_dir = input("Enter save path (e.g. ./plots): ")
    model_choice = input("Which model? (scaled/attenuation): ").strip().lower()

    plot_gamma_cdf(kappa_vals, d, save_dir, x_max=x_max, model_type=model_choice)
