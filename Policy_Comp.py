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


def plot_action_distribution_comparison_IL_JAL_DIST(
    AC_user_IL,
    AC_user_JAL,
    AC_user_DIST,
    output_dir="plots",
    output_filename="IL_JAL_DIST_action_prob_trend.pdf"
):
    """
    Plot IL, JAL, and DIST action distribution evolution over tests in one figure.

    AC_user_*: 3D arrays of shape [num_tests, num_users, num_slots] representing slot allocations.
    Each user’s total 1s in a test/frame is their action (replica count).
    """
    def compute_action_probabilities(AC_user, max_action=None):
        num_tests = AC_user.shape[0]
        actions_per_user = np.sum(AC_user, axis=2)  # shape: [num_tests, num_users]
        if max_action is None:
            max_action = np.max(actions_per_user)
        action_probs = np.zeros((num_tests, max_action + 1))
        for t in range(num_tests):
            for a in range(max_action + 1):
                action_probs[t, a] = np.mean(actions_per_user[t] == a)
        return action_probs

    # Compute action probabilities
    prob_IL = compute_action_probabilities(AC_user_IL)
    prob_JAL = compute_action_probabilities(AC_user_JAL)
    prob_DIST = compute_action_probabilities(AC_user_DIST)

    num_tests = prob_IL.shape[0]
    x = np.arange(num_tests)

    # Plot
    plt.figure(figsize=(12, 6), dpi=600)

    for a in range(prob_IL.shape[1]):
        if np.any(prob_IL[:, a]):
            plt.plot(x, prob_IL[:, a], linestyle='--', linewidth=2,
                     marker='o', markevery=10, label=f'IL Action {a}')

    for a in range(prob_JAL.shape[1]):
        if np.any(prob_JAL[:, a]):
            plt.plot(x, prob_JAL[:, a], linestyle=':', linewidth=2,
                     marker='s', markevery=10, label=f'JAL Action {a}')

    for a in range(prob_DIST.shape[1]):
        if np.any(prob_DIST[:, a]):
            plt.plot(x, prob_DIST[:, a], linestyle='-', linewidth=2,
                     marker='^', markevery=10, label=f'Dist Action {a}')

    plt.xlabel("Test Index", fontsize=12, fontweight='bold')
    plt.ylabel("Probability", fontsize=12, fontweight='bold')
    plt.title("Action Probability Evolution Comparison", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(np.arange(0, num_tests + 1, 10), fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(fontsize=9, ncol=3)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, output_filename)
    plt.savefig(out_path, format='pdf', dpi=600)
    plt.close()

    return out_path


plot_action_distribution_comparison_IL_JAL_DIST(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_dir="Policy_Comp",
    output_filename="comp_J_I_d.pdf"
)

