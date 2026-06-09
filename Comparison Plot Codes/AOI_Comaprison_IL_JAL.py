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

# (optional) if your load_… functions expect a str rather than a Path
Out_dir_05 = str(Out_dir_05)

slots_062 = 160
subfolder_062 = f"IL_S_{slots_062}_U_{users}_UP_020"
Out_dir_062 = BASE_DIR / subfolder_062
Out_dir_062 = str(Out_dir_062)
#Out_dir_05 = "JAL_S_40_U_40_UP2"
#Out_dir_IL = "S_40_U_40_BT_003"

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

AOI_user_05 = load_test_matrix_npy("AOI_test_iter", Out_dir_05)[:200,:,:]
AOI_user_062 = load_test_matrix_npy("AOI_test_iter", Out_dir_062)[:200,:,:]
AOI_user_075 = load_test_matrix_npy("AOI_test_iter", Out_dir_075)[:200,:,:]
AOI_user_01 = load_test_matrix_npy("AOI_test_iter", Out_dir_01)[:200,:,:]
AOI_user_133 = load_test_matrix_npy("AOI_test_iter", Out_dir_133)[:200,:,:]
AOI_user_20 = load_test_matrix_npy("AOI_test_iter", Out_dir_20)[:200,:,:]


def compare_aoi_per_user(
    AOI_dict: dict[float, np.ndarray],
    save_dir: str | Path,
    num_users: int,
    smoothing_window: int = 3
):
    """
    Overlay normalized per-user final AoI (last iteration) across tests
    for multiple gains G = M / N.

    Parameters
    ----------
    AOI_dict : dict
        Mapping from gain G to a (tests, iters, users) array.
    save_dir : str or Path
        Folder to save the PDF.
    num_users : int
        Number of users (M), used for normalization.
    smoothing_window : int
        Window in tests for SMA smoothing.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    final_aoi = {G: arr[:, -1, :] / num_users for G, arr in AOI_dict.items()}
    sample = next(iter(final_aoi.values()))
    num_tests, total_users = sample.shape

    cols = 5
    rows = int(np.ceil(total_users / cols))
    fig, axs = plt.subplots(rows, cols,
                            figsize=(4*cols, 3*rows),
                            constrained_layout=True)
    axs = axs.flatten()
    color_cycle = plt.cm.get_cmap('tab10', len(AOI_dict))

    for u in range(total_users):
        ax = axs[u]
        for idx, (G, data) in enumerate(final_aoi.items()):
            raw = data[:, u]
            smooth = pd.Series(raw).rolling(
                window=smoothing_window,
                min_periods=1,
                center=True
            ).mean()
            color = color_cycle(idx)
            ax.plot(raw, linestyle='--', alpha=0.5, color=color)
            ax.plot(smooth, linewidth=2, label=f"G={G}", color=color)
        ax.set_title(f"User {u}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Test Index", fontsize=11, fontweight='bold')
        ax.set_ylabel("Normalized AAoI ($\\bar{{A}}_m$)", fontsize=11, fontweight='bold')
        ax.tick_params(axis='both', labelsize=10, width=1.5)
        ax.grid(True)
        if u == 0:
            ax.legend()

    for idx in range(total_users, len(axs)):
        fig.delaxes(axs[idx])

    fig.suptitle("Per-User Normalized AAoI: Gains Compared", fontsize=16, fontweight='bold')
    out_file = save_path / "aoi_per_user_comparison.pdf"
    fig.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.show()


def compare_aoi_mean_overall(
    AOI_dict: dict[float, np.ndarray],
    save_dir: str | Path,
    num_users: int,
    smoothing_window: int = 3
):
    """
    Plot normalized mean final AoI (averaged over users) vs test-index
    for each gain G on one set of axes.

    Parameters
    ----------
    AOI_dict : dict
        Mapping from gain G to a (tests, iters, users) array.
    save_dir : str or Path
        Folder to save the PDF.
    num_users : int
        Number of users (M), used for normalization.
    smoothing_window : int
        Window in tests for SMA smoothing.
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10,6))
    color_cycle = plt.cm.get_cmap('tab10', len(AOI_dict))

    for idx, (G, arr) in enumerate(AOI_dict.items()):
        final_per_test = arr[:, -1, :].mean(axis=1) / num_users
        smooth = pd.Series(final_per_test).rolling(
            window=smoothing_window,
            min_periods=1,
            center=True
        ).mean()
        color = color_cycle(idx)
        plt.plot(final_per_test, linestyle='--', alpha=0.5, color=color)
        plt.plot(smooth, linewidth=2, label=f"G={G}", color=color)

    plt.title("Normalized Mean Final AAoI over Tests: Gains Compared", fontsize=16, fontweight='bold')
    plt.xlabel("Test Index", fontsize=12, fontweight='bold')
    plt.ylabel("Normalized AAoI ($\\bar{{A}}$)", fontsize=12, fontweight='bold')
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.grid(True)
    plt.legend(title="Load G", fontsize=10)
    plt.tight_layout()

    out_file = save_path / "aoi_mean_overall_comparison.pdf"
    plt.savefig(out_file, dpi=600)
    print("Saved:", out_file)
    plt.show()



AOI_dict = {0.5: AOI_user_05, 0.625: AOI_user_062, 0.75: AOI_user_075, 1.0: AOI_user_01, 1.33: AOI_user_133, 2.0: AOI_user_20}
save_folder = "aoi_comparison_IL_all"
compare_aoi_per_user(AOI_dict, save_folder, users, smoothing_window=3)
compare_aoi_mean_overall(AOI_dict, save_folder, users, smoothing_window=3)
