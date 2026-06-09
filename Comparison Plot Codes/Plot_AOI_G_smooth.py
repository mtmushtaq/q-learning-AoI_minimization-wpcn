import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from data_npy_io import *
from pathlib import Path
import argparse

# Fixed parameters
users = 100
users_IL = 100
users_JAL = 100
users_dist = 100
users_rd = 100

# Slot and gain definitions
slots_IL = [250, 225, 200, 166, 133, 100, 75, 62, 56, 50]
gains_IL = [round(users_IL / s, 3) for s in slots_IL]
store_dirs_IL = [
    "IL_S_250_U_100_c", "IL_S_225_U_100_c", "IL_S_200_U_100_c",
    "IL_S_166_U_100_c", "IL_S_133_U_100_c", "IL_S_100_U_100_c",
    "IL_S_75_U_100_c", "IL_S_62_U_100_c", "IL_S_56_U_100_c", "IL_S_50_U_100_c"
]

slots_JAL = [250, 225, 200, 160, 133, 100, 75, 62, 56, 50]
gains_JAL = [round(users_JAL / s, 3) for s in slots_JAL]
store_dirs_JAL = [
    "JAL_S_250_U_100", "JAL_S_225_U_100", "JAL_S_200_U_100",
    "JAL_S_160_U_100", "JAL_S_133_U_100", "JAL_S_100_U_100",
    "JAL_S_75_U_100", "JAL_S_62_U_100", "JAL_S_56_U_100", "JAL_S_50_U_100"
]

slots_dist = [250, 225, 200, 160, 133, 100, 75, 50]
gains_dist = [round(users_dist / s, 3) for s in slots_dist]
store_dirs_dist = [
    "Dist_S_250_U_100", "Dist_S_225_U_100", "Dist_S_200_U_100",
    "Dist_S_160_U_100", "Dist_S_133_U_100", "Dist_S_100_U_100",
    "Dist_S_75_U_100", "Dist_S_50_U_100"
]

slots_rd = [250, 225, 200, 160, 133, 100, 75, 50]
gains_rd = [round(users_rd / s, 3) for s in slots_rd]
store_dirs_rd = [
    "Random_S_250_U_100", "Random_S_225_U_100", "Random_S_200_U_100",
    "Random_S_160_U_100", "Random_S_133_U_100", "Random_S_100_U_100",
    "Random_S_75_U_100", "Random_S_50_U_100"
]

# Base directories (adjust as needed)
BASE_DIR_IL = Path(r"E:/IL_U100")
BASE_DIR_JAL = Path(r"E:/JAL_U100")
BASE_DIR_RD = Path(r"E:/Random_U100")
BASE_DIR_DIST = Path(r"E:/Dist_U100")


# Helper to load final AAoI
def compute_final_aaoi(store_dirs, key="AOI_test_iter"):
    aaoi_list = []
    for folder in store_dirs:
        try:
            aoi_test = load_test_matrix_npy(key, folder)
            aaoi_list.append(np.mean(aoi_test[-1, :]))
        except Exception as e:
            print(f"⚠️ Failed to load AOI from {folder}: {e}")
            aaoi_list.append(np.nan)
    return aaoi_list


# Plot with smoothing
def plot_with_smoothing(gains, aaoi, label, color, marker, linestyle, smooth=True):
    data = sorted(zip(gains, aaoi))
    g, a = zip(*data)
    g = np.array(g);
    a = np.array(a)
    plt.scatter(g, a, marker=marker, color=color, edgecolor='k', s=60, label=f"{label} (raw)")
    if smooth:
        interp = interp1d(g, a, kind='cubic', fill_value='extrapolate')
        g_fine = np.linspace(g.min(), g.max(), 200)
        a_smooth = interp(g_fine)
        plt.plot(g_fine, a_smooth, linestyle=linestyle, linewidth=2, color=color, alpha=0.8, label=f"{label} (smooth)")
    else:
        plt.plot(g, a, linestyle=linestyle, linewidth=2, color=color, label=label)


# Multi-method comparison
def plot_gain_vs_aaoi_multi_comparison(methods_data, output_path, normalize_users=True, dpi=600):
    plt.figure(figsize=(8, 5), dpi=dpi)
    for store_dirs, gains, label, color, marker, users in methods_data:
        full_paths = [str(d) for d in store_dirs]
        aaoi = compute_final_aaoi(full_paths)
        if normalize_users:
            aaoi = np.array(aaoi) / users
        plot_with_smoothing(gains, aaoi, label, color, marker, linestyle='--', smooth=True)
    plt.xlabel(r"Normalized Channel Traffic $G$", fontsize=12, fontweight='bold')
    plt.ylabel(r"Normalized Average AoI $\bar{A}_{norm}$", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.legend(fontsize=11)
    plt.tight_layout()
    # ensure output directory exists
    os.makedirs(output_path.parent, exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot AAoI vs Gain with smoothing and choose output directory.")
    parser.add_argument('--output-dir', type=str, required=False,
                        help='Directory to save the output PDF file.')
    args = parser.parse_args()

    # Determine output directory
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        inp = input("Enter directory to save the PDF (default: current dir): ").strip()
        out_dir = Path(inp) if inp else Path('.')

    # Build methods data with full paths
    methods_data = [
        ([BASE_DIR_IL / d for d in store_dirs_IL], gains_IL, "IL", "blue", 'o', users_IL),
        ([BASE_DIR_JAL / d for d in store_dirs_JAL], gains_JAL, "JAL", "darkorange", 's', users_JAL),
        ([BASE_DIR_RD / d for d in store_dirs_rd], gains_rd, "Random", "green", 'D', users_rd),
        ([BASE_DIR_DIST / d for d in store_dirs_dist], gains_dist, "OT1", "purple", '^', users_dist)
    ]
    output_file = out_dir / "comparison_gain_vs_aaoi_ALL.pdf"
    plot_gain_vs_aaoi_multi_comparison(methods_data, output_file)
