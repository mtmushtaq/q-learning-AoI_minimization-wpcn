import numpy as np
import matplotlib.pyplot as plt
import os
from data_npy_io import *

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

BASE_DIR_DIST = Path(r"E:\Dist_U100")
store_dirs_dist = ["Dist_S_100_U_100"]
full_paths_dist = [BASE_DIR_DIST / subdir for subdir in store_dirs_dist]
full_paths_dist = [str(path) for path in full_paths_dist]

BASE_DIR_RD = Path(r"E:\Random_U100")
store_dirs_rd = ["Random_S_100_U_100"]
full_paths_rd = [BASE_DIR_RD / subdir for subdir in store_dirs_rd]
full_paths_rd = [str(path) for path in full_paths_rd]

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100")

store_dirs_IL = ["IL_S_100_U_100_UP_020"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_100_U_100"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]


BT_user_IL = load_test_matrix_npy("BT_user_tests", full_paths_IL[0])[:100,:,:]
BT_user_JAL = load_test_matrix_npy("BT_user_tests", full_paths_JAL[0])[:100,:,:]
BT_user_Dist = load_test_matrix_npy("BT_user_tests", full_paths_dist[0])[:100,:,:]
BT_user_Random = load_test_matrix_npy("BT_user_tests", full_paths_rd[0])[:100,:,:]

#BT_user_01 = load_test_matrix_npy("BT_user_tests", Out_dir_01)[:100,:,:]
#BT_user_133 = load_test_matrix_npy("BT_user_tests", Out_dir_133)[:100,:,:]
#BT_user_20 = load_test_matrix_npy("BT_user_tests", Out_dir_20)[:100,:,:]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

def compare_battery_per_user_fixed_methods(
    BT_dict: dict[str, np.ndarray],
    save_dir: str | Path,
    output_name: str,
    gain_value: float,
    smoothing_window: int = 3
):
    """
    Overlay per-user average battery (over iterations) across tests
    for multiple methods at a fixed gain G.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    sample = next(iter(BT_dict.values()))
    num_tests, num_iters, num_users = sample.shape
    avg_batt = {method: arr.mean(axis=1) for method, arr in BT_dict.items()}

    cols = 5
    rows = int(np.ceil(num_users / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(4*cols, 3*rows), constrained_layout=True)
    axs = axs.flatten()
    color_cycle = plt.cm.get_cmap('tab10', len(BT_dict))

    for u in range(num_users):
        ax = axs[u]
        for idx, (method, mat) in enumerate(avg_batt.items()):
            raw = mat[:, u]
            smooth = pd.Series(raw).rolling(window=smoothing_window, min_periods=1, center=True).mean()
            color = color_cycle(idx)
            ax.plot(raw, linestyle='--', alpha=0.5, color=color, marker='o', markevery=10, markersize=3)
            ax.plot(smooth, linewidth=2, label=method, color=color)
        ax.set_title(f"User {u}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Test Index", fontsize=11, fontweight='bold')
        ax.set_ylabel("Avg Battery", fontsize=11, fontweight='bold')
        ax.tick_params(axis='both', labelsize=10, width=1.5)
        ax.set_xticks(np.arange(0, num_tests + 1, 10))
        ax.grid(True)
        if u == 0:
            ax.legend()

    for idx in range(num_users, len(axs)):
        fig.delaxes(axs[idx])

    fig.suptitle(f"Per‑User Battery Evolution (G={gain_value})", fontsize=16, fontweight='bold')
    out_file = save_path / f"{output_name}_battery_per_user_G{gain_value}.pdf"
    fig.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.close()


def compare_battery_mean_overall_fixed_methods(
    BT_dict: dict[str, np.ndarray],
    save_dir: str | Path,
    output_name: str,
    gain_value: float,
    smoothing_window: int = 3
):
    """
    Plot the mean-battery (over users & iters) vs test-index
    for each method on one set of axes at fixed G.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    color_cycle = plt.cm.get_cmap('tab10', len(BT_dict))
    num_tests = next(iter(BT_dict.values())).shape[0]

    for idx, (method, arr) in enumerate(BT_dict.items()):
        mean_over_users = arr.mean(axis=1).mean(axis=1) if arr.ndim == 3 else arr.mean(axis=1)
        smooth = pd.Series(mean_over_users).rolling(window=smoothing_window, min_periods=1, center=True).mean()
        color = color_cycle(idx)
        plt.plot(mean_over_users, linestyle='--', alpha=0.5, color=color, marker='o', markevery=10, markersize=4)
        plt.plot(smooth, linewidth=2, label=method, color=color)

    plt.title(f"Mean Battery over Tests (G={gain_value})", fontsize=16, fontweight='bold')
    plt.xlabel("Test Index", fontsize=12, fontweight='bold')
    plt.ylabel("Mean Battery (over users & iters)", fontsize=12, fontweight='bold')
    plt.xticks(np.arange(0, num_tests + 1, 10), fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.grid(True)
    plt.legend(title="Method", fontsize=10)
    plt.tight_layout()

    out_file = save_path / f"{output_name}_battery_mean_overall_G{gain_value}.pdf"
    plt.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.close()


BT_dict = {"IL": BT_user_IL, "JAL": BT_user_JAL, "Dist": BT_user_Dist, "Random": BT_user_Random}

compare_battery_per_user_fixed_methods(BT_dict, "BatteryPlots", "BT_Users10", gain_value=1)
compare_battery_mean_overall_fixed_methods(BT_dict, "BatteryPlots", "BT_Mean10", gain_value=1)
