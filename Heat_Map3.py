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

# Plot 4×8 grid of heatmaps: rows 0-1 IL, 2-3 JAL

def plot_full_grid(output_dir, filename):
    import os
    os.makedirs(output_dir, exist_ok=True)

    # 4 rows × 4 cols: rows 0–1 = IL, rows 2–3 = JAL
    fig, axes = plt.subplots(4, 4, figsize=(16, 12), dpi=300)
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    # Precompute all grids
    grids = {'IL': [], 'JAL': []}
    for method in ('IL', 'JAL'):
        for slot in slots:
            BT, CH, AC = load_data(method, slot)
            grids[method].append(compute_action_grid(BT, CH, AC))

    # Shared color normalization
    all_vals = np.concatenate([np.array(grids['IL']).ravel(),
                               np.array(grids['JAL']).ravel()])
    norm = Normalize(vmin=np.nanmin(all_vals), vmax=np.nanmax(all_vals))

    # Plotting
    for m_idx, method in enumerate(('IL', 'JAL')):
        for gain_idx in range(8):
            # Determine row/col
            row = m_idx * 2 + (0 if gain_idx < 4 else 1)
            col = gain_idx % 4
            ax = axes[row, col]

            grid = grids[method][gain_idx]
            im = ax.imshow(grid, cmap=custom_cmap, norm=norm,
                           origin='lower', aspect='auto')

            # Title
            ax.set_title(f"{method}, G={gains[gain_idx]}", fontsize=9)

            # Ticks
            ax.set_xticks(np.arange(channel_levels))
            ax.set_yticks(np.arange(battery_levels))
            ax.tick_params(labelsize=7)

            # Axis labels only on leftmost & bottom
            if col == 0:
                ax.set_ylabel(r"Battery, $\zeta$", fontsize=8)
            if row == 3:
                ax.set_xlabel(r"Channel, $\Upsilon$", fontsize=8)

    # Shared colorbar on the right
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(),
                        fraction=0.02, pad=0.01)
    cbar.set_label('Avg Action', fontsize=10)
    cbar.ax.tick_params(labelsize=8)

    plt.tight_layout()
    fig.savefig(Path(output_dir)/filename, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    plot_full_grid('Heatmap_Plots', 'full_IL_JAL_grid_gain2.pdf')
