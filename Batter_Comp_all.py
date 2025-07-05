import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from data_npy_io import load_test_matrix_npy

# Configuration
tests_to_plot = 100  # only plot first 100 tests to match Dist method
users = 100           # number of users (M)

# Gain settings (manual slots to avoid rounding errors)
gains = [0.4, 0.44, 0.5, 0.6, 0.75, 1.0, 1.33, 2.0]
slots = [250, 225, 200, 160, 133, 100, 75, 50]

# Methods and base directories
table = {
    'IL':    {'base_dir': Path(r'E:/IL_U100'),   'color': 'tab:blue',   'marker':'o', 'linestyle':'-'},
    'JAL':   {'base_dir': Path(r'E:/JAL_U100'),  'color': 'tab:orange', 'marker':'s', 'linestyle':'--'},
    'Dist':  {'base_dir': Path(r'E:/Dist_U100'), 'color': 'tab:purple', 'marker':'^', 'linestyle':'-.'},
    'Random':{'base_dir': Path(r'E:/Random_U100'),'color': 'tab:green',  'marker':'D', 'linestyle':':'}
}

# Helper to load mean battery over tests for given folder
def load_battery_mean(folder, key='BT_user_tests', tests=tests_to_plot, method=None):
    arr = load_test_matrix_npy(key, str(folder))[:tests, :, :]
    if method == 'Dist':
        arr = arr / 3.0
    return arr.mean(axis=(1,2))

# Plot battery performance across gains
def plot_battery_all_gains(save_dir, output_name, smoothing_window=3):
    # Prepare output dir
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 4, figsize=(16, 8), dpi=600, sharey=False)

    for idx, (g, slot) in enumerate(zip(gains, slots)):
        row, col = divmod(idx, 4)
        ax = axes[row, col]

        # Plot each method on this gain
        for method, cfg in table.items():
            # Build folder
            name = f"{method}_S_{slot}_U_{users}" + ("_c" if method=='IL' else "")
            folder = cfg['base_dir'] / name
            data = load_battery_mean(folder, method=method)

            # Smooth
            smooth = pd.Series(data).rolling(window=smoothing_window,
                                              min_periods=1, center=True).mean()
            x = np.arange(len(smooth))
            ax.plot(x, smooth, color=cfg['color'], linestyle=cfg['linestyle'],
                    linewidth=2)
            # Markers every 20 tests
            m_x = x[::20]; m_y = smooth[::20]
            ax.plot(m_x, m_y, linestyle='None', marker=cfg['marker'],
                    color=cfg['color'], markersize=6)

        # Subplot formatting
        ax.set_title(f"G={g}", fontsize=12, fontweight='bold')
        ax.set_xticks(np.arange(0, tests_to_plot+1, 20))
        ax.tick_params(axis='x', labelsize=12, width=1.5, length=6)

        if col == 0:
            ax.set_ylabel('Average Available Battery Units', fontsize=12, fontweight='bold')
            ax.tick_params(axis='y', labelsize=12, width=1.5, length=6)
        else:
            # hide only the axis label (not tick labels)
            ax.set_ylabel('')
        ax.grid(True, linestyle='--', alpha=0.5)

        # Legend inside first subplot reflecting line and marker styles
    # Create dummy handles for each method to correctly show color, linestyle, and marker
    legend_handles = []
    legend_labels = []
    for method, cfg in table.items():
        # dummy line
        handle, = axes[0,3].plot([], [],
            color=cfg['color'],
            linestyle=cfg['linestyle'],
            marker=cfg['marker'],
            markersize=6,
            label=method
        )
        legend_handles.append(handle)
        legend_labels.append(method)
    axes[0,3].legend(legend_handles, legend_labels,
                     fontsize=10, loc='upper right', frameon=False)

    # Make tick labels bold
    for ax in axes.flatten():
        for label in ax.get_xticklabels():
            label.set_fontweight('bold')
        # only first column shows y-tick labels
        if ax in axes[:,0]:
            for label in ax.get_yticklabels():
                label.set_fontweight('bold')

    fig.suptitle('Average Available Battery Units over First 100 Tests across Gains',
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))

    # Save
    out_file = save_path / f"{output_name}_battery_gains.pdf"
    fig.savefig(out_file)
    plt.show()

if __name__ == '__main__':
    plot_battery_all_gains('BatteryPlots_all', 'BT_AllGains2')
