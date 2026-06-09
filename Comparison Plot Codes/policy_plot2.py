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

store_dirs_IL = ["IL_S_250_U_100_UP_020"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_250_U_100"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

path_IL = "IL_S_250_U_100"
path_JAL = "JAL_S_250_U_100_2"

AC_user_IL = load_test_matrix_npy("AC_user_tests", path_IL)
Bt_user_IL = load_test_vector_npy("BT_user_tests", path_IL)
CH_user_IL = load_test_matrix_npy("CH_user_tests", path_IL)


AC_user_JAL = load_test_matrix_npy("AC_user_tests", path_JAL)[:100,:,:]
Bt_user_JAL = load_test_vector_npy("BT_user_tests", path_JAL)[:100,:,:]
CH_user_JAL = load_test_matrix_npy("CH_user_tests", path_JAL)[:100,:,:]


def plot_discrete_joint_decision_comparison_mode(
    BT_user_IL, CH_user_IL, AC_user_IL,
    BT_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="plots",
    output_filename="discrete_joint_decision_comparison_mode.pdf"
):
    battery_IL = BT_user_IL.flatten().astype(int)
    channel_IL = CH_user_IL.flatten().astype(int)
    actions_IL = AC_user_IL.flatten().astype(int)

    battery_JAL = BT_user_JAL.flatten().astype(int)
    channel_JAL = CH_user_JAL.flatten().astype(int)
    actions_JAL = AC_user_JAL.flatten().astype(int)

    battery_levels = 6
    channel_levels = 8

    mode_grid_IL = np.full((battery_levels, channel_levels), np.nan)
    mode_grid_JAL = np.full((battery_levels, channel_levels), np.nan)

    action_dict_IL = defaultdict(list)
    action_dict_JAL = defaultdict(list)

    for b, c, a in zip(battery_IL, channel_IL, actions_IL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            action_dict_IL[(b, c)].append(a)

    for b, c, a in zip(battery_JAL, channel_JAL, actions_JAL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            action_dict_JAL[(b, c)].append(a)

    for (b, c), actions in action_dict_IL.items():
        mode_grid_IL[b, c] = Counter(actions).most_common(1)[0][0]

    for (b, c), actions in action_dict_JAL.items():
        mode_grid_JAL[b, c] = Counter(actions).most_common(1)[0][0]

    X, Y = np.meshgrid(np.arange(battery_levels), np.arange(channel_levels), indexing='ij')

    fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    im1 = axs[0].pcolormesh(X, Y, mode_grid_IL, shading='auto', cmap='viridis')
    axs[0].set_title("IL: Battery vs Channel vs Action (Mode)", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Battery Level")
    axs[0].set_ylabel("Channel State")
    plt.colorbar(im1, ax=axs[0], label="Most Common Action", shrink=0.85)

    im2 = axs[1].pcolormesh(X, Y, mode_grid_JAL, shading='auto', cmap='viridis')
    axs[1].set_title("JAL: Battery vs Channel vs Action (Mode)", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Battery Level")
    axs[1].set_ylabel("Channel State")
    plt.colorbar(im2, ax=axs[1], label="Most Common Action", shrink=0.85)

    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()
    print(f"✅ Mode heatmap plot saved: {full_path}")

def plot_discrete_joint_decision_comparison_scatter_mode(
    BT_user_IL, CH_user_IL, AC_user_IL,
    BT_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="plots",
    output_filename="discrete_joint_decision_scatter_comparison_mode.pdf",
    battery_levels=6, channel_levels=8
):
    battery_IL = BT_user_IL.flatten().astype(int)
    channel_IL = CH_user_IL.flatten().astype(int)
    actions_IL = AC_user_IL.flatten().astype(int)

    battery_JAL = BT_user_JAL.flatten().astype(int)
    channel_JAL = CH_user_JAL.flatten().astype(int)
    actions_JAL = AC_user_JAL.flatten().astype(int)

    action_dict_IL = defaultdict(list)
    action_dict_JAL = defaultdict(list)

    for b, c, a in zip(battery_IL, channel_IL, actions_IL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            action_dict_IL[(b, c)].append(a)

    for b, c, a in zip(battery_JAL, channel_JAL, actions_JAL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            action_dict_JAL[(b, c)].append(a)

    mode_action_IL = np.full((battery_levels, channel_levels), np.nan)
    mode_action_JAL = np.full((battery_levels, channel_levels), np.nan)

    for (b, c), actions in action_dict_IL.items():
        mode_action_IL[b, c] = Counter(actions).most_common(1)[0][0]

    for (b, c), actions in action_dict_JAL.items():
        mode_action_JAL[b, c] = Counter(actions).most_common(1)[0][0]

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    vmin, vmax = 0, battery_levels - 1

    for b in range(battery_levels):
        for c in range(channel_levels):
            color = mode_action_IL[b, c] if not np.isnan(mode_action_IL[b, c]) else 0
            axs[0].scatter(b, c, c=color, cmap='jet', vmin=vmin, vmax=vmax, s=300, edgecolor='black')

    axs[0].set_title("IL: Policy Mapping (Mode)", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Battery Level")
    axs[0].set_ylabel("Channel State")
    axs[0].set_xticks(range(battery_levels))
    axs[0].set_yticks(range(channel_levels))
    axs[0].grid(True, linestyle='--', alpha=0.5)

    for b in range(battery_levels):
        for c in range(channel_levels):
            color = mode_action_JAL[b, c] if not np.isnan(mode_action_JAL[b, c]) else 0
            axs[1].scatter(b, c, c=color, cmap='jet', vmin=vmin, vmax=vmax, s=300, edgecolor='black')

    axs[1].set_title("JAL: Policy Mapping (Mode)", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Battery Level")
    axs[1].set_ylabel("Channel State")
    axs[1].set_xticks(range(battery_levels))
    axs[1].set_yticks(range(channel_levels))
    axs[1].grid(True, linestyle='--', alpha=0.5)

    norm = plt.Normalize(vmin, vmax)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axs, fraction=0.04, pad=0.04)
    cbar.set_label("Most Common Action", fontsize=12, fontweight='bold')

    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✅ Mode scatter plot saved: {full_path}")


plot_discrete_joint_decision_comparison_mode(
    Bt_user_IL, CH_user_IL, AC_user_IL,
    Bt_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="scatter_plots",
    output_filename="HP_G04.pdf"
)


plot_discrete_joint_decision_comparison_scatter_mode(
    Bt_user_IL, CH_user_IL, AC_user_IL,
    Bt_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="scatter_plots",
    output_filename="scatter_G04.pdf",
    battery_levels=6, channel_levels=8
)

