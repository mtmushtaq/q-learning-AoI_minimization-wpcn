import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0

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

def plot_gamma_pdf(kappa_vals, distance, save_dir, x_max=3.0,
                   use_log_scale=False, model_type='scaled'):
    gamma_vals = np.linspace(0, x_max, 1000)
    colors = ['green', 'blue', 'black', 'purple', 'orange', 'brown', 'cyan', 'magenta']
    shading_colors = ['#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff8080',
                      '#ff6666', '#ff4d4d', '#ff3333', '#ff1a1a']
    c = 1.0
    alpha = 2.0

    os.makedirs(save_dir, exist_ok=True)
    plt.figure(dpi=600)

    for kappa, color in zip(kappa_vals, colors):
        pdf_vals = gamma_pdf(gamma_vals, kappa, distance, model_type=model_type,
                             c=c, alpha=alpha)
        if use_log_scale:
            pdf_vals = np.maximum(pdf_vals, 1e-12)
        plt.plot(gamma_vals, pdf_vals, label=fr'$\kappa$ = {kappa}', linewidth=2.5, color=color)

    # Grading thresholds
    thresholds = np.arange(0, x_max + 0.5, 0.5)
    for i in range(len(thresholds) - 1):
        plt.axvspan(thresholds[i], thresholds[i+1],
                    color=shading_colors[i % len(shading_colors)], alpha=0.3)
    for thresh in thresholds[1:-1]:
        plt.axvline(x=thresh, color='red', linestyle='dotted', linewidth=2, label='_nolegend_')
    plt.axvline(x=-1, color='red', linestyle='dotted', linewidth=2, label='Grading Thresholds')

    if use_log_scale:
        plt.yscale('log')
        y_label = 'PDF (log scale)'
        filename_suffix = '_logscale'
    else:
        y_label = 'PDF'
        filename_suffix = ''

    model_label = 'atten' if model_type == 'attenuation' else 'scaled'
    plt.xlabel(r'$\gamma$ (Channel Gain)', fontsize=14, fontweight='bold')
    plt.ylabel(y_label, fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.xlim([0, x_max])
    plt.legend(fontsize=10)
    plt.title(fr'PDF of $\gamma$ with $d={distance}$ ({model_label})', fontsize=16, fontweight='bold')
    plt.grid(True, which='both' if use_log_scale else 'major', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    pdf_path = os.path.join(save_dir, f'gamma_pdf_d{distance}_{model_label}_xmax{x_max}{filename_suffix}.pdf')
    png_path = os.path.join(save_dir, f'gamma_pdf_d{distance}_{model_label}_xmax{x_max}{filename_suffix}.png')
    plt.savefig(pdf_path, format='pdf')
    plt.savefig(png_path, format='png')
    plt.show()

    print(f"✅ Saved to:\n📄 {pdf_path}\n🖼️ {png_path}")

# === Interactive Use ===
if __name__ == "__main__":
    kappa_input = input("Enter comma-separated κ values (e.g. 0,3,6,9): ")
    kappa_vals = [int(k) for k in kappa_input.split(",")]

    d = float(input("Enter distance d (e.g. 2.0): "))
    x_max = float(input("Enter x-axis max value (e.g. 3 or 5 or 10): "))
    save_dir = input("Enter save path (e.g. ./plots): ")
    log_choice = input("Use log scale for Y-axis? (yes/no): ").strip().lower()
    model_choice = input("Which model? (scaled/attenuation): ").strip().lower()

    plot_gamma_pdf(kappa_vals, d, save_dir, x_max=x_max,
                   use_log_scale=(log_choice == "yes"),
                   model_type=model_choice)
