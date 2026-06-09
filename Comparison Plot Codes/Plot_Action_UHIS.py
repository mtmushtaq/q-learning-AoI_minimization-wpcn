import os
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# ===== IEEE-aligned figure style =====
IEEE_WIDTH = 3.4  # inches
IEEE_HEIGHT = 2.1  # inches
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "pdf.use14corefonts": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.8,
    "axes.titlesize": 9,
    "axes.linewidth": 0.9,
    "lines.linewidth": 1.4,
    "grid.linewidth": 0.5,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

# ===== CONFIG =====
BASE = "./"
S = 5
U_LIST = [10, 12, 15]
PL_LIST = [2, 3, 4, 5]
COLORS = {10: "#7B1FA2", 12: "#2E7D32", 15: "#1565C0"}  # purple, green, blue


# ===== HELPERS =====
def find_run_dirs(base, pl, u):
    pat = os.path.join(base, f"TILPDNOMA_S_5_U_{u}_PL{pl}_BT0.2_T1000")
    paths = sorted(glob.glob(pat))
    return [p for p in paths if os.path.isdir(p)]


def load_ac_data(run_dir):
    """Return action mean from 'AC_user_mean.npy'. """
    path = os.path.join(run_dir, "AC_user_mean.npy")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No AC_user_mean.npy in {run_dir}")
    ac = np.load(path)
    return ac


# ===== MAIN =====
for u in U_LIST:
    for pl in PL_LIST:
        runs = find_run_dirs(BASE, pl, u)
        if not runs:
            print(f"⚠️ No directory found for U={u}, PL{pl}")
            continue

        plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))

        for r in runs:
            try:
                actions = load_ac_data(r)
                # Plot histogram
                plt.hist(
                    actions,
                    bins=np.arange(actions.min(), actions.max() + 1) - 0.5,
                    density=True,
                    alpha=0.7,
                    label=f"PL {pl}",
                    color=COLORS.get(u, None)
                )
            except Exception as e:
                print(f" ⚠️ Skip {r}: {e}")

        plt.xlabel("Action")
        plt.ylabel("Probability")
        plt.title(f"Action Probabilities for U={u}")
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(frameon=False)
        plt.tight_layout()
        plt.savefig(f"Action_Probabilities_U{u}_PL{pl}.png", format="png", dpi=600, bbox_inches="tight")
        plt.show()