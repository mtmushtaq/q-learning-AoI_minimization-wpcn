import numpy as np
import matplotlib.pyplot as plt
import random as rd

import matplotlib
import numpy as np
from numpy import ndarray, dtype
from scipy.signal import square
from State_User import * #generate_rician_fading, gamma_EH, compute_energy_harvested
from Discritize_state import get_dis_BT, get_dis_AT, CH_dist
from SIC import *
from User import User
from Data_IO import *
import os
import matplotlib.patches as patches
from scipy.stats import binned_statistic_2d
#import pandas as pd
from pandas import DataFrame
import scipy.interpolate

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_npy_io import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import Axes3D

Out_dir_JAL = "BT_S_8_U_5_JAL"
Out_dir_IL = "BT_S_8_U_5_IL"

AC_user_IL = load_test_matrix_npy("AC_user_tests", Out_dir_IL)
Bt_user_IL = load_test_vector_npy("BT_user_tests", Out_dir_IL)
CH_user_IL = load_test_matrix_npy("CH_user_tests", Out_dir_IL)
AOI_IL = load_test_matrix_npy("AOI_test_iter", Out_dir_IL)

AC_user_JAL = load_test_matrix_npy("AC_user_tests", Out_dir_JAL)[:200,:,:]
Bt_user_JAL = load_test_vector_npy("BT_user_tests", Out_dir_JAL)[:200,:,:]
CH_user_JAL = load_test_matrix_npy("CH_user_tests", Out_dir_JAL)[:200,:,:]
AOI_JAl = load_test_matrix_npy("AOI_test_iter", Out_dir_JAL)[:200,:,:]


def compute_battery_per_update_general(AOI, AC, slots):
    """
    Accumulates battery consumption between consecutive AoI updates.
    Supports any algorithm (IL, JAL etc.)
    """
    num_tests, num_iters, num_users = AOI.shape
    consumption = []

    for t in range(num_tests):
        for u in range(num_users):
            battery_counter = 0
            for i in range(num_iters):
                battery_counter += AC[t, i, u]

                if AOI[t, i, u] < slots:  # update occurred
                    if battery_counter > 0:
                        consumption.append(battery_counter)
                        battery_counter = 0
    return np.array(consumption)


def plot_battery_efficiency_multiple_algorithms(
        data_dict,
        max_battery=15,   # 🔥 limit here!
        save_pdf=False,
        output_dir="plots",
        filename="battery_efficiency_multi_algorithms.pdf"
):
    """
    Compare battery efficiency histograms for multiple algorithms, limiting extreme values.
    """

    # Compute all consumption arrays
    consumption_dict = {}
    for label, (AOI, AC, slots) in data_dict.items():
        consumption = compute_battery_per_update_general(AOI, AC, slots)
        consumption = consumption[consumption <= max_battery]   # 🔥 limit values
        consumption_dict[label] = consumption

    bins = np.arange(1, max_battery + 2)
    bin_centers = bins[:-1]
    width = 0.8 / len(consumption_dict)

    plt.figure(figsize=(10, 6), dpi=400)

    for idx, (label, consumption) in enumerate(consumption_dict.items()):
        hist, _ = np.histogram(consumption, bins=bins)
        perc = hist / hist.sum() * 100
        plt.bar(bin_centers + (idx - len(consumption_dict)/2)*width, perc,
                width=width, label=label)

    plt.xticks(bin_centers, fontweight='bold')
    plt.xlabel("Accumulated Battery Consumption per Update", fontsize=12, fontweight='bold')
    plt.ylabel("Percentage of Updates (%)", fontsize=12, fontweight='bold')
    plt.title("Battery Cost per AoI Update", fontsize=14, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()

    if save_pdf:
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, filename), format='pdf', dpi=600, bbox_inches='tight')
        print(f"✅ Saved: {os.path.join(output_dir, filename)}")

    plt.show()


def plot_cdf_battery_efficiency(data_dict, max_battery=15, output_dir="plots", filename="battery_efficiency_cdf.pdf"):
    plt.figure(figsize=(10, 6), dpi=400)

    for label, (AOI, AC, slots) in data_dict.items():
        consumption = compute_battery_per_update_general(AOI, AC, slots)
        consumption = consumption[consumption <= max_battery]  # 🔥 truncate outliers

        sorted_vals = np.sort(consumption)
        cdf_vals = np.arange(1, len(sorted_vals)+1) / len(sorted_vals)
        plt.step(sorted_vals, cdf_vals, label=label, linewidth=2)

    plt.xlabel("Battery Consumption per Update", fontsize=12, fontweight='bold')
    plt.ylabel("Cumulative Probability", fontsize=12, fontweight='bold')
    plt.title("CDF: Battery Cost per AoI Update", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), format='pdf', dpi=600, bbox_inches='tight')
    plt.show()


# Example dummy input structure (replace with your loaded npy files)
slots_IL = 8
slots_JAL = 8
data_dict = {
    "IL": (AOI_IL, AC_user_IL, slots_IL),
    "JAL": (AOI_JAl, AC_user_JAL, slots_JAL),
}

# Full Histogram Plot:
plot_battery_efficiency_multiple_algorithms(data_dict, max_battery=15,  save_pdf=True, output_dir="BTresults", filename="battery_hist.pdf")

# CDF Plot:
plot_cdf_battery_efficiency(data_dict, max_battery=15, output_dir="BTresults", filename="battery_cdf.pdf")
