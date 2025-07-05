import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from data_npy_io import *
from pathlib import Path
import argparse

# Fixed parameters
users_IL = 100
users_JAL = 100
users_dist = 100
users_rd = 100

# Slot and gain definitions
table = {
    "IL": {
        "slots": [250,225,200,166,133,100,75,62,56,50],
        "base_dir": Path(r"E:/IL_U100"),
        "color": "blue",
        "marker": 'o',
        "users": users_IL
    },
    "JAL": {
        "slots": [250,225,200,160,133,100,75,62,56,50],
        "base_dir": Path(r"E:/JAL_U100"),
        "color": "darkorange",
        "marker": 's',
        "users": users_JAL
    },
    "Random": {
        "slots": [250,225,200,160,133,100,75,50],
        "base_dir": Path(r"E:/Random_U100"),
        "color": "green",
        "marker": 'D',
        "users": users_rd
    },
    "Dist": {
        "slots": [250,225,200,160,133,100,75,50],
        "base_dir": Path(r"E:/Dist_U100"),
        "color": "purple",
        "marker": '^',
        "users": users_dist
    }
}

# Helper to load final AAoI
def compute_final_aaoi(folders, key="AOI_test_iter"):
    aaoi_list = []
    for folder in folders:
        try:
            aoi_test = load_test_matrix_npy(key, folder)
            aaoi_list.append(np.mean(aoi_test[-1, :]))
        except Exception as e:
            print(f"⚠️ Failed to load from {folder}: {e}")
            aaoi_list.append(np.nan)
    return aaoi_list

# Plotting function
def plot_gain_vs_aaoi(methods, output_path, normalize_users=True, dpi=600):
    plt.figure(figsize=(8,5), dpi=dpi)
    for label, cfg in methods.items():
        slots = cfg['slots']
        gains = np.array([round(cfg['users']/s,3) for s in slots])
        folders = [cfg['base_dir']/f for f in [
            f"{label}_S_{s}_U_100" + ("_c" if label=="IL" else "")
            for s in slots
        ]]
        aaoi = np.array(compute_final_aaoi(folders))/cfg['users'] if normalize_users else np.array(compute_final_aaoi(folders))
        # sort
        idx = np.argsort(gains)
        g_sorted = gains[idx]
        a_sorted = aaoi[idx]
        # smooth curve
        interp = interp1d(g_sorted, a_sorted, kind='cubic', fill_value='extrapolate')
        g_fine = np.linspace(g_sorted.min(), g_sorted.max(), 200)
        a_smooth = interp(g_fine)
        plt.plot(g_fine, a_smooth, linestyle='-', linewidth=2, color=cfg['color'], label=label)
        # ticks at actual data points
        plt.plot(g_sorted, a_sorted, marker=cfg['marker'], linestyle='None', markersize=6, color=cfg['color'])

    plt.xlabel(r"Normalized Channel Traffic $G$", fontsize=12, fontweight='bold')
    plt.ylabel(r"Normalized Average AoI $\bar{A}_{norm}$", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.legend(fontsize=11)
    plt.tight_layout()
    os.makedirs(output_path.parent, exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smoothed AAoI vs Gain plot.")
    parser.add_argument('--output-dir', type=str, help='Directory to save PDF')
    args = parser.parse_args()
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        inp = input("Enter directory to save the PDF (default current dir): ").strip()
        out_dir = Path(inp) if inp else Path('.')
    output_file = out_dir / "comparison_gain_vs_aaoi_n.pdf"
    plot_gain_vs_aaoi(table, output_file)
