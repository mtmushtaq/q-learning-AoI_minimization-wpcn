import numpy as np
import matplotlib.pyplot as plt

#from Plot_AOI import users
from data_npy_io import *
from pathlib import Path

# Fixed parameters
users = 100
users_IL = 100
users_JAL = 100

slots_IL = [250, 225, 200, 166, 133, 100, 75, 62, 56, 50]
gains_IL = [round(users/ s, 3) for s in slots_IL]
store_dirs_IL = ["IL_S_250_U_100_c", "IL_S_225_U_100_c", "IL_S_200_U_100_c", "IL_S_160_U_100_c", "IL_S_133_U_100_c", "IL_S_100_U_100_c", "IL_S_75_U_100_c", "IL_S_62_U_100_c", "IL_S_56_U_100_c", "IL_S_50_U_100_c"]

# Do the same for JAL
slots_JAL = [250, 225, 200, 160, 133, 100, 75, 62, 56, 50]
gains_JAL = [round(users / s, 3) for s in slots_JAL]
store_dirs_JAL = [
    "JAL_S_250_U_100_c", "JAL_S_225_U_100_c", "JAL_S_200_U_100",
    "JAL_S_160_U_100", "JAL_S_133_U_100", "JAL_S_100_U_100",
    "JAL_S_75_U_100", "JAL_S_62_U_100", "JAL_S_56_U_100_c", "JAL_S_50_U_100_c"
]


for g, d in zip(gains_IL, store_dirs_IL):
    print(f"G = {g:.3f} → {d}")


users_dist = 100
slots_dist = [250, 225, 200, 160, 133, 100, 75, 50]
gains_dist = [round(users_dist / s, 3) for s in slots_dist]

users_rd = 100
slots_rd = [250, 225, 200, 160, 133, 100, 75, 62, 56, 50]
gains_rd = [round(users_rd / s, 3) for s in slots_rd]

BASE_DIR = Path(
    r"C:\Users\Tauseef\OneDrive - Politecnico di Bari"
    r"\AOI Q learning Paper\Data 10 June"
)

BASE_DIR_IL = Path (BASE_DIR / r"E:\IL_U100")


BASE_DIR_JAL = Path(
    r"E:\JAL_U100c"
)


BASE_DIR_RD = Path(r"C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q learning Paper\Data July\IRSA_U100")

BASE_DIR_DIST = Path(r"E:\Dist_U100")

store_dirs_dist = ["Dist_S_250_U_100", "Dist_S_225_U_100", "Dist_S_200_U_100", "Dist_S_160_U_100", "Dist_S_133_U_100", "Dist_S_100_U_100", "Dist_S_75_U_100", "Dist_S_50_U_100"]
store_dirs_rd = ["IRSA_S_250_U_100", "IRSA_S_225_U_100", "IRSA_S_200_U_100", "IRSA_S_160_U_100", "IRSA_S_133_U_100", "IRSA_S_100_U_100", "IRSA_S_75_U_100", "IRSA_S_62_U_100", "IRSA_S_56_U_100","IRSA_S_50_U_100"]

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

    plt.xlabel(r"Normalized Channel Traffic $G$", fontsize=12, fontweight='bold')
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

# Combine each directory with BASE_DIR
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

full_paths_RD = [BASE_DIR_RD / subdir for subdir in store_dirs_rd]
full_paths_RD = [str(path) for path in full_paths_RD]

full_paths_dist = [BASE_DIR_DIST / subdir for subdir in store_dirs_dist]
full_paths_dist = [str(path) for path in full_paths_dist]

methods_data = [
    # IL
    (full_paths_IL , gains_IL, "IL", "blue", 'o', users_IL),

    # JAL
    (full_paths_JAL, gains_JAL, "JAL", "darkorange", 's', users_JAL),

    # Random
    (full_paths_RD , gains_rd, "IRSA", "green", 'D', users_rd),

    # Fixed Distribution
    (full_paths_dist, gains_dist, "IRSA-EH", "purple", '^', users_dist)
]

plot_gain_vs_aaoi_multi_comparison(methods_data, output_file="gain_vs_aaoi_IRSA.pdf")



#plot_gain_vs_aaoi_from_dirs(full_paths_IL, gains_IL, label="IL", color="purple", output_file="IL_gain_vs_aaoi.pdf")
