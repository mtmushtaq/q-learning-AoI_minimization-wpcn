#!/usr/bin/env python3
import os, glob
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
N      = 5       # slots
M      = 15      # users
PLS    = [2, 3, 4, 5]

PAT_IL  = "TILPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T1000"
PAT_RND = "RNDPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T100"
PAT_GRD = "GRDPDNOMA_S_{N}_U_{M}_PL{pl}_BT0.2_T100"

CLR_IL  = "#7B1FA2"  # purple
CLR_RND = "#616161"  # dark gray
CLR_GRD = "#EF6C00"  # orange

# ===== HELPERS =====
def find_dirs(base, pattern):
    paths = sorted(glob.glob(os.path.join(base, pattern)))
    return [p for p in paths if os.path.isdir(p)]

def load_energy_array(run_dir):
    """Load Total_energy_tests.npy and ensure shape [tests, episodes, users]."""
    cand = [os.path.join(run_dir, "Total_energy_tests.npy")]
    cand += glob.glob(os.path.join(run_dir, "**", "Total_energy_tests.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No Total_energy_tests.npy in {run_dir}")
    arr = np.load(cand[0])
    arr = np.asarray(arr, dtype=float)
    if arr.ndim == 3:
        return arr
    elif arr.ndim == 2:
        return arr[None, :, :]
    elif arr.ndim == 1:
        return arr[None, :, None]
    else:
        raise ValueError(f"Unexpected shape {arr.shape}")

def final_mean_energy(ener3):
    """Mean energy at last episode, averaged over tests & users."""
    return float(np.nanmean(ener3[:, -1, :]))

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
                vals.append(final_mean_energy(load_energy_array(d)))
            except Exception as e:
                print(f"  ⚠️  Skip {d}: {e}")
        if vals:
            pl_vals.append(pl)
            mean_vals.append(float(np.mean(vals)))
    idx = np.argsort(pl_vals)
    return list(np.array(pl_vals)[idx]), list(np.array(mean_vals)[idx])

# ===== BUILD SERIES =====
pl_il,  e_il  = series_for_method(BASE, PAT_IL,  PLS)
pl_rnd, e_rnd = series_for_method(BASE, PAT_RND, PLS)
pl_grd, e_grd = series_for_method(BASE, PAT_GRD, PLS)

if not (pl_il or pl_rnd or pl_grd):
    raise SystemExit("No energy data found for IL/RND/GRD.")

# ===== PLOT =====
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))

if pl_il:
    plt.plot(pl_il,  e_il,  'o-', lw=1.4, ms=4.5, color=CLR_IL,  label="Proposed IL")
if pl_rnd:
    plt.plot(pl_rnd, e_rnd, 's--', lw=1.4, ms=4.5, color=CLR_RND, label="Random")
if pl_grd:
    plt.plot(pl_grd, e_grd, 'd-.', lw=1.4, ms=4.5, color=CLR_GRD, label="Greedy")

plt.xlabel(r"Power Level ($k$)")
plt.ylabel(r"Energy Consumption (Joule)")

# X-axis ticks fixed only at 2, 3, 4, 5
plt.xticks([2, 3, 4, 5])

plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(frameon=False, title=fr"$M={M}$, $N={N}$")
plt.tight_layout()

plt.savefig("Energy_vs_PL_IL_RND_GRD_M15_N5.png", format="png", dpi=600, bbox_inches="tight")
plt.show()
