import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- Robust helpers ----------

def safe_mean(arr, axis=None):
    arr = np.asarray(arr)
    if arr.size == 0:
        return np.nan
    good = np.isfinite(arr)
    if not np.any(good):
        return np.nan
    return np.nanmean(arr, axis=axis)

def load_final_aaoi_one_folder(folder, final_only=True):
    """
    Returns a single scalar AAoI from folder.
    Tries AOI_test_iter.npy: shape [tests, iterations, users].
    If not found, returns NaN.
    """
    f = os.path.join(folder, "AOI_test_iter.npy")
    if not os.path.isfile(f):
        return np.nan
    A = np.load(f)
    A = np.asarray(A)
    # Expected [tests, iterations, users]
    if A.ndim == 3:
        if final_only:
            # last test, last iteration → mean over users
            return safe_mean(A[-1, -1, :])
        else:
            return safe_mean(A)
    elif A.ndim == 2:
        # [iterations, users]
        return safe_mean(A[-1, :]) if final_only else safe_mean(A)
    else:
        return safe_mean(A)

def load_battery_mean_one_folder(folder, final_only=True):
    """
    Returns a single scalar Battery mean from folder.
    Priority: Battery_mean.npy → BT_user_tests.npy.
    Converts nothing here (raw units). Use converter in the plotting function.
    """
    f1 = os.path.join(folder, "Battery_mean.npy")
    if os.path.isfile(f1):
        bm = np.load(f1)
        bm = np.asarray(bm)
        if bm.ndim == 0:
            return float(bm)
        if final_only:
            if bm.ndim == 1:    # [iterations]
                return safe_mean(bm[-1])
            elif bm.ndim == 2:  # [tests, iterations]
                return safe_mean(bm[-1, -1])
            else:
                return safe_mean(bm)
        else:
            return safe_mean(bm)

    f2 = os.path.join(folder, "BT_user_tests.npy")
    if os.path.isfile(f2):
        bt = np.load(f2)
        bt = np.asarray(bt)   # expected [tests, iterations, users]
        if bt.ndim == 3:
            return safe_mean(bt[-1, -1, :]) if final_only else safe_mean(bt)
        elif bt.ndim == 2:
            return safe_mean(bt[-1, :]) if final_only else safe_mean(bt)
        else:
            return safe_mean(bt)

    return np.nan

# ---------- Point builders (two modes) ----------

def compute_aaoi_points(pl_vals, rows=None, folders_by_pl=None):
    """
    Returns (pls, aaoi_mean, aaoi_std).
    - rows mode: rows=[(pl, folder, aoi_value, batt_value), ...]  (uses aoi_value)
    - folder mode: folders_by_pl={pl: [folder1, folder2, ...]}  (loads from disk)
    """
    AAoI_mean, AAoI_std = [], []

    for pl in pl_vals:
        if rows is not None:
            a = np.array([aoi for p, _, aoi, _ in rows if p == pl], dtype=float)
        else:
            # load from folders
            folders = folders_by_pl.get(pl, []) if folders_by_pl else []
            a = np.array([load_final_aaoi_one_folder(fd, final_only=True) for fd in folders], dtype=float)

        AAoI_mean.append(np.nanmean(a) if a.size else np.nan)
        AAoI_std.append(np.nanstd(a) if a.size else np.nan)

    return np.array(pl_vals), np.array(AAoI_mean), np.array(AAoI_std)

def compute_battery_points(pl_vals, rows=None, folders_by_pl=None, mu=0.005):
    """
    Returns (pls, batt_mean_J, batt_std_J).
    Converts raw battery units → Joules by multiplying with mu.
    - rows mode: uses batt_value from rows (assumed raw units)
    - folder mode: loads from disk per folder
    """
    Batt_mean, Batt_std = [], []

    for pl in pl_vals:
        if rows is not None:
            b_raw = np.array([bt for p, _, _, bt in rows if p == pl], dtype=float)
        else:
            folders = folders_by_pl.get(pl, []) if folders_by_pl else []
            b_raw = np.array([load_battery_mean_one_folder(fd, final_only=True) for fd in folders], dtype=float)

        bJ = b_raw * mu  # convert to Joules
        Batt_mean.append(np.nanmean(bJ) if bJ.size else np.nan)
        Batt_std.append(np.nanstd(bJ) if bJ.size else np.nan)

    return np.array(pl_vals), np.array(Batt_mean), np.array(Batt_std)

# ---------- Plotter (dual y-axis) ----------

def plot_aaoi_and_battery_dual_axis(pls, aaoi_m, aaoi_s, batt_mJ, batt_sJ, out_pdf="IL_PDNOMA_AAOI_Battery_vs_PL.pdf"):
    """
    Dual-axis plot: left y = Average AAoI, right y = Battery (J).
    Saves a single PDF.
    """
    fig, ax1 = plt.subplots(figsize=(7.2, 4.2), dpi=300)

    # Left axis: AAoI
    ln1 = ax1.errorbar(pls, aaoi_m, yerr=aaoi_s, fmt='o-', linewidth=2,
                       capsize=4, label="Final Avg AoI", zorder=3)
    ax1.set_xlabel("Number of Power Levels (PL)")
    ax1.set_ylabel("Final Average AoI (slots)")
    ax1.grid(True, linestyle='--', alpha=0.35)

    # Right axis: Battery (J)
    ax2 = ax1.twinx()
    ln2 = ax2.errorbar(pls, batt_mJ, yerr=batt_sJ, fmt='s--', linewidth=2,
                       capsize=4, label="Mean Battery (J)", zorder=2)
    ax2.set_ylabel("Mean Battery (Joules)")

    # Combined legend
    lines = ln1.lines + ln2.lines
    labels = [l.get_label() for l in [ln1, ln2]]
    ax1.legend(lines, labels, loc="best")

    fig.tight_layout()
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_pdf}")

# ---------- Optional: build folders_by_pl from a base directory ----------

def discover_folders_by_pl(base_dir, u=12, s=5, pl_list=(3,4,5)):
    """
    Returns dict {pl: [folders]} by globbing patterns like:
      ILPDNOMA_S_{s}_U_{u}_PL{pl}_I
    Accepts both exact name and with suffixes (e.g., _I, _I_something).
    """
    base = Path(base_dir)
    out = {}
    for pl in pl_list:
        # exact name
        p_exact = base.glob(f"ILPDNOMA_S_{s}_U_{u}_PL{pl}_I")
        # allow trailing stuff after _I (e.g., _I_v2)
        p_loose = base.glob(f"ILPDNOMA_S_{s}_U_{u}_PL{pl}_I*")
        # combine and keep only directories
        folders = [str(p) for p in list(p_exact) + list(p_loose) if p.is_dir()]
        out[pl] = sorted(set(folders))
    return out



base_dir = "/Users/muhammadtauseefmushtaq/Documents/GitHub/AOI_JAL_IL"   # parent of ILPDNOMA_S_5_U_12_PL*_I folders
pl_vals  = [2, 3, 4, 5]

folders_by_pl = discover_folders_by_pl(base_dir, u=5, s=8, pl_list=pl_vals)

pls, aaoi_m, aaoi_s = compute_aaoi_points(pl_vals, rows=None, folders_by_pl=folders_by_pl)
_,   batt_mJ, batt_sJ = compute_battery_points(pl_vals, rows=None, folders_by_pl=folders_by_pl, mu=0.005)

plot_aaoi_and_battery_dual_axis(pls, aaoi_m, aaoi_s, batt_mJ, batt_sJ,
                                out_pdf="IL_PDNOMA_AAOI_Battery_vs_PL.pdf")
