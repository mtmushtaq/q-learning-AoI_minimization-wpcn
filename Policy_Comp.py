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


import matplotlib.pyplot as plt
import numpy as np
import os

def plot_action_policy_from_arrays(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_folder,
    output_name="policy_comparison_generic",
    dpi=600
):
    """
    Plot action policy evolution for three methods from already loaded numpy arrays.

    Parameters:
    - AC_user_IL, AC_user_JAL, AC_user_dist: 3D numpy arrays [test, user, actions]
    - output_folder: folder to save the figure
    - output_name: base filename for the PDF
    - dpi: resolution for PDF
    """
    # Calculate sum over users => get count per action per test
    def aggregate_action_counts(array):
        return np.sum(array, axis=1)  # shape becomes [test, action]

    IL_counts = aggregate_action_counts(AC_user_IL)
    JAL_counts = aggregate_action_counts(AC_user_JAL)
    DIST_counts = aggregate_action_counts(AC_user_dist)

    num_tests = IL_counts.shape[0]
    x = np.arange(num_tests)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=dpi)

    styles = ['-', '--', '-.']
    markers = ['o', 's', '^']
    colors = ['blue', 'green', 'red']
    labels = ['IL', 'JAL', 'Dist']
    data_list = [IL_counts, JAL_counts, DIST_counts]

    for data, label, color, marker, style in zip(data_list, labels, colors, markers, styles):
        num_actions = data.shape[1]
        for act in range(num_actions):
            ax.plot(
                x, data[:, act],
                style,
                label=f"{label} – Action {act+1}",
                linewidth=2,
                color=color,
                marker=marker,
                markevery=10,
                markersize=6,
                alpha=0.8
            )

    ax.set_xticks(np.arange(0, num_tests+1, 10))
    ax.set_xlabel("Test Index", fontsize=12, fontweight='bold')
    ax.set_ylabel("Number of Users Taking Action", fontsize=12, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=9, loc='upper right', ncol=2)
    ax.set_title("Action Policy Evolution Comparison", fontsize=14, fontweight='bold')
    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)
    out_path = os.path.join(output_folder, f"{output_name}.pdf")
    plt.savefig(out_path, format="pdf", dpi=dpi, bbox_inches='tight')
    plt.show()

    return out_path



plot_action_policy_from_arrays(
    AC_user_IL,
    AC_user_JAL,
    AC_user_dist,
    output_folder="Action_Policy_Dist",
    output_name="action_policy_comp_dist"
)
