import numpy as np
import matplotlib.pyplot as plt
from data_npy_io import *

# Fixed parameters
users = 40
slots = [20, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
gains_IL = [round(users / s, 3) for s in slots]

users_JAL = 24
slots_JAL = [12, 18, 27, 34, 48, 54, 60]
gains_JAL = [round(users_JAL / s, 3) for s in slots_JAL]

# Corresponding folders (must match slot order)
store_dirs_IL = [
    "S_20_U_40_UP_020", "S_30_U_40_UP_020", "S_35_U_40_UP_020",
    "S_40_U_40_UP_020", "S_45_U_40_UP_020", "S_50_U_40_UP_020",
    "S_60_U_40_UP_020", "S_70_U_40_UP_020", "S_80_U_40_UP_020",
    "S_90_U_40_UP_020", "S_100_U_40_UP_020"
]

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
    normalized_aaoi_IL = sorted_aaoi_IL / users
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



# Call the function
plot_gain_vs_aaoi_from_dirs(store_dirs_IL, gains_IL, label="IL", color="blue")

store_dirs_JAL = [
    "JAL_S_12_U_24", "JAL_S_18_U_24", "JAL_S_27_U_24", "JAL_S_34_U_24", "JAL_S_48_U_24", "JAL_S_54_U_24", "JAL_S_60_U_24" ]

# Call the function for JAL
plot_gain_vs_aaoi_from_dirs(store_dirs_JAL, gains_JAL, label="JAL", color="orange", output_file="JAL_gain_vs_aaoi.pdf")

plot_gain_vs_aaoi_comparison(
    store_dirs_IL, gains_IL,
    store_dirs_JAL, gains_JAL,
    output_file="IL_vs_JAL_gain_vs_aaoi.pdf"
)