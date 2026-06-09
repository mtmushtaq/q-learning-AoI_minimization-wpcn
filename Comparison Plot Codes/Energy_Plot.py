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
BASE     = "./"
S, U     = 5, 15
PL_LIST  = [2, 3, 4, 5]
# bright distinct colors
PL_COL   = {2: "#1565C0", 3: "#2E7D32", 4: "#EF6C00", 5: "#7B1FA2"}

# ===== HELPERS =====
def find_run_dirs(base, pl):
    pat = os.path.join(base, f"TILPDNOMA_S_{S}_U_{U}_PL{pl}_BT0.2_T1000")
    paths = sorted(glob.glob(pat))
    return [p for p in paths if os.path.isdir(p)]

def load_energy_array(run_dir):
    """
    Load Total_energy_tests.npy (robust to common shapes):
      [tests, episodes, users] -> return as is
      [episodes, users]        -> add a fake tests axis
      [episodes]               -> add tests and users axes
    """
    primary = os.path.join(run_dir, "Total_energy_tests.npy")
    cand = [primary] + glob.glob(os.path.join(run_dir, "**", "Total_energy_tests.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No Total_energy_tests.npy in {run_dir}")
    arr = np.load(cand[0])

    arr = np.asarray(arr, dtype=float)
    if arr.ndim == 3:
        # [tests, episodes, users]
        return arr
    elif arr.ndim == 2:
        # [episodes, users] -> add tests axis of length 1
        return arr[None, :, :]
    elif arr.ndim == 1:
        # [episodes] -> add tests and users axes of length 1
        return arr[None, :, None]
    else:
        raise ValueError(f"Unexpected energy array shape {arr.shape} in {run_dir}")

def episode_mean_over_users_and_tests(ener3):
    """
    ener3: [tests, episodes, users]
    Return 1D series per episode: mean over tests and users.
    """
    return np.nanmean(np.nanmean(ener3, axis=0), axis=1)  # (episodes,)

def final_mean_energy(ener3):
    """
    ener3: [tests, episodes, users]
    Return scalar: mean energy at *last episode* averaged over tests and users.
    """
    return float(np.nanmean(ener3[:, -1, :]))

def centered_moving_avg(x, win=5):
    if win <= 1 or len(x) == 0:
        return x
    # simple centered with reflection padding at ends for stability
    import numpy as _np
    pad = win // 2
    xp = _np.pad(_np.asarray(x, dtype=float), (pad, pad), mode="edge")
    c = _np.cumsum(_np.insert(xp, 0, 0.0))
    ma = (c[win:] - c[:-win]) / float(win)
    return ma

# ===== LOAD & AGGREGATE =====
per_pl_series = {}  # pl -> 1D array (episodes) averaged over runs
per_pl_final  = {}  # pl -> scalar final mean energy (averaged over runs)

for pl in PL_LIST:
    runs = find_run_dirs(BASE, pl)
    if not runs:
        print(f"⚠️ No directory found for PL{pl}")
        continue

    ep_series_list = []
    finals_list    = []

    for r in runs:
        try:
            ener3 = load_energy_array(r)              # [tests, episodes, users]
            ep_s  = episode_mean_over_users_and_tests(ener3)  # (episodes,)
            fin   = final_mean_energy(ener3)          # scalar
            ep_series_list.append(ep_s)
            finals_list.append(fin)
        except Exception as e:
            print(f"  ⚠️ Skip {r}: {e}")

    if not ep_series_list:
        continue

    # Align episode lengths across runs (truncate to min length)
    Lmin = min(len(s) for s in ep_series_list)
    ep_series_list = [s[:Lmin] for s in ep_series_list]
    # Mean across runs
    per_pl_series[pl] = np.nanmean(np.vstack(ep_series_list), axis=0)
    per_pl_final[pl]  = float(np.nanmean(np.asarray(finals_list, dtype=float)))

if not per_pl_series:
    raise SystemExit("No energy data found. Check BASE path and file names.")

# ===== 1) Plot: Convergence trend (per-episode mean energy) =====
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))
for pl in sorted(per_pl_series.keys()):
    raw = per_pl_series[pl]
    sma = centered_moving_avg(raw, win=max(5, len(raw)//40))  # gentle smoothing
    color = PL_COL.get(pl, None)
    # faded raw + solid smoothed
    plt.plot(raw, alpha=0.35, linewidth=1.0, color=color)
    plt.plot(sma, linewidth=1.6, color=color, label=f"$k$ = {pl}")

plt.xlabel(r"Frames ($I$)")
plt.ylabel(r"Energy Consumption (Joule)")
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(frameon=False, ncol=2)
plt.tight_layout()
plt.savefig("Energy_convergence_U15_PL_2_3_4_5.png", format="png", dpi=600, bbox_inches="tight")
plt.show()

# ===== 2) Plot: Final mean energy per update (single point per PL) =====
pls_sorted  = sorted(per_pl_final.keys())
final_vals  = [per_pl_final[p] for p in pls_sorted]

plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))
plt.plot(pls_sorted, final_vals, 'o-', lw=1.4, ms=4.5, color="#37474F")
plt.xlabel(r"Power Level ($k$)")
plt.ylabel(r"Energy Consumption (Joule)")
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("Final_mean_energy_vs_PL_U15.png", format="png", dpi=600, bbox_inches="tight")
plt.show()
