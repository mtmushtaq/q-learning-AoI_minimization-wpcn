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
    "pdf.fonttype": 42,      # embed TrueType
    "ps.fonttype": 42,       # embed TrueType for EPS
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
BASE = "./"           # path to your results
PL_LIST = [2, 3, 4, 5]
S, U = 5, 10          # system identifiers (only for title)

# ===== HELPERS =====
def find_run_dirs(base, pl):
    """Return directory matching pattern for this PL."""
    pat = os.path.join(base, f"TILPDNOMA_S_5_U_10_PL{pl}_BT0.2_T1000")
    paths = sorted(glob.glob(pat))
    return [p for p in paths if os.path.isdir(p)]

def load_final_aoi(run_dir):
    """Load AOI_test_iter.npy → mean AoI at last test/iteration (avg over users)."""
    primary = os.path.join(run_dir, "AOI_test_iter.npy")
    cand = [primary] + glob.glob(os.path.join(run_dir, "**", "AOI_test_iter.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No AOI_test_iter.npy in {run_dir}")
    aoi = np.load(cand[0])
    if aoi.ndim != 3:
        raise ValueError(f"Unexpected AOI_test_iter shape {aoi.shape} in {run_dir}")
    return float(np.mean(aoi[-1, -1, :]))  # last test, last iter, mean over users

# ===== MAIN =====
rows = []  # (PL, run_dir, final_aoi)

for pl in PL_LIST:
    runs = find_run_dirs(BASE, pl)
    if not runs:
        print(f"⚠️ No directory found for PL{pl}")
        continue
    for r in runs:
        try:
            aoi = load_final_aoi(r)
        except Exception as e:
            print(f"  ⚠️ Skip {r}: {e}")
            aoi = np.nan
        rows.append((pl, r, aoi))

if not rows:
    raise SystemExit("No data found. Check BASE path and directory names.")

# Aggregate per PL (handle multiple seeds)
pl_vals = sorted(set(pl for pl, _, _ in rows))
AAoI_mean = []
AAoI_std  = []
for pl in pl_vals:
    a = np.array([aoi for p, _, aoi in rows if p == pl], dtype=float)
    AAoI_mean.append(np.nanmean(a))
    AAoI_std.append(np.nanstd(a))

# ===== Print summary table =====
print("\n=== Final Average AoI per Power Level ===")
print(f"{'PL':>4}  {'Final_AAoI':>12}  {'n_runs':>6}")
for pl, m in zip(pl_vals, AAoI_mean):
    n = sum(1 for p, _, _ in rows if p == pl)
    print(f"{pl:>4}  {m:12.4f}  {n:6d}")

# ===== Plot: Final AAoI vs PL =====
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))
plt.errorbar(pl_vals, AAoI_mean, yerr=AAoI_std, fmt='o-', lw=1.4, ms=4.5, capsize=3)
plt.xlabel("Power Levels (PL)")
plt.ylabel("Final Average AoI")
plt.title(f"TILPDNOMA  S={S}, U={U}")
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()

# Save IEEE-style figure as high-res PNG
plt.savefig("PL_lastpoint_AAoI_IEEE.png", format="png", dpi=600, bbox_inches="tight")
plt.show()
