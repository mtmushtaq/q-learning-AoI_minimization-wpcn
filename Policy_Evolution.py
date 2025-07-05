import numpy as np
import matplotlib.pyplot as plt
import os
from data_npy_io import *

from pathlib import Path



BASE_DIR_DIST = Path(r"E:\Dist_U100")
store_dirs_dist = ["Dist_S_200_U_100"]
full_paths_dist = [BASE_DIR_DIST / subdir for subdir in store_dirs_dist]
full_paths_dist = [str(path) for path in full_paths_dist]

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100c")

store_dirs_IL = ["IL_S_250_U_100_c"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_250_U_100_c"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

path_IL = "IL_S_250_U_100"
path_JAL = "JAL_S_250_U_100_2"

AC_user_IL = load_test_matrix_npy("AC_user_tests", full_paths_IL[0])[:200,:,:]

AC_user_JAL = load_test_matrix_npy("AC_user_tests", full_paths_JAL[0])[:200,:,:]

AC_user_dist = load_test_matrix_npy("AC_user_tests", full_paths_dist[0])[:100,:,:]


import numpy as np
import matplotlib.pyplot as plt
import os

def plot_action_distribution_comparison_over_tests(
    AC_user_tests_IL,
    AC_user_tests_JAL,
    num_actions=6,
    output_dir="plots",
    output_filename="IL_vs_JAL_action_prob_trend.pdf"
):
    """
    Plot IL and JAL action distribution evolution over tests side-by-side
    (dotted lines + reduced x-ticks for clean scientific figure).
    """

    # Compute action probability evolution for IL
    num_tests_IL = AC_user_tests_IL.shape[0]
    action_probs_IL = np.zeros((num_tests_IL, num_actions))

    for t in range(num_tests_IL):
        actions_flat = AC_user_tests_IL[t].flatten()
        for a in range(num_actions):
            action_probs_IL[t, a] = np.mean(actions_flat == a)

    # Compute action probability evolution for JAL
    num_tests_JAL = AC_user_tests_JAL.shape[0]
    action_probs_JAL = np.zeros((num_tests_JAL, num_actions))

    for t in range(num_tests_JAL):
        actions_flat = AC_user_tests_JAL[t].flatten()
        for a in range(num_actions):
            action_probs_JAL[t, a] = np.mean(actions_flat == a)

    # Plot side-by-side
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    for a in range(num_actions):
        axs[0].plot(range(num_tests_IL), action_probs_IL[:, a],
                    marker='o', markersize=3, linestyle=':', linewidth=1.5, label=f"Action {a}")
    axs[0].set_title("IL Action Probability Evolution", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Test Index", fontsize=12, fontweight='bold')
    axs[0].set_ylabel("Probability", fontsize=12, fontweight='bold')
    axs[0].grid(True, linestyle='--', alpha=0.5)
    axs[0].legend(fontsize='small')
    axs[0].set_xticks(np.arange(0, num_tests_IL, 10))

    for a in range(num_actions):
        axs[1].plot(range(num_tests_JAL), action_probs_JAL[:, a],
                    marker='o', markersize=3, linestyle=':', linewidth=1.5, label=f"Action {a}")
    axs[1].set_title("JAL Action Probability Evolution", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Test Index", fontsize=12, fontweight='bold')
    axs[1].set_ylabel("Probability", fontsize=12, fontweight='bold')
    axs[1].grid(True, linestyle='--', alpha=0.5)
    axs[1].legend(fontsize='small')
    axs[1].set_xticks(np.arange(0, num_tests_JAL, 10))

    # Save high-res PDF
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    plt.savefig(full_path, format='pdf', dpi=600, bbox_inches='tight')
    plt.close()
    print(f"✅ High-res PDF saved: {full_path}")






plot_action_distribution_comparison_over_tests(
    AC_user_IL,
    AC_user_JAL,
    num_actions=6,
    output_dir="Policy_evo_U100",
    output_filename="IL_vs_JAL_action_prob_trendg0.4.pdf"
)
