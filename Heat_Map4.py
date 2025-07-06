import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import Normalize, LinearSegmentedColormap
from data_npy_io import load_test_matrix_npy

# Configuration
users = 100
tests_to_plot = 100
battery_levels = 6  # 0..5
channel_levels = 8  # 0..7
slots = [250, 225, 200, 160, 133, 100, 75, 50]
gains = [round(users/s,3) for s in slots]

# Directories
BASE_DIR_IL  = Path(r"E:/IL_U100")
BASE_DIR_JAL = Path(r"C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q learning Paper\Data July\JAL_U100")

# Helper to load data
def load_data(method, slot):
    base_dir = BASE_DIR_IL if method=='IL' else BASE_DIR_JAL
    folder = base_dir / f"{method}_S_{slot}_U_{users}_c"
    AC = load_test_matrix_npy("AC_user_tests", str(folder))[:tests_to_plot,:,:]
    BT = load_test_matrix_npy("BT_user_tests", str(folder))[:tests_to_plot,:,:]
    CH = load_test_matrix_npy("CH_user_tests", str(folder))[:tests_to_plot,:,:]
    return BT, CH, AC

# Compute heatmap grid for mean action
def compute_action_grid(BT, CH, AC):
    grid_sum = np.zeros((battery_levels, channel_levels))
    grid_count = np.zeros((battery_levels, channel_levels))
    for t in range(tests_to_plot):
        for f in range(BT.shape[1]):
            for u in range(users):
                b = int(BT[t,f,u]); c = int(CH[t,f,u]); a = AC[t,f,u]
                if 0<=b<battery_levels and 0<=c<channel_levels:
                    grid_sum[b,c] += a; grid_count[b,c] += 1
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.divide(grid_sum, grid_count, out=np.zeros_like(grid_sum), where=grid_count>0)

# Custom colormap: orange to purple
dict_c = {
    'red':   [(0,1,1),(1,0.4,0.4)],
    'green': [(0,0.8,0.8),(1,0,0)],
    'blue':  [(0,0.2,0.2),(1,0.6,0.6)]
}
custom_cmap = LinearSegmentedColormap('OrangePurple', dict_c, 256)

# Plot 4×4 grid of heatmaps
def plot_full_grid(output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(4, 4, figsize=(14, 10), dpi=300)
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    # compute all grids
    grids = {'IL': [], 'JAL': []}
    for method in ('IL', 'JAL'):
        for slot in slots:
            BT, CH, AC = load_data(method, slot)
            grids[method].append(compute_action_grid(BT, CH, AC))

    # shared color normalization
    all_vals = np.concatenate([np.array(grids['IL']).ravel(), np.array(grids['JAL']).ravel()])
    norm = Normalize(vmin=np.nanmin(all_vals), vmax=np.nanmax(all_vals))

    # Plot heatmaps
    for m_idx, method in enumerate(('IL', 'JAL')):
        for idx in range(8):
            row = m_idx*2 + (0 if idx < 4 else 1)
            col = idx % 4
            ax = axes[row, col]
            grid = grids[method][idx]
            im = ax.imshow(grid, cmap=custom_cmap, norm=norm,
                           origin='lower', aspect='auto')

            # Title
            ax.set_title(f"{method}, G={gains[idx]}", fontsize=10, fontweight='bold')
            # Ticks
            ax.set_xticks(np.arange(channel_levels)); ax.set_yticks(np.arange(battery_levels))
            ax.tick_params(labelsize=8, width=1, length=3)
            # Axis labels on leftmost & bottom
            if col == 0:
                ax.set_ylabel(r"Battery, $\zeta$", fontsize=9, fontweight='bold')
            if row == 3:
                ax.set_xlabel(r"Channel, $\Upsilon$", fontsize=9, fontweight='bold')

            # Colorbar for each
            cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01)
            cbar.ax.tick_params(labelsize=6)

    plt.tight_layout()
    fig.savefig(Path(output_dir)/filename, bbox_inches='tight')
    plt.show()

# main
def main():
    plot_full_grid('Heatmap_Plots', 'full_IL_JAL_gridC.pdf')

if __name__ == '__main__':
    main()
