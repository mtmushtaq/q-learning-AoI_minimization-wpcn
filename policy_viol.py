# Re-import required libraries after code execution environment reset
import numpy as np
import matplotlib.pyplot as plt
import os

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_npy_io import *
from collections import defaultdict, Counter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import Axes3D

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100")

store_dirs_IL = ["IL_S_250_U_100_c"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_250_U_100"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

path_IL = "IL_S_200_U_100"
path_JAL = "JAL_S_250_U_100_2"

AC_user_IL = load_test_matrix_npy("AC_user_tests", full_paths_IL[0])
Bt_user_IL = load_test_vector_npy("BT_user_tests", full_paths_IL[0])
CH_user_IL = load_test_matrix_npy("CH_user_tests", full_paths_IL[0])


AC_user_JAL = load_test_matrix_npy("AC_user_tests", full_paths_JAL[0])[:200,:,:]
Bt_user_JAL = load_test_vector_npy("BT_user_tests", full_paths_JAL[0])[:200,:,:]
CH_user_JAL = load_test_matrix_npy("CH_user_tests", full_paths_JAL[0])[:200,:,:]


def plot_policy_violation_map(
    BT_user_IL, CH_user_IL, AC_user_IL,
    BT_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="plots",
    output_filename="policy_violation_map.pdf",
    battery_levels=6,
    channel_levels=8
):
    """
    Plots a violation heatmap showing where actions exceeded available battery for IL and JAL.
    """

    # Flatten input data
    battery_IL = BT_user_IL.flatten().astype(int)
    channel_IL = CH_user_IL.flatten().astype(int)
    actions_IL = AC_user_IL.flatten().astype(int)

    battery_JAL = BT_user_JAL.flatten().astype(int)
    channel_JAL = CH_user_JAL.flatten().astype(int)
    actions_JAL = AC_user_JAL.flatten().astype(int)

    # Initialize violation grids
    violation_IL = np.zeros((battery_levels, channel_levels), dtype=int)
    violation_JAL = np.zeros((battery_levels, channel_levels), dtype=int)

    # Populate violation grids: 1 if any a > b seen for that (b, c)
    for b, c, a in zip(battery_IL, channel_IL, actions_IL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            if a > b:
                violation_IL[b, c] = 1

    for b, c, a in zip(battery_JAL, channel_JAL, actions_JAL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            if a > b:
                violation_JAL[b, c] = 1

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

    cmap = plt.cm.Reds
    bounds = [0, 0.5, 1]
    norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    im1 = axs[0].imshow(violation_IL, cmap=cmap, norm=norm)
    axs[0].set_title("IL: Policy Violations (a > battery)", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Channel State")
    axs[0].set_ylabel("Battery Level")
    axs[0].set_xticks(np.arange(channel_levels))
    axs[0].set_yticks(np.arange(battery_levels))

    im2 = axs[1].imshow(violation_JAL, cmap=cmap, norm=norm)
    axs[1].set_title("JAL: Policy Violations (a > battery)", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Channel State")
    axs[1].set_ylabel("Battery Level")
    axs[1].set_xticks(np.arange(channel_levels))
    axs[1].set_yticks(np.arange(battery_levels))

    # Shared colorbar
    cbar = fig.colorbar(im2, ax=axs, orientation='vertical', shrink=0.8, ticks=[0, 1])
    cbar.ax.set_yticklabels(['Valid', 'Violated'])
    cbar.set_label("Violation Flag", fontsize=12, fontweight='bold')

    # Save
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()
    print(f"✅ Violation map saved: {full_path}")


plot_policy_violation_map(
    Bt_user_IL, CH_user_IL, AC_user_IL,
    Bt_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="policy_v",
    output_filename="policy_violation_map.pdf",
    battery_levels=6,
    channel_levels=8
)