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

# ————————————————
# 1) absolute base dir:
# ————————————————
BASE_DIR = Path(
    r"C:\Users\Tauseef\OneDrive - Politecnico di Bari"
    r"\AOI Q learning Paper\Data 10 June"
)
if not BASE_DIR.exists():
    raise FileNotFoundError(f"{BASE_DIR!r} does not exist")
# ——————————————————————————————————
# 2) construct the per‐experiment subfolder
# ——————————————————————————————————
slots_05 = 200
users = 100

subfolder_05 = f"IL_S_{slots_05}_U_{users}_UP_020"
Out_dir_05 = BASE_DIR / subfolder_05

slots_062 = 160
subfolder_062 = f"IL_S_{slots_062}_U_{users}_UP_020"
Out_dir_062 = BASE_DIR / subfolder_062
Out_dir_062 = str(Out_dir_062)

# (optional) if your load_… functions expect a str rather than a Path
Out_dir_05 = str(Out_dir_05)
slots_075 = 133
subfolder_075 = f"IL_S_{slots_075}_U_{users}_UP_020"
Out_dir_075 = BASE_DIR / subfolder_075
Out_dir_075 = str(Out_dir_075)

slots_01 = 100
subfolder_01 = f"IL_S_{slots_01}_U_{users}_UP_020"
Out_dir_01 = BASE_DIR / subfolder_01
Out_dir_01 = str(Out_dir_01)

slots_133 = 75
subfolder_133 = f"IL_S_{slots_133}_U_{users}_UP_020"
Out_dir_133 = BASE_DIR / subfolder_133
Out_dir_133 = str(Out_dir_133)

slots_20 = 50
subfolder_20 = f"IL_S_{slots_20}_U_{users}_UP_020"
Out_dir_20 = BASE_DIR / subfolder_20
Out_dir_20 = str(Out_dir_20)


# Load AoI matrices for each gain

BT_user_05 = load_test_matrix_npy("BT_user_tests", Out_dir_05)[:200,:,:]
BT_user_062 = load_test_matrix_npy("BT_user_tests", Out_dir_062)[:200,:,:]
BT_user_075 = load_test_matrix_npy("BT_user_tests", Out_dir_075)[:200,:,:]
BT_user_01 = load_test_matrix_npy("BT_user_tests", Out_dir_01)[:200,:,:]
BT_user_133 = load_test_matrix_npy("BT_user_tests", Out_dir_133)[:200,:,:]
BT_user_20 = load_test_matrix_npy("BT_user_tests", Out_dir_20)[:200,:,:]

def compare_battery_per_user(
    BT_dict: dict[float, np.ndarray],
    save_dir: str | Path,
    smoothing_window: int = 3
):
    """
    Overlay per-user average battery (over iterations) across tests
    for multiple gains G.

    Parameters
    ----------
    BT_dict : dict
        Mapping from gain G to a (tests, iters, users) array.
    save_dir : str or Path
        Folder to save the PDF.
    smoothing_window : int
        Window in tests for SMA smoothing.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    sample = next(iter(BT_dict.values()))
    num_tests, num_iters, num_users = sample.shape
    avg_batt = {G: arr.mean(axis=1) for G, arr in BT_dict.items()}

    cols = 5
    rows = int(np.ceil(num_users / cols))
    fig, axs = plt.subplots(rows, cols,
                            figsize=(4*cols, 3*rows),
                            constrained_layout=True)
    axs = axs.flatten()
    color_cycle = plt.cm.get_cmap('tab10', len(BT_dict))

    for u in range(num_users):
        ax = axs[u]
        for idx, (G, mat) in enumerate(avg_batt.items()):
            raw = mat[:, u]
            smooth = pd.Series(raw).rolling(window=smoothing_window,
                                            min_periods=1,
                                            center=True).mean()
            color = color_cycle(idx)
            ax.plot(raw, linestyle='--', alpha=0.5, color=color)
            ax.plot(smooth, linewidth=2, label=f"G={G}", color=color)
        ax.set_title(f"User {u}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Test Index", fontsize=11, fontweight='bold')
        ax.set_ylabel("Avg Battery", fontsize=11, fontweight='bold')
        ax.tick_params(axis='both', labelsize=10, width=1.5)
        ax.grid(True)
        if u == 0:
            ax.legend()

    for idx in range(num_users, len(axs)):
        fig.delaxes(axs[idx])

    fig.suptitle("Per‑User Battery Evolution: Gains Compared", fontsize=16, fontweight='bold')
    out_file = save_path / "battery_per_user_comparison.pdf"
    fig.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.show()


def compare_battery_mean_overall(
    BT_dict: dict[float, np.ndarray],
    save_dir: str | Path,
    smoothing_window: int = 3
):
    """
    Plot the mean-battery (over users & iters) vs test-index
    for each gain G on one set of axes.

    Parameters
    ----------
    BT_dict : dict
        Mapping from gain G to a (tests, iters, users) array.
    save_dir : str or Path
        Folder to save the PDF.
    smoothing_window : int
        Window in tests for SMA smoothing.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10,6))
    color_cycle = plt.cm.get_cmap('tab10', len(BT_dict))

    for idx, (G, arr) in enumerate(BT_dict.items()):
        mean_over_users = arr.mean(axis=1).mean(axis=1) if arr.ndim == 3 else arr.mean(axis=1)
        smooth = pd.Series(mean_over_users).rolling(
            window=smoothing_window,
            min_periods=1,
            center=True
        ).mean()
        color = color_cycle(idx)
        plt.plot(mean_over_users, linestyle='--', alpha=0.5, color=color)
        plt.plot(smooth, linewidth=2, label=f"G={G}", color=color)

    plt.title("Mean Battery over Tests: Gains Compared", fontsize=16, fontweight='bold')
    plt.xlabel("Test Index", fontsize=12, fontweight='bold')
    plt.ylabel("Mean Battery (over users & iters)", fontsize=12, fontweight='bold')
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.grid(True)
    plt.legend(title="Load G", fontsize=10)
    plt.tight_layout()

    out_file = save_path / "battery_mean_overall_comparison.pdf"
    plt.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.show()




BT_dict = {0.5:   BT_user_05, 0.625: BT_user_062, 0.75: BT_user_075, 1.0: BT_user_01, 1.33: BT_user_133, 2.0: BT_user_20}

out_folder = "BT_Comparison_new"

compare_battery_per_user(BT_dict, out_folder, smoothing_window=5)
compare_battery_mean_overall(BT_dict, out_folder, smoothing_window=5)
