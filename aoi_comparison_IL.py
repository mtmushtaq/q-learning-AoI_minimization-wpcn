import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from data_npy_io import load_test_matrix_npy

# Configuration
tests_to_plot = 200  # number of tests to include on x-axis
users = 100  # number of users (M)

# Methods and their gain settings
# slots correspond to gains = users/slots
slots = [200, 133, 100]
gains = [round(users / s, 3) for s in slots]

# Assign a bright color to each gain for solid plotting
gain_colors = {
    gains[0]: 'purple',  # G=0.5
    gains[1]: 'green',  # G=0.75
    gains[2]: 'orange'  # G=1.0
}

table = {
    'IL': {
        'base_dir': Path(r'E:/IL_U100'),
        'linestyle': '-',
        'marker': 'o'
    },
    'JAL': {
        'base_dir': Path(r'E:/JAL_U100'),
        'linestyle': '--',
        'marker': 's'
    }
}


# Helper to load final AAoI per test
def compute_final_aaoi(folder, key="AOI_test_iter"):
    try:
        aoi_all = load_test_matrix_npy(key, str(folder))[:tests_to_plot, :, :]
        return aoi_all[:, -1, :].mean(axis=1) / users
    except Exception as e:
        print(f"Failed to load from {folder}: {e}")
        return np.full(tests_to_plot, np.nan)


# Plotting

def plot_aoi_comparison(methods_map, output_path):
    plt.figure(figsize=(10, 6), dpi=600)
    for name, cfg in methods_map.items():
        for s, g in zip(slots, gains):
            # build folder name
            folder_name = f"{name}_S_{s}_U_{users}" + ('_c' if name == 'IL' else '')
            folder = cfg['base_dir'] / folder_name
            data = compute_final_aaoi(folder)
            # smooth
            smooth = pd.Series(data).rolling(window=5, min_periods=1, center=True).mean()
            x = np.arange(tests_to_plot)
            interp = pd.Series(smooth).interpolate(method='cubic')
            color = gain_colors[g]
            # plot
            plt.plot(
                x, interp,
                color=color,
                linestyle=cfg['linestyle'],
                linewidth=2,
                label=f"{name}, G={g}"
            )
            # markers every 20
            m_x = x[::20]
            m_y = interp[::20]
            plt.plot(
                m_x, m_y,
                linestyle='None',
                marker=cfg['marker'],
                color=color,
                markersize=6
            )

    # Styling
    tick_params = {'axis': 'both', 'which': 'major', 'labelsize': 12, 'width': 1.5, 'length': 6}
    plt.tick_params(**tick_params)
    plt.xlabel('Test Index', fontsize=14, fontweight='bold')
    plt.ylabel(r"Normalized AAoI $A_{norm}$", fontsize=14, fontweight='bold')
    plt.title(r"$A_{norm}$ over Tests for IL and JAL at Various Gains", fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=11, ncol=3)
    plt.tight_layout()
    os.makedirs(output_path.parent, exist_ok=True)
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    out_folder = Path('aoi_comparison_IL_JAL')
    output_file = out_folder / 'aoi_comparison_IL_JAL.pdf'
    plot_aoi_comparison(table, output_file)
