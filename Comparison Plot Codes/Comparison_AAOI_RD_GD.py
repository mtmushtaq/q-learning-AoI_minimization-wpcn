#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# ===== IEEE-aligned figure style =====
IEEE_WIDTH  = 3.4   # inches
IEEE_HEIGHT = 2.1   # inches
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
BASE   = "./"
N      = 5        # slots
M      = 10       # users
PLS    = [2, 3, 4, 5]

PAT_PROPOSED = "TILPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T1000"
PAT_RANDOM   = "RNDPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T100"
PAT_GREEDY   = "GRDPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T100"

# Colors
CLR_IL  = "#7B1FA2"  # purple
CLR_RND = "#616161"  # dark gray
CLR_GRD = "#EF6C00"  # orange

# ===== HELPERS =====
def find_dirs(base, pattern):
    paths = sorted(glob.glob(os.path.join(base, pattern)))
    return [p for p in paths if os.path.isdir(p)]

def load_final_aoi(run_dir):
    cand = [os.path.join(run_dir, "AOI_test_iter.npy")]
    cand += glob.glob(os.path.join(run_dir, "**", "AOI_test_iter.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No AOI_test_iter.npy in {run_dir}")
    aoi = np.load(cand[0])
    if aoi.ndim != 3:
        raise ValueError(f"Unexpected AOI_test_iter shape {aoi.shape} in {run_dir}")
    return float(np.mean(aoi[-1, -1, :]))

def series_for_method(base, pat_template, pls):
    pl_vals, mean_vals = [], []
    for pl in pls:
        pat = pat_template.format(N=N, M=M, pl=pl)
        dirs = find_dirs(base, pat)
        if not dirs:
            print(f"⚠️  No runs for pattern: {pat}")
            continue
        vals = []
        for d in dirs:
            try:
                vals.append(load_final_aoi(d))
            except Exception as e:
                print(f"  ⚠️  Skip {d}: {e}")
        if vals:
            pl_vals.append(pl)
            mean_vals.append(float(np.mean(vals)))
    idx = np.argsort(pl_vals)
    return list(np.array(pl_vals)[idx]), list(np.array(mean_vals)[idx])

# ===== BUILD SERIES =====
pl_il,  a_il  = series_for_method(BASE, PAT_PROPOSED, PLS)
pl_rnd, a_rnd = series_for_method(BASE, PAT_RANDOM,   PLS)
pl_grd, a_grd = series_for_method(BASE, PAT_GREEDY,   PLS)

if not (pl_il or pl_rnd or pl_grd):
    raise SystemExit("No data found for IL/RND/GRD. Check BASE and folder names.")

# ===== PLOT =====
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))

if pl_il:
    plt.plot(pl_il,  a_il,  'o-', lw=1.4, ms=4.5, color=CLR_IL,  label="Proposed IL")
if pl_rnd:
    plt.plot(pl_rnd, a_rnd, 's--', lw=1.4, ms=4.5, color=CLR_RND, label="Random")
if pl_grd:
    plt.plot(pl_grd, a_grd, 'd-.', lw=1.4, ms=4.5, color=CLR_GRD, label="Greedy")

plt.xlabel(r"Power Level ($k$)")
plt.ylabel(r"Average AoI ($\bar{A}$)")

# X-axis ticks fixed to 2, 3, 4, 5 only
plt.xticks([2, 3, 4, 5])

plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(frameon=False, title=fr"$M={M}$, $N={N}$")
plt.tight_layout()

plt.savefig("AAoI_vs_PL_IL_RND_GRD_M10_N5.png",
            format="png", dpi=600, bbox_inches="tight")
plt.show()
