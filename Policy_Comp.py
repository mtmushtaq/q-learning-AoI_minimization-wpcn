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
store_dirs_dist = ["Dist_S_133_U_100"]
full_paths_dist = [BASE_DIR_DIST / subdir for subdir in store_dirs_dist]
full_paths_dist = [str(path) for path in full_paths_dist]

BASE_DIR_IL = Path (r"E:\IL_U100")
BASE_DIR_JAL = Path(r"E:\JAL_U100")

store_dirs_IL = ["IL_S_133_U_100_UP_020"]
full_paths_IL = [BASE_DIR_IL / subdir for subdir in store_dirs_IL]
full_paths_IL = [str(path) for path in full_paths_IL]

store_dirs_JAL = ["JAL_S_133_U_100"]
full_paths_JAL = [BASE_DIR_JAL / subdir for subdir in store_dirs_JAL]
full_paths_JAL = [str(path) for path in full_paths_JAL]

AC_user_IL = load_test_matrix_npy("AC_user_tests", full_paths_IL[0])[:100,:,:]

AC_user_JAL = load_test_matrix_npy("AC_user_tests", full_paths_JAL[0])[:100,:,:]

AC_user_dist = load_test_matrix_npy("AC_user_tests", full_paths_dist[0])[:100,:,:]


def plot_action_distribution_comparison_IL_JAL_DIST_final(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_dir="plots",
    output_filename="action_policy_comparison_filtered.pdf"
):
    """
    Plot action distribution evolution over tests for IL, JAL, and Dist in a single plot.
    Filters out actions not applicable to IL/JAL (e.g., action=6 if their max is 5).
    Markers placed every 10 tests. Axis ticks bold.
    """
    num_tests = min(AC_user_IL.shape[0], AC_user_JAL.shape[0], AC_user_dist.shape[0])

    # Detect all actions actually taken (non-zero in any method)
    all_actions = np.unique(
        np.concatenate([
            AC_user_IL[:num_tests].flatten(),
            AC_user_JAL[:num_tests].flatten(),
            AC_user_dist[:num_tests].flatten()
        ])
    )
    all_actions = all_actions[all_actions >= 0]  # ensure non-negative
    all_actions = np.sort(all_actions).astype(int)
    num_actions = len(all_actions)

    def compute_action_probs(matrix):
        probs = np.zeros((num_tests, num_actions))
        for t in range(num_tests):
            flat = matrix[t].flatten()
            for i, a in enumerate(all_actions):
                probs[t, i] = np.mean(flat == a)
        return probs

    probs_IL = compute_action_probs(AC_user_IL)
    probs_JAL = compute_action_probs(AC_user_JAL)
    probs_dist = compute_action_probs(AC_user_dist)

    plt.figure(figsize=(14, 7))
    markers = ['o', 's', '^', 'd', 'x', '*', '+', 'v', '<', '>']
    test_indices = np.arange(num_tests)
    marker_indices = test_indices[::10]

    for i, a in enumerate(all_actions):
        m = markers[i % len(markers)]
        if np.any(probs_IL[:, i] > 0):
            plt.plot(test_indices, probs_IL[:, i], linestyle='--', marker=m,
                     markevery=marker_indices, linewidth=2, label=f"IL Action {a}")
        if np.any(probs_JAL[:, i] > 0):
            plt.plot(test_indices, probs_JAL[:, i], linestyle=':', marker=m,
                     markevery=marker_indices, linewidth=2, label=f"JAL Action {a}")
        plt.plot(test_indices, probs_dist[:, i], linestyle='-', marker=m,
                 markevery=marker_indices, linewidth=2, label=f"Dist Action {a}")

    plt.xlabel("Test Index", fontsize=13, fontweight='bold')
    plt.ylabel("Probability", fontsize=13, fontweight='bold')
    plt.title(r"Action Probability Evolution Comparison $G = 0.75$", fontsize=15, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize='small', ncol=2)
    plt.xticks(np.arange(0, num_tests + 1, 10), fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, output_filename)
    plt.savefig(save_path, dpi=600, format='pdf')
    plt.close()

    print(f"✅ Final plot saved (filtered IL/JAL actions) to {save_path}")


plot_action_distribution_comparison_IL_JAL_DIST_final(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_dir="Policy_Comp",
    output_filename="IJD_AC_G075.pdf"
)

