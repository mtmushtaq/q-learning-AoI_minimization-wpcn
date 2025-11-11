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
BASE     = "./"
S        = 5
U_LIST   = [10, 12, 15]
PL_LIST  = [2, 3, 4, 5]
COLORS   = {10: "#7B1FA2", 12: "#2E7D32", 15: "#1565C0"}  # purple, green, blue

# ===== HELPERS =====
def find_run_dirs(base, pl, u):
    pat = os.path.join(base, f"TILPDNOMA_S_{S}_U_{u}_PL{pl}_BT0.2_T1000")
    paths = sorted(glob.glob(pat))
    return [p for p in paths if os.path.isdir(p)]

def load_final_aoi(run_dir):
    """Return mean AoI at last test/iteration (avg over users)."""
    cand = [os.path.join(run_dir, "AOI_test_iter.npy")]
    cand += glob.glob(os.path.join(run_dir, "**", "AOI_test_iter.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No AOI_test_iter.npy in {run_dir}")
    aoi = np.load(cand[0])
    if aoi.ndim != 3:
        raise ValueError(f"Unexpected AOI_test_iter shape {aoi.shape} in {run_dir}")
    return float(np.mean(aoi[-1, -1, :]))

# ===== MAIN =====
series = {}
for u in U_LIST:
    rows = []
    for pl in PL_LIST:
        runs = find_run_dirs(BASE, pl, u)
        if not runs:
            print(f"⚠️ No directory found for U={u}, PL{pl}")
            continue
        vals = []
        for r in runs:
            try:
                vals.append(load_final_aoi(r))
            except Exception as e:
                print(f"  ⚠️ Skip {r}: {e}")
        if vals:
            rows.append((pl, np.mean(vals)))
    if rows:
        rows = sorted(rows, key=lambda x: x[0])
        series[u] = {
            'pl_vals': [p for p, _ in rows],
            'mean':    [v for _, v in rows]
        }

if not series:
    raise SystemExit("No data found.")

# ===== Plot: simple curves (no error bars) =====
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))

for u in U_LIST:
    if u not in series:
        continue
    data = series[u]
    color = COLORS.get(u, None)
    label = f"$M={u}$  ($G={u/S:.2f}$)"
    plt.plot(data['pl_vals'], data['mean'], 'o-', lw=1.4, ms=4.5, color=color, label=label)

plt.xlabel(r"Power Level ($k$)")
plt.ylabel(r"Average AoI ($\bar{A}$)")
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("AAoI_vs_PL_U10_U12_U15.png", format="png", dpi=600, bbox_inches="tight")
plt.show()
