import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from data_npy_io import load_test_matrix_npy
import matplotlib.ticker as mticker


# Configuration
tests_to_plot = 100  # plot first 100 tests
users = 100           # number of users (M)

# Gain settings
gains = [0.4, 1.0, 1.33, 2.0]
slots = [250, 100, 75, 50]

# Methods and base directories
table = {
    'IL':    {'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data July\IL_U100'),   'color': 'tab:blue',   'marker':'o', 'linestyle':'-'},
    'JAL':   {'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data July\JAL_U100'), 'color': 'tab:orange', 'marker':'s', 'linestyle':'--'},
    'Dist':  {'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data July\Dist_U100'), 'color': 'tab:purple', 'marker':'^', 'linestyle':'-.'},
    'IRSA':  {'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data July\IRSA_U100'),'color': 'tab:green',  'marker':'D', 'linestyle':':'}
}
# Legend names override
legend_name = {'Dist':'EH-IRSA', 'IRSA':'IRSA'}

# Load mean battery per test
def load_battery_mean(folder, key='BT_user_tests', method=None):
    arr = load_test_matrix_npy(key, str(folder))[:tests_to_plot, :, :]
    if method == 'Dist':
        arr = arr / 2.0
    return arr.mean(axis=(1,2))

# Plot battery performance across gains
def plot_battery_all_gains(save_dir, output_name, smoothing_window=3):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 4, figsize=(16, 8), dpi=600, sharey=False)

    for idx, (g, slot) in enumerate(zip(gains, slots)):
        row, col = divmod(idx, 4)
        ax = axes[row, col]

        # Plot each method
        for method, cfg in table.items():
            # folder name suffix
            suffix = '_c' if method in ('IL','JAL') else ''
            folder_name = f"{method}_S_{slot}_U_{users}{suffix}"
            folder = cfg['base_dir'] / folder_name
            data = load_battery_mean(folder, method=method)

            # smooth curve
            smooth = pd.Series(data).rolling(window=smoothing_window,
                                            min_periods=1, center=True).mean()
            x = np.arange(len(smooth))
            ax.plot(x, smooth,
                    color=cfg['color'], linestyle=cfg['linestyle'], linewidth=2,
                    label=legend_name.get(method, method))
            # markers every 20 tests
            m_x = x[::20]; m_y = smooth[::20]
            ax.plot(m_x, m_y, linestyle='None', marker=cfg['marker'],
                    color=cfg['color'], markersize=6)

        # formatting
        ax.set_title(f"G={g}", fontsize=12, fontweight='bold')
        ax.set_xticks(np.arange(0, tests_to_plot+1, 20))
        ax.tick_params(axis='x', labelsize=12, width=1.5, length=6)

        # y-axis only label on first column
        if col == 0:
            ax.set_ylabel('Average Available Battery Units', fontsize=12, fontweight='bold')

        if row == 1:
            ax.set_xlabel('Test', fontsize=12, fontweight='bold')
        # grid
        ax.grid(True, linestyle='--', alpha=0.5)

        # legend per subplot, placed top right
        ax.legend(fontsize=8, loc='upper right', frameon=False)

    # Bold tick labels for all
    for ax in axes.flatten():
        ax.tick_params(axis='y', labelsize=12, width=1.5, length=6)
        for lbl in ax.get_xticklabels()+ax.get_yticklabels():
            lbl.set_fontweight('bold')

    fig.suptitle('Average Available Battery Units over First 100 Tests across Gains',
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))

    out_file = save_path / f"{output_name}_battery_gains.pdf"
    fig.savefig(out_file)
    plt.show()

def plot_battery_all_gains_log(save_dir, output_name, smoothing_window=3):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=600, sharey=False)

    for idx, (g, slot) in enumerate(zip(gains, slots)):
        row, col = divmod(idx, 2)
        ax = axes[row, col]

        # Plot each method
        for method, cfg in table.items():
            suffix = '_c' if method in ('IL', 'JAL') else ''
            folder_name = f"{method}_S_{slot}_U_{users}{suffix}"
            folder = cfg['base_dir'] / folder_name
            data = load_battery_mean(folder, method=method)

            # Smooth the curve
            smooth = pd.Series(data).rolling(
                window=smoothing_window, min_periods=1, center=True
            ).mean()
            x = np.arange(len(smooth))
            ax.plot(
                x, smooth,
                color=cfg['color'], linestyle=cfg['linestyle'], linewidth=2,
                label=legend_name.get(method, method)
            )
            # markers every 20 tests
            m_x = x[::20]; m_y = smooth[::20]
            ax.plot(
                m_x, m_y, linestyle='None', marker=cfg['marker'],
                color=cfg['color'], markersize=6
            )

        # Formatting
        ax.set_title(f"G={g}", fontsize=15, fontweight='light')
        ax.set_xticks(np.arange(0, tests_to_plot+1, 20))
        ax.tick_params(axis='x', labelsize=12, width=1.5, length=6)

        # Log scale and equal y‑limits [0,5]
        ax.set_yscale('log')
        ax.set_ylim(0.3, 5.2)          # since log scale, use appropriate range
        #ax.set_ylim(0.3, 5.2)          # or convert your data to powers-of-10
        # Set y-ticks manually at finer granularity
        yticks = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
        ax.set_yticks(yticks)
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())  # show actual numbers

        # If your raw battery values range 1–5, you can instead do:
        # ax.set_ylim(0.1, 10)

        # y-axis label only on first column
        if col == 0:
            ax.set_ylabel(r"$\bar{\zeta}(t; G)$", fontsize=15, fontweight='light')

        # x-axis label on bottom row
        if row == 1:
            ax.set_xlabel('Test Index', fontsize=15, fontweight='light')

        ax.grid(True, linestyle='--', alpha=0.5, which='both')
        ax.legend(fontsize=8, loc='upper right', frameon=False)

    # Bold tick labels everywhere
    for ax in axes.flatten():
        ax.tick_params(axis='y', labelsize=12, width=1.5, length=6)
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontweight('bold')

    #fig.suptitle(
     #   r"$\bar{\zeta}(t; G)$ over First 100 Tests across Gains",
      #  fontsize=14, fontweight='bold'
    #)
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))

    out_file = save_path / f"{output_name}_battery_gains.pdf"
    fig.savefig(out_file)
    plt.show()


if __name__ == '__main__':
    plot_battery_all_gains_log('BatteryPlots_all', 'BT_4')
