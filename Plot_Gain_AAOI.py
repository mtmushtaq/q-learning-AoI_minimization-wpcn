import os
import numpy as np
import matplotlib.pyplot as plt
import re

users = 40
slots = [20, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
Gain = []
Gain = users/slots

def extract_gain_from_foldername(foldername):
    """Extract slots and users from folder like 'S_20_U_40_UP_020'"""
    match = re.search(r'S_(\d+)_U_(\d+)', foldername)
    if match:
        slots, users = map(int, match.groups())
        gain = round(users / slots, 3)
        return gain
    return None

def load_test_matrix_npy(name, input_dir):
    """Load npy matrix from given folder"""
    return np.load(os.path.join(input_dir, f"{name}.npy"))

def plot_gain_vs_aaoi_from_dirs(store_dirs, label="IL", color="blue"):
    """
    Plot Gain vs Final AAoI for a list of folders.

    Parameters:
    - base_path: root path where all folders are stored
    - store_dirs: list of folder names to process
    - label: legend label for plot
    - color: line color
    """
    gains = []
    final_aaoi = []

    for folder in store_dirs:
        #full_path = os.path.join(base_path, folder)
        gain = extract_gain_from_foldername(folder)
        if gain is None:
            print(f"❌ Skipped: Cannot extract gain from {folder}")
            continue

        try:
            aoi_test = load_test_matrix_npy("AOI_test", store_dirs[folder])  # shape: (tests, users)
            last_test_mean = np.mean(aoi_test[-1, :])               # final AAoI
            gains.append(gain)
            final_aaoi.append(last_test_mean)
        except Exception as e:
            print(f"⚠️ Failed to load from {folder}: {e}")

    # Sort for clean plotting
    sorted_data = sorted(zip(gains, final_aaoi))
    gains_sorted, aaoi_sorted = zip(*sorted_data)

    # Plot
    plt.plot(gains_sorted, aaoi_sorted, marker='o', color=color, label=label)
    plt.xlabel("Gain (Users / Slots)")
    plt.ylabel("Final Average AoI")
    plt.title(f"{label} — Gain vs Final Average AoI")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{label}_gain_vs_aaoi.pdf", bbox_inches='tight')
    plt.show()

store_dirs = [
    "S_20_U_40_UP_020", "S_30_U_40_UP_020", "S_35_U_40_UP_020",
    "S_40_U_40_UP_020", "S_45_U_40_UP_020", "S_50_U_40_UP_020",
    "S_60_U_40_UP_020", "S_70_U_40_UP_020", "S_80_U_40_UP_020",
    "S_90_U_40_UP_020", "S_100_U_40_UP_020"
]

#base_path = r"C:\Users\Tauseef\Documents\GitHub\AOI_JAL_IL"

plot_gain_vs_aaoi_from_dirs(store_dirs, label="IL", color="blue")