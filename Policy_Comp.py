import numpy as np
import matplotlib.pyplot as plt
import os
from data_npy_io import *

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import os

# ————————————————
# 1) absolute base dir:
# ————————————————


BASE_DIR_DIST = Path(r"E:\Dist_U100")
store_dirs_dist = ["Dist_S_200_U_100"]
full_paths_dist = [BASE_DIR_DIST / subdir for subdir in store_dirs_dist]
full_paths_dist = [str(path) for path in full_paths_dist]

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100")

store_dirs_IL = ["IL_S_200_U_100_UP_020"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_200_U_100"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

AC_user_IL = load_test_matrix_npy("AC_user_tests", full_paths_IL[0])[:100,:,:]

AC_user_JAL = load_test_matrix_npy("AC_user_tests", full_paths_JAL[0])[:100,:,:]

AC_user_dist = load_test_matrix_npy("AC_user_tests", full_paths_dist[0])[:100,:,:]


def plot_action_distribution_comparison_IL_JAL_DIST_fixed(
        AC_user_IL,
        AC_user_JAL,
        AC_user_dist,
        output_dir="plots",
        output_filename="action_policy_comparison_all.pdf"
):
    """
    Plot action distribution evolution over tests for IL, JAL, and Dist in a single plot.
    """
    num_tests = min(AC_user_IL.shape[0], AC_user_JAL.shape[0], AC_user_dist.shape[0])

    # Combine all unique actions from all sources
    all_actions = np.unique(
        np.concatenate([
            AC_user_IL[:num_tests].flatten(),
            AC_user_JAL[:num_tests].flatten(),
            AC_user_dist[:num_tests].flatten()
        ])
    )
    all_actions = np.sort(all_actions).astype(int)
    num_actions = len(all_actions)

    def compute_action_probs(matrix, label):
        probs = np.zeros((num_tests, num_actions))
        for t in range(num_tests):
            flat = matrix[t].flatten()
            for i, a in enumerate(all_actions):
                probs[t, i] = np.mean(flat == a)
        return probs

    probs_IL = compute_action_probs(AC_user_IL, "IL")
    probs_JAL = compute_action_probs(AC_user_JAL, "JAL")
    probs_dist = compute_action_probs(AC_user_dist, "Dist")

    plt.figure(figsize=(14, 7))
    markers = ['o', 's', '^', 'd', 'x', '*', '+', 'v', '<', '>']
    for i, a in enumerate(all_actions):
        m = markers[i % len(markers)]
        plt.plot(range(num_tests), probs_IL[:, i], label=f"IL Action {a}", linestyle='--', marker=m, linewidth=2)
        plt.plot(range(num_tests), probs_JAL[:, i], label=f"JAL Action {a}", linestyle=':', marker=m, linewidth=2)
        plt.plot(range(num_tests), probs_dist[:, i], label=f"Dist Action {a}", linestyle='-', marker=m, linewidth=2)

    plt.xlabel("Test Index", fontsize=13, fontweight='bold')
    plt.ylabel("Probability", fontsize=13, fontweight='bold')
    plt.title(r"Action Probability Evolution Comparison $G = 0.5$ ", fontsize=15, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize='small', ncol=2)
    plt.xticks(np.arange(0, num_tests + 1, 10))
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, output_filename)
    plt.savefig(save_path, dpi=600, format='pdf')
    plt.close()

    print(f"✅ Saved comparison plot to {save_path}")


plot_action_distribution_comparison_IL_JAL_DIST_fixed(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_dir="Policy_Comp",
    output_filename="IJD_AC_plotG05.pdf"
)

