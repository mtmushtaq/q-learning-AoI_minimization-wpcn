import numpy as np
import matplotlib.pyplot as plt
import os
from data_npy_io import *

from pathlib import Path

# ————————————————
# 1) absolute base dir:
# ————————————————
BASE_DIR = Path(
    r"C:\Users\Tauseef\OneDrive - Politecnico di Bari"
    r"\AOI Q learning Paper\Data 10 June"
)
if not BASE_DIR.exists():
    raise FileNotFoundError(f"{BASE_DIR!r} does not exist")
# ——————————————————————————————————
# 2) construct the per‐experiment subfolder
# ——————————————————————————————————
slots_05 = 200
users = 100

subfolder_05 = f"IL_S_{slots_05}_U_{users}_UP_020"
Out_dir_05 = BASE_DIR / subfolder_05

# (optional) if your load_… functions expect a str rather than a Path
Out_dir_05 = str(Out_dir_05)

slots_062 = 160
subfolder_062 = f"IL_S_{slots_062}_U_{users}_UP_020"
Out_dir_062 = BASE_DIR / subfolder_062
Out_dir_062 = str(Out_dir_062)
#Out_dir_05 = "JAL_S_40_U_40_UP2"
#Out_dir_IL = "S_40_U_40_BT_003"


AC_user_05 = load_test_matrix_npy("AC_user_tests", Out_dir_05)[:200,:,:]


AC_user_062 = load_test_matrix_npy("AC_user_tests", Out_dir_062)[:200,:,:]


import numpy as np
import matplotlib.pyplot as plt
import os

def plot_action_distribution_comparison_over_tests(
    AC_user_tests_05,
    AC_user_tests_062,
    num_actions=6,
    output_dir="plots",
    output_filename="IL_vs_JAL_action_prob_trend.pdf"
):
    """
    Plot IL and JAL action distribution evolution over tests side-by-side
    (dotted lines + reduced x-ticks for clean scientific figure).
    """

    # Compute action probability evolution for IL
    num_tests_IL = AC_user_tests_05.shape[0]
    action_probs_IL = np.zeros((num_tests_IL, num_actions))

    for t in range(num_tests_IL):
        actions_flat = AC_user_tests_05[t].flatten()
        for a in range(num_actions):
            action_probs_IL[t, a] = np.mean(actions_flat == a)

    # Compute action probability evolution for JAL
    num_tests_JAL = AC_user_tests_062.shape[0]
    action_probs_JAL = np.zeros((num_tests_JAL, num_actions))

    for t in range(num_tests_JAL):
        actions_flat = AC_user_tests_062[t].flatten()
        for a in range(num_actions):
            action_probs_JAL[t, a] = np.mean(actions_flat == a)

    # Plot side-by-side
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    for a in range(num_actions):
        axs[0].plot(range(num_tests_IL), action_probs_IL[:, a],
                    marker='o', markersize=3, linestyle=':', linewidth=1.5, label=f"Action {a}")
    axs[0].set_title("Action Probability Evolution M= 100, N = 200", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Test Index", fontsize=12, fontweight='bold')
    axs[0].set_ylabel("Probability", fontsize=12, fontweight='bold')
    axs[0].grid(True, linestyle='--', alpha=0.5)
    axs[0].legend(fontsize='small')
    axs[0].set_xticks(np.arange(0, num_tests_IL, 10))

    for a in range(num_actions):
        axs[1].plot(range(num_tests_JAL), action_probs_JAL[:, a],
                    marker='o', markersize=3, linestyle=':', linewidth=1.5, label=f"Action {a}")
    axs[1].set_title("Action Probability Evolution M = 100, N = 160", fontsize=14, fontweight='bold')
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
    AC_user_05,
    AC_user_062,
    num_actions=6,
    output_dir="Policy_evo_IL_G05_062",
    output_filename="IL_action_trend_G05_062.pdf"
)
