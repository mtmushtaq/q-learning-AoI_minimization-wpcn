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

def plot_gain_vs_aaoi_from_dirs(store_dirs, gains, label="IL", color="blue"):
    """
    Plot Gain vs Final AAoI using provided folders and gains.
    - store_dirs: list of folder paths (same order as slots/gains)
    - gains: list of gain values
    """
    final_aaoi = []

    for folder in store_dirs:
        try:
            aoi_test = load_test_matrix_npy("AOI_test_iter", folder)  # shape: (tests, users)
            last_test_mean = np.mean(aoi_test[-1, :])            # mean over users in final test
            final_aaoi.append(last_test_mean)
        except Exception as e:
            print(f"⚠️ Failed to load AOI from {folder}: {e}")
            final_aaoi.append(np.nan)

    # Sort by gain (just in case)
    sorted_data = sorted(zip(gains, final_aaoi))
    sorted_gains, sorted_aaoi = zip(*sorted_data)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(sorted_gains, sorted_aaoi, marker='o', color=color, label=label)
    plt.xlabel("Gain (Users / Slots)")
    plt.ylabel("Final Average AoI")
    plt.title(f"{label} — Gain vs Final Average AoI")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{label}_gain_vs_aaoi.pdf", bbox_inches='tight')
    plt.show()

# Call the function
plot_gain_vs_aaoi_from_dirs(store_dirs, gains, label="IL", color="blue")
