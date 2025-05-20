import numpy as np
import matplotlib.pyplot as plt
from data_npy_io import *

# Fixed parameters
users = 40
slots = [20, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
gains = [round(users / s, 3) for s in slots]

# Corresponding folders (must match slot order)
store_dirs = [
    "S_20_U_40_UP_020", "S_30_U_40_UP_020", "S_35_U_40_UP_020",
    "S_40_U_40_UP_020", "S_45_U_40_UP_020", "S_50_U_40_UP_020",
    "S_60_U_40_UP_020", "S_70_U_40_UP_020", "S_80_U_40_UP_020",
    "S_90_U_40_UP_020", "S_100_U_40_UP_020"
]

def plot_gain_vs_aaoi_from_dirs(store_dirs, gains, label="IL", color="blue", output_file="IL_gain_vs_aaoi.pdf"):
    """
    Plot Gain vs Final AAoI using provided folders and gains.
    - store_dirs: list of folder paths (same order as slots/gains)
    - gains: list of gain values
    """
    final_aaoi = []

    for folder in store_dirs:
        try:
            aoi_test = load_test_matrix_npy("AOI_test", folder)  # shape: (tests, users)
            last_test_mean = np.mean(aoi_test[-1, :])            # mean over users in final test
            final_aaoi.append(last_test_mean)
        except Exception as e:
            print(f"⚠️ Failed to load AOI from {folder}: {e}")
            final_aaoi.append(np.nan)

    # Clean & sort data
    sorted_data = sorted(zip(gains, final_aaoi))
    sorted_gains, sorted_aaoi = zip(*sorted_data)

    # Plot
    plt.figure(figsize=(8, 5), dpi=300)  # High DPI for clarity in PDF
    plt.plot(
        sorted_gains,
        sorted_aaoi,
        marker='o',
        markersize=8,
        color=color,
        linestyle='--',
        linewidth=2,
        label=label
    )

    # Styling
    plt.xlabel(r"Normalized Channel Traffic $G = \frac{M}{N}$", fontsize=12)
    plt.ylabel(r"Final Average AoI $\bar{A}$", fontsize=12)
    plt.title(r"{label} — Gain ($G$) vs Average AoI ($ \bar{A}$)", fontsize=13, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()
# Call the function
plot_gain_vs_aaoi_from_dirs(store_dirs, gains, label="IL", color="blue")
