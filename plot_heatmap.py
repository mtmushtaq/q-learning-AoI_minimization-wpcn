import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import Normalize, LinearSegmentedColormap
from data_npy_io import load_test_matrix_npy, load_test_vector_npy

# Configuration
users = 100
tests_to_plot = 100
battery_levels = 6   # 0..5
channel_levels = 8   # 0..7

# Directories
BASE_DIR_IL  = Path(r"E:/IL_U100")
BASE_DIR_JAL = Path(r"C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q learning Paper\Data July\JAL_U100")

# Helper: load full matrices for a given method and slot
def load_data(method, slot):
    suffix = '_c' if method in ('IL', 'JAL') else ''
    base_dir = BASE_DIR_IL if method == 'IL' else BASE_DIR_JAL
    folder = base_dir / f"{method}_S_{slot}_U_{users}{suffix}"
    AC = load_test_matrix_npy("AC_user_tests", str(folder))[:tests_to_plot, :, :]
    BT = load_test_matrix_npy("BT_user_tests", str(folder))[:tests_to_plot, :, :]
    CH = load_test_matrix_npy("CH_user_tests", str(folder))[:tests_to_plot, :, :]
    return BT, CH, AC

# Build heatmap grid (mean action) for a given method
def compute_action_grid(BT, CH, AC):
    grid_sum = np.zeros((battery_levels, channel_levels))
    grid_count = np.zeros((battery_levels, channel_levels))
    # accumulate over tests and users
    for t in range(tests_to_plot):
        for u in range(users):
            b = int(BT[t, -1, u])  # final battery frame
            c = int(CH[t, -1, u])  # final channel state
            a = AC[t, -1, u]       # final action
            if 0 <= b < battery_levels and 0 <= c < channel_levels:
                grid_sum[b, c] += a
                grid_count[b, c] += 1
    # compute mean action
    with np.errstate(divide='ignore', invalid='ignore'):
        grid = np.divide(grid_sum, grid_count, out=np.zeros_like(grid_sum), where=grid_count > 0)
    return grid

# Custom colormap: light green to dark purple
cdict = {
    'red':   [(0.0, 0.8, 0.8), (0.5, 0.2, 0.2), (1.0, 0.4, 0.4)],
    'green': [(0.0, 1.0, 1.0), (0.5, 0.8, 0.8), (1.0, 0.2, 0.2)],
    'blue':  [(0.0, 0.6, 0.6), (0.5, 0.4, 0.4), (1.0, 0.6, 0.6)]
}
custom_cmap = LinearSegmentedColormap('GreenPurple', segmentdata=cdict, N=256)

# Plot heatmap and scatter comparison
def plot_discrete_joint_decision_comparison(BT_IL, CH_IL, AC_IL,
                                           BT_JAL, CH_JAL, AC_JAL,
                                           output_dir="plots",
                                           output_filename="policy_heatmap_comparison.pdf"):
    # compute grids
    grid_IL = compute_action_grid(BT_IL, CH_IL, AC_IL)
    grid_JAL = compute_action_grid(BT_JAL, CH_JAL, AC_JAL)

    # shared color scale
    vmin = min(np.nanmin(grid_IL), np.nanmin(grid_JAL))
    vmax = max(np.nanmax(grid_IL), np.nanmax(grid_JAL))
    norm = Normalize(vmin=vmin, vmax=vmax)

    # Heatmaps
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), dpi=600)
    for ax, grid, title in zip(axs, [grid_IL, grid_JAL], ['IL', 'JAL']):
        im = ax.imshow(grid, cmap=custom_cmap, norm=norm, origin='lower', aspect='auto')
        ax.set_title(f"{title}: Battery vs Channel Action", fontsize=14, fontweight='bold')
        ax.set_xlabel('Channel State', fontsize=12, fontweight='bold')
        ax.set_ylabel('Battery Level', fontsize=12, fontweight='bold')
        ax.set_xticks(np.arange(channel_levels))
        ax.set_yticks(np.arange(battery_levels))
        ax.tick_params(labelsize=10)
    # shared colorbar
    cbar = fig.colorbar(im, ax=axs.tolist(), fraction=0.046, pad=0.04)
    cbar.set_label('Average Action', fontsize=12, fontweight='bold')
    cbar.ax.tick_params(labelsize=10)

    # Scatter maps
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    for ax, grid, title in zip(axs2, [grid_IL, grid_JAL], ['IL', 'JAL']):
        for b in range(battery_levels):
            for c in range(channel_levels):
                ax.scatter(c, b, c=grid[b, c], cmap=custom_cmap, norm=norm,
                           s=300, edgecolors='k')
        ax.set_title(f"{title}: Scatter Action Map", fontsize=14, fontweight='bold')
        ax.set_xlabel('Channel State', fontsize=12, fontweight='bold')
        ax.set_ylabel('Battery Level', fontsize=12, fontweight='bold')
        ax.set_xticks(np.arange(channel_levels))
        ax.set_yticks(np.arange(battery_levels))
        ax.tick_params(labelsize=10)
    # colorbar for scatter
    cbar2 = fig2.colorbar(im, ax=axs2.tolist(), fraction=0.046, pad=0.04)
    cbar2.set_label('Average Action', fontsize=12, fontweight='bold')
    cbar2.ax.tick_params(labelsize=10)

    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(Path(output_dir)/output_filename, bbox_inches='tight')
    fig2.savefig(Path(output_dir)/output_filename.replace('.pdf','_scatter.pdf'), bbox_inches='tight')
    plt.show()

# Usage example
if __name__ == '__main__':
    # load data for slot=100 or adjust
    slot = 160
    BT_IL, CH_IL, AC_IL   = load_data('IL', slot)
    BT_JAL, CH_JAL, AC_JAL = load_data('JAL', slot)
    plot_discrete_joint_decision_comparison(
        BT_IL, CH_IL, AC_IL,
        BT_JAL, CH_JAL, AC_JAL,
        output_dir="Heatmap_Plots",
        output_filename="policy_heatmap_S160.pdf"
    )
