import numpy as np
import matplotlib.pyplot as plt
from data_npy_io import *

# Fixed parameters
users_IL = 40
slots_IL = [20, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
gains_IL = [round(users_IL / s, 3) for s in slots_IL]

#users_JAL = 24
#slots_JAL = [12, 18, 27, 34, 48, 54, 60]
#gains_JAL = [round(users_JAL / s, 3) for s in slots_JAL]

users_JAL = 40
slots_JAL = [20, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
gains_JAL = [round(users_JAL / s, 3) for s in slots_JAL]

users_dist = 20
slots_dist = [10, 15, 20, 25, 30, 35, 40]
gains_dist = [round(users_dist / s, 3) for s in slots_dist]

users_rd = 20
slots_rd = [10, 15, 20, 25, 32, 40, 50]
gains_rd = [round(users_rd / s, 3) for s in slots_rd]
# Corresponding folders (must match slot order)
store_dirs_IL = [
    "S_20_U_40_UP_020", "S_30_U_40_UP_020", "S_35_U_40_UP_020",
    "S_40_U_40_UP_020", "S_45_U_40_UP_020", "S_50_U_40_UP_020",
     "S_70_U_40_UP_020", "S_80_U_40_UP_020",
    "S_90_U_40_UP_020", "S_100_U_40_UP_020"
]
store_dirs_JAL = [ "JAL_S_20_U_40_UP2", "JAL_S_30_U_40_UP2","JAL_S_40_U_40_UP2", "JAL_S_50_U_40_UP2", "JAL_S_60_U_40_UP2", "JAL_S_70_U_40_UP2", "JAL_S_80_U_40_UP2", "JAL_S_90_U_40_UP2", "JAL_S_100_U_40_UP2"]
#store_dirs_JAL = ["JAL_S_18_U_24", "JAL_S_27_U_24", "JAL_S_34_U_24", "JAL_S_48_U_24", "JAL_S_54_U_24", "JAL_S_60_U_24"]
store_dirs_dist = ["Dist_S_10_U_20_UP2", "Dist_S_15_U_20_UP2", "Dist_S_20_U_20_UP2", "Dist_S_25_U_20_UP2", "Dist_S_30_U_20_UP2", "Dist_S_35_U_20_UP2", "Dist_S_40_U_20_UP2"]
store_dirs_rd = ["Random_S_10_U_20_UP2", "Random_S_15_U_20_UP2", "Random_S_20_U_20_UP2", "Random_S_25_U_20_UP2", "Random_S_32_U_20_UP2", "Random_S_40_U_20_UP2", "Random_S_50_U_20_UP2"]

def plot_gain_vs_aaoi_from_dirs(store_dirs, gains, label="IL", color="blue", output_file="IL_gain_vs_aaoi.pdf"):
    """
    Plot Gain vs Final AAoI using provided folders and gains.
    - store_dirs: list of folder paths (same order as slots/gains)
    - gains: list of gain values
    """
    final_aaoi = []

    for folder in store_dirs:
        try:
            aoi_test = load_test_matrix_npy("AOI_test_iter", folder)  # shape: (tests, users)
            last_test_mean = np.mean(aoi_test[-1, :])            # mean over users in final test
            final_aaoi.append(last_test_mean)
        except Exception as e:
            print(f"⚠️ Failed to load AOI from {folder}: {e}")
            final_aaoi.append(np.nan)

    # Clean & sort data
    sorted_data = sorted(zip(gains, final_aaoi))
    sorted_gains, sorted_aaoi = zip(*sorted_data)

    # Plot
    plt.figure(figsize=(8, 5), dpi=300)  # High DPI for clarity in PDF
    plt.plot(
        sorted_gains,
        sorted_aaoi,
        marker='o',
        markersize=8,
        color=color,
        linestyle='--',
        linewidth=2,
        label=label
    )

    # Styling
    plt.xlabel(r"Normalized Channel Traffic $G = \frac{M}{N}$", fontsize=12)
    plt.ylabel(r"Final Average AoI $\bar{A}$", fontsize=12)
    plt.title(r"Gain ($G$) vs Average AoI ($ \bar{A}$)", fontsize=13, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()


def plot_gain_vs_aaoi_comparison(
    store_dirs_IL, gains_IL,
    store_dirs_JAL, gains_JAL,
    output_file="IL_vs_JAL_gain_vs_aaoi.pdf"
):
    """
    Plot Gain vs Final AAoI for both IL and JAL in a single figure.
    """
    def compute_final_aaoi(store_dirs):
        aaoi_list = []
        for folder in store_dirs:
            try:
                aoi_test = load_test_matrix_npy("AOI_test_iter", folder)
                last_test_mean = np.mean(aoi_test[-1, :])
                aaoi_list.append(last_test_mean)
            except Exception as e:
                print(f"⚠️ Failed to load AOI from {folder}: {e}")
                aaoi_list.append(np.nan)
        return aaoi_list

    # Compute AAoI for each algorithm
    aaoi_IL = compute_final_aaoi(store_dirs_IL)
    aaoi_JAL = compute_final_aaoi(store_dirs_JAL)

    # Sort each set by gain
    data_IL = sorted(zip(gains_IL, aaoi_IL))
    data_JAL = sorted(zip(gains_JAL, aaoi_JAL))
    sorted_gains_IL, sorted_aaoi_IL = zip(*data_IL)
    sorted_gains_JAL, sorted_aaoi_JAL = zip(*data_JAL)
    # Convert to arrays
    sorted_aaoi_IL = np.array(sorted_aaoi_IL)
    sorted_aaoi_JAL = np.array(sorted_aaoi_JAL)

    # Normalize by user count
    normalized_aaoi_IL = sorted_aaoi_IL / users_IL
    normalized_aaoi_JAL = sorted_aaoi_JAL / users_JAL

    # Plot
    plt.figure(figsize=(8, 5), dpi=300)

    # IL Line
    plt.plot(sorted_gains_IL, normalized_aaoi_IL,
             marker='o', markersize=8,
             color='blue', linestyle='--', linewidth=2,
             label='IL')

    # JAL Line
    plt.plot(sorted_gains_JAL, normalized_aaoi_JAL,
             marker='s', markersize=8,
             color='darkorange', linestyle='-', linewidth=2,
             label='JAL')

    # Axis Labels & Styling
    plt.xlabel(r"Normalized Channel Traffic $G$", fontsize=12)
    plt.ylabel(r"Normalized Average AoI $\bar{A}_{norm}$", fontsize=12)
    plt.title(r"Comparison of IL and JAL", fontsize=13, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()


def plot_gain_vs_aaoi_multi_comparison(
    methods_data,
    output_file="multi_method_gain_vs_aaoi.pdf",
    normalize_users=True,
    dpi=600
):
    """
    Plot Gain vs Final AAoI comparison for multiple methods.

    Parameters:
    - methods_data: list of tuples (store_dirs, gains, label, color, marker, users)
    - output_file: filename for the saved PDF
    - normalize_users: if True, normalize AAoI by user count
    - dpi: resolution of the saved figure
    """

    def compute_final_aaoi(store_dirs):
        aaoi_list = []
        for folder in store_dirs:
            try:
                aoi_test = np.load(os.path.join(folder, "AOI_test_iter.npy"))
                last_test_mean = np.mean(aoi_test[-1, :])
                aaoi_list.append(last_test_mean)
            except Exception as e:
                print(f"⚠️ Failed to load AOI from {folder}: {e}")
                aaoi_list.append(np.nan)
        return aaoi_list

    plt.figure(figsize=(8, 5), dpi=dpi)

    for store_dirs, gains, label, color, marker, users in methods_data:
        aaoi = compute_final_aaoi(store_dirs)
        sorted_data = sorted(zip(gains, aaoi))
        sorted_gains, sorted_aaoi = zip(*sorted_data)

        sorted_aaoi = np.array(sorted_aaoi)
        if normalize_users:
            sorted_aaoi = sorted_aaoi / users

        plt.plot(sorted_gains, sorted_aaoi,
                 marker=marker, markersize=8,
                 linestyle='--', linewidth=2,
                 label=label, color=color)

    plt.xlabel(r"Normalized Channel Traffic $'G'$", fontsize=12, fontweight='bold')
    plt.ylabel(r"Normalized Average AoI $\bar{A}_{norm}$", fontsize=12, fontweight='bold')
    #plt.title("Gain vs Final Average AoI Across Methods", fontsize=13, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()


# Call the function
#plot_gain_vs_aaoi_from_dirs(store_dirs_IL, gains_IL, label="IL", color="blue")


# Call the function for JAL
#plot_gain_vs_aaoi_from_dirs(store_dirs_JAL, gains_JAL, label="JAL", color="orange", output_file="JAL_gain_vs_aaoi.pdf")

#plot_gain_vs_aaoi_comparison(
 #   store_dirs_IL, gains_IL,
  #  store_dirs_JAL, gains_JAL,
   # output_file="IL_vs_JAL_gain_vs_aaoi.pdf"
#)

methods_data = [
    # IL
    (store_dirs_IL, gains_IL, "IL", "blue", 'o', users_IL),

    # JAL
    (store_dirs_JAL, gains_JAL, "JAL", "darkorange", 's', users_JAL),

    # Random
    (store_dirs_rd, gains_rd, "Random", "green", 'D', users_rd),

    # Fixed Distribution
    (store_dirs_dist, gains_dist, "OT1", "purple", '^', users_dist)
]

plot_gain_vs_aaoi_multi_comparison(methods_data, output_file="comparison_gain_vs_aaoi.pdf")