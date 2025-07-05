import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_npy_io import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import Axes3D

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100")

store_dirs_IL = ["IL_S_50_U_100_c"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_50_U_100_c"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

path_IL = "IL_S_200_U_100_c"
path_JAL = "JAL_S_250_U_100"

AC_user_IL = load_test_matrix_npy("AC_user_tests", full_paths_IL[0])
Bt_user_IL = load_test_vector_npy("BT_user_tests", full_paths_IL[0])
CH_user_IL = load_test_matrix_npy("CH_user_tests", full_paths_IL[0])


AC_user_JAL = load_test_matrix_npy("AC_user_tests", full_paths_JAL[0])[:200,:,:]
Bt_user_JAL = load_test_vector_npy("BT_user_tests", full_paths_JAL[0])[:200,:,:]
CH_user_JAL = load_test_matrix_npy("CH_user_tests", full_paths_JAL[0])[:200,:,:]


def plot_discrete_joint_decision_comparison(
BT_user_IL, CH_user_IL, AC_user_IL,
BT_user_JAL, CH_user_JAL, AC_user_JAL,
output_dir="plots",
output_filename="discrete_joint_decision_comparison.pdf"):
    """
    Compare IL vs JAL discrete joint Battery vs Channel vs Action maps.

    Inputs are full 3D arrays: [tests, frames, users]
    """

    # Flatten both datasets
    battery_IL = BT_user_IL.flatten().astype(int)
    channel_IL = CH_user_IL.flatten().astype(int)
    actions_IL = AC_user_IL.flatten()

    battery_JAL = BT_user_JAL.flatten().astype(int)
    channel_JAL = CH_user_JAL.flatten().astype(int)
    actions_JAL = AC_user_JAL.flatten()

    # Discrete levels
    battery_levels = 6   # 0 to 5
    channel_levels = 8   # 0 to 7

    # Create grids
    action_grid_IL = np.full((battery_levels, channel_levels), np.nan)
    count_grid_IL = np.zeros((battery_levels, channel_levels))

    action_grid_JAL = np.full((battery_levels, channel_levels), np.nan)
    count_grid_JAL = np.zeros((battery_levels, channel_levels))

    # Fill IL grid
    for b, c, a in zip(battery_IL, channel_IL, actions_IL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            if np.isnan(action_grid_IL[b, c]):
                action_grid_IL[b, c] = 0
            action_grid_IL[b, c] += a
            count_grid_IL[b, c] += 1

    # Fill JAL grid
    for b, c, a in zip(battery_JAL, channel_JAL, actions_JAL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            if np.isnan(action_grid_JAL[b, c]):
                action_grid_JAL[b, c] = 0
            action_grid_JAL[b, c] += a
            count_grid_JAL[b, c] += 1

    # Compute means
    with np.errstate(invalid='ignore'):
        action_grid_IL = action_grid_IL / count_grid_IL
        action_grid_JAL = action_grid_JAL / count_grid_JAL

    # Mesh for plotting
    battery_ticks = np.arange(battery_levels)
    channel_ticks = np.arange(channel_levels)
    X, Y = np.meshgrid(battery_ticks, channel_ticks, indexing='ij')

    # Plot side-by-side
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    # IL plot
    im1 = axs[0].pcolormesh(X, Y, action_grid_IL, shading='auto', cmap='viridis')
    axs[0].set_title("IL: Battery vs Channel vs Action", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Battery Level", fontsize=12, fontweight='bold')
    axs[0].set_ylabel("Channel State", fontsize=12, fontweight='bold')
    axs[0].set_xticks(battery_ticks)
    axs[0].set_yticks(channel_ticks)
    axs[0].grid(alpha=0.3, linestyle='--')
    plt.colorbar(im1, ax=axs[0], label="Average Action", shrink=0.85)

    # JAL plot
    im2 = axs[1].pcolormesh(X, Y, action_grid_JAL, shading='auto', cmap='viridis')
    axs[1].set_title("JAL: Battery vs Channel vs Action", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Battery Level", fontsize=12, fontweight='bold')
    axs[1].set_ylabel("Channel State", fontsize=12, fontweight='bold')
    axs[1].set_xticks(battery_ticks)
    axs[1].set_yticks(channel_ticks)
    axs[1].grid(alpha=0.3, linestyle='--')
    plt.colorbar(im2, ax=axs[1], label="Average Action", shrink=0.85)

    # Save
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()
    print(f"✅ Comparison plot saved: {full_path}")


def plot_discrete_joint_decision_comparison_scatter(
    BT_user_IL, CH_user_IL, AC_user_IL,
    BT_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="plots",
    output_filename="discrete_joint_decision_scatter_comparison.pdf",
    battery_levels=6, channel_levels=8
):
    """
    Compare IL vs JAL discrete joint Battery vs Channel vs Action maps
    using scatter plot version (similar to academic paper style).
    """

    # Flatten all data
    battery_IL = BT_user_IL.flatten().astype(int)
    channel_IL = CH_user_IL.flatten().astype(int)
    actions_IL = AC_user_IL.flatten()

    battery_JAL = BT_user_JAL.flatten().astype(int)
    channel_JAL = CH_user_JAL.flatten().astype(int)
    actions_JAL = AC_user_JAL.flatten()

    # Initialize grid storage
    sum_actions_IL = np.zeros((battery_levels, channel_levels))
    count_IL = np.zeros((battery_levels, channel_levels))

    sum_actions_JAL = np.zeros((battery_levels, channel_levels))
    count_JAL = np.zeros((battery_levels, channel_levels))

    # Fill IL statistics
    for b, c, a in zip(battery_IL, channel_IL, actions_IL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            sum_actions_IL[b, c] += a
            count_IL[b, c] += 1

    # Fill JAL statistics
    for b, c, a in zip(battery_JAL, channel_JAL, actions_JAL):
        if 0 <= b < battery_levels and 0 <= c < channel_levels:
            sum_actions_JAL[b, c] += a
            count_JAL[b, c] += 1

    # Compute average actions
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_action_IL = np.divide(sum_actions_IL, count_IL, out=np.zeros_like(sum_actions_IL), where=count_IL!=0)
        avg_action_JAL = np.divide(sum_actions_JAL, count_JAL, out=np.zeros_like(sum_actions_JAL), where=count_JAL!=0)

    # Plotting scatter style like your attached figure
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    vmin, vmax = 0, battery_levels - 1  # color scale range

    # IL plot
    for b in range(battery_levels):
        for c in range(channel_levels):
            color = avg_action_IL[b, c] if count_IL[b, c] > 0 else 0
            axs[0].scatter(b, c, c=color, cmap='jet', vmin=vmin, vmax=vmax, s=300, edgecolor='black')
    axs[0].set_title("IL: Policy Mapping", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Battery Level", fontsize=12, fontweight='bold')
    axs[0].set_ylabel("Channel State", fontsize=12, fontweight='bold')
    axs[0].set_xticks(range(battery_levels))
    axs[0].set_yticks(range(channel_levels))
    axs[0].grid(True, linestyle='--', alpha=0.5)

    # JAL plot
    for b in range(battery_levels):
        for c in range(channel_levels):
            color = avg_action_JAL[b, c] if count_JAL[b, c] > 0 else 0
            axs[1].scatter(b, c, c=color, cmap='jet', vmin=vmin, vmax=vmax, s=300, edgecolor='black')
    axs[1].set_title("JAL: Policy Mapping", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Battery Level", fontsize=12, fontweight='bold')
    axs[1].set_ylabel("Channel State", fontsize=12, fontweight='bold')
    axs[1].set_xticks(range(battery_levels))
    axs[1].set_yticks(range(channel_levels))
    axs[1].grid(True, linestyle='--', alpha=0.5)

    # Shared colorbar
    norm = plt.Normalize(vmin, vmax)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axs, fraction=0.04, pad=0.04)
    cbar.set_label("Average Action", fontsize=12, fontweight='bold')

    # Save high-res PDF
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()

    print(f"✅ Scatter comparison plot saved: {full_path}")



# You just pass your IL and JAL full data:
plot_discrete_joint_decision_comparison(
    Bt_user_IL, CH_user_IL, AC_user_IL,
    Bt_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="scatter_plots_2July",
    output_filename="IL_vs_JAL_U100_S50_C.pdf"
)


plot_discrete_joint_decision_comparison_scatter(
    Bt_user_IL, CH_user_IL, AC_user_IL,
    Bt_user_JAL, CH_user_JAL, AC_user_JAL,
    output_dir="scatter_plots_2July",
    output_filename="IL_vs_JAL_scatter_U100_S50_C.pdf"
)
