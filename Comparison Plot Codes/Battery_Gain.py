import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from data_npy_io import load_test_matrix_npy
import matplotlib.ticker as mticker

# Configuration
users = 100
gains = [0.4, 0.44, 0.5, 0.6, 0.75, 1.0, 1.33, 2.0]
slots = [250, 225, 200, 160, 133, 100, 75, 50]

table = {
    'IL':    {'base_dir': Path(r'C:/Users/Tauseef/OneDrive - Politecnico di Bari/AOI Q learning Infocom/Data July/IL_U100'),   'color': 'tab:blue',   'marker': 'o', 'linestyle': '-'},
    'JAL':   {'base_dir': Path(r'C:/Users/Tauseef/OneDrive - Politecnico di Bari/AOI Q Learning Infocom/Data July/JAL_U100'),  'color': 'tab:orange','marker': 's', 'linestyle': '--'},
    'Dist':  {'base_dir': Path(r'C:/Users/Tauseef/OneDrive - Politecnico di Bari/AOI Q Learning Infocom/Data July/Dist_U100'), 'color': 'tab:purple','marker': '^', 'linestyle': '-.'},
    'IRSA':  {'base_dir': Path(r'C:/Users/Tauseef/OneDrive - Politecnico di Bari/AOI Q Learning Infocom/Data July/IRSA_U100'), 'color': 'tab:green', 'marker': 'D', 'linestyle': ':'}
}
legend_name = {'Dist': 'EH-IRSA', 'IRSA': 'IRSA'}

def plot_final_battery_vs_gain(output_file="Final_Battery_vs_Gain.pdf"):
    plt.figure(figsize=(8, 5), dpi=600)

    for method, cfg in table.items():
        avg_battery_last_test = []

        for slot in slots:
            suffix = "_c" if method in ['IL', 'JAL'] else ""
            folder_name = f"{method}_S_{slot}_U_{users}{suffix}"
            folder = cfg["base_dir"] / folder_name

            try:
                bt = load_test_matrix_npy("BT_user_tests", str(folder))  # shape: (tests, users, time)
                last_test_avg = bt[-1].mean()
                if method == "Dist":
                    last_test_avg /= 2.0
                avg_battery_last_test.append(last_test_avg)
            except Exception as e:
                print(f"⚠️ Could not load from {folder}: {e}")
                avg_battery_last_test.append(np.nan)

        sorted_data = sorted(zip(gains, avg_battery_last_test))
        sorted_gains, sorted_values = zip(*sorted_data)

        plt.plot(sorted_gains, sorted_values,
                 label=legend_name.get(method, method),
                 color=cfg['color'],
                 marker=cfg['marker'],
                 linestyle=cfg['linestyle'],
                 linewidth=2, markersize=7)

    plt.xlabel(r"Normalized Channel Traffic $G$", fontsize=15, fontweight='light')
    plt.ylabel(r"Final Avg. Battery Units $\bar{\zeta}(T; G)$", fontsize=15, fontweight='light')
    #plt.title("Average Battery Level ", fontsize=13, fontweight='bold')
    plt.yscale('log')
    plt.ylim(0.3, 5.15)

    # Force fixed ticks and proper formatting
    yticks = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    plt.gca().yaxis.set_major_locator(mticker.FixedLocator(yticks))
    plt.gca().yaxis.set_major_formatter(mticker.ScalarFormatter())

    plt.yticks(fontsize=11, fontweight='bold')  # apply style to those ticks
    plt.grid(True, linestyle='--', alpha=0.5, which='both')
    plt.legend(fontsize=10)
    plt.xticks(fontsize=11, fontweight='bold')
    # ❌ DO NOT add another plt.yticks() here
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')  # Optional: save to file
    plt.show()  # Required: actually displays the plot window


if __name__ == "__main__":
    plot_final_battery_vs_gain()
