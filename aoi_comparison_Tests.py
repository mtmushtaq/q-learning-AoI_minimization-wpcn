import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from data_npy_io import load_test_matrix_npy
from matplotlib.lines import Line2D

# Configuration
tests_to_plot = 200
users = 100

slots = [200, 133, 100]
gains = [round(users / s, 2) for s in slots]

gain_colors = {
    gains[0]: 'purple',
    gains[1]: 'green',
    gains[2]: 'orange'
}

table = {
    'IL': {
        'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data 10 June\IL_U100'),
        'linestyle': '-',
        'marker': 'o'
    },
    'JAL': {
        'base_dir': Path(r'C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q Learning Infocom\Data 10 June\JAL_U100'),
        'linestyle': '--',
        'marker': 's'
    }
}


def compute_final_aaoi(folder, key="AOI_test_iter"):
    try:
        aoi_all = load_test_matrix_npy(key, str(folder))
        print(f"Loaded AOI shape from {folder}: {aoi_all.shape}")
        effective_tests = min(tests_to_plot, aoi_all.shape[0])
        aoi_all = aoi_all[:effective_tests, :, :]
        return aoi_all[:, -1, :].mean(axis=1) / users
    except Exception as e:
        print(f"Failed to load from {folder}: {e}")
        return np.full(tests_to_plot, np.nan)


def plot_aoi_comparison(methods_map, output_path):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=600)

    handles_IL = []
    handles_JAL = []

    for name, cfg in methods_map.items():
        for s, g in zip(slots, gains):
            folder_name = f"{name}_S_{s}_U_{users}"
            folder = cfg['base_dir'] / folder_name
            data = compute_final_aaoi(folder)

            smooth = pd.Series(data).rolling(window=5, min_periods=1, center=True).mean()
            x = np.arange(len(smooth))
            interp = pd.Series(smooth).interpolate(method='cubic')
            color = gain_colors[g]

            # Plot line
            ax.plot(
                x, interp,
                color=color,
                linestyle=cfg['linestyle'],
                linewidth=2
            )

            # Plot markers every 20
            ax.plot(
                x[::20], interp[::20],
                linestyle='None',
                marker=cfg['marker'],
                color=color,
                markersize=6
            )

            # Save handle for legend
            handle = Line2D([0], [0],
                            color=color,
                            linestyle=cfg['linestyle'],
                            marker=cfg['marker'],
                            label=f"EE-{name}, G={g}")
            if name == 'IL':
                handles_IL.append(handle)
            else:
                handles_JAL.append(handle)

    # Axis styling
    ax.set_xlabel('Test Index', fontsize=15, fontweight='light')
    ax.set_ylabel(r"Normalized AAoI $\bar{A}_{norm}$", fontsize=15, fontweight='light')
    ax.tick_params(axis='both', which='major', labelsize=12, width=1.5, length=6)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Remove padding and force tight limits on x-axis
    ax.set_xlim(0, tests_to_plot - 1)
    ax.set_xticks(np.linspace(0, tests_to_plot, num=11, endpoint=True, dtype=int))

    # Combined legend inside the grid area (top-right, 2 columns)
    combined_handles = []
    combined_labels = []

    # Combine in gain order: EE-IL, EE-JAL per gain
    for h_il, h_jal in zip(handles_IL, handles_JAL):
        combined_handles.extend([h_il, h_jal])
        combined_labels.extend([h_il.get_label(), h_jal.get_label()])

    # Place inside the plot, upper-right
    ax.legend(combined_handles, combined_labels,
              fontsize=10, loc='upper right',
              ncol=2, frameon=False, columnspacing=1.0, handletextpad=0.5)

    plt.tight_layout()
    os.makedirs(output_path.parent, exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.show()



if __name__ == '__main__':
    out_folder = Path('aoi_4Gs_IL_JAL')
    output_file = out_folder / 'aoi_comparison_IL_JAL_matrix_legend.pdf'
    plot_aoi_comparison(table, output_file)
