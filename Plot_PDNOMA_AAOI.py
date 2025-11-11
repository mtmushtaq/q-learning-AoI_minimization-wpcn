#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# ---- (optional) use your helpers if available) ----
try:
    from data_npy_io import load_test_matrix_npy  # your helper
except Exception:
    load_test_matrix_npy = None

# ====== CONFIG ======
# Point this to the parent folder that contains ILPDNOMA_S_5_U_12_PL*_I runs
BASE = r"./"   # e.g., r"E:\IL_PD_NOMA_Results"
S, U = 5, 10
PL_LIST = [2, 3, 4, 5]  # which power levels to pull

# ====== HELPERS ======
def find_run_dirs(base, pl):
    pat1 = os.path.join(base, f"TILPDNOMA_S_5_U_10_PL{pl}_BT0.2_T1000")
    #pat2 = os.path.join(base, f"ILPDNOMA_S_{s}_U_{u}_PL{pl}")
    paths = sorted(glob.glob(pat1)) #+ sorted(glob.glob(pat2))
    return [p for p in paths if os.path.isdir(p)]

def load_final_aoi(run_dir):
    """
    Return the last-iteration, last-test mean AoI over users.
    Expects AOI_test_iter.npy with shape (tests, iterations, users).
    """
    path = os.path.join(run_dir, "AOI_test_iter.npy")
    if load_test_matrix_npy is not None and os.path.isfile(path):
        aoi = load_test_matrix_npy("AOI_test_iter", run_dir)
    else:
        # recursive fallback
        hit = [path] + glob.glob(os.path.join(run_dir, "**", "AOI_test_iter.npy"), recursive=True)
        hit = [h for h in hit if os.path.isfile(h)]
        if not hit:
            raise FileNotFoundError(f"No AOI_test_iter.npy in {run_dir}")
        aoi = np.load(hit[0])

    if aoi.ndim != 3:
        raise ValueError(f"AOI_test_iter shape unexpected {aoi.shape} in {run_dir}")
    # last test, last iteration, mean over users
    return float(np.mean(aoi[-1, -1, :]))

def load_final_battery(run_dir):
    """
    Return a single scalar: final mean battery.
    Preference:
      1) Battery_mean.npy  -> last element
      2) BT_user_test.npy  -> last test/iteration, mean over users
      3) BT_user_tests.npy -> last test/iteration, mean over users
    """
    # 1) Battery_mean.npy (vector over iterations/tests)
    cand = [os.path.join(run_dir, "Battery_mean.npy")]
    cand += glob.glob(os.path.join(run_dir, "**", "Battery_mean.npy"), recursive=True)
    for p in cand:
        if os.path.isfile(p):
            arr = np.load(p)
            return float(arr[-1]) if arr.size else float(np.nan)

    # 2) BT_user_test.npy (tests x iterations x users) — many repos call it this
    for name in ["BT_user_test.npy", "BT_user_tests.npy"]:
        cand = [os.path.join(run_dir, name)]
        cand += glob.glob(os.path.join(run_dir, "**", name), recursive=True)
        for p in cand:
            if os.path.isfile(p):
                arr = np.load(p)
                if arr.ndim != 3:
                    # sometimes stored as (iterations, users) per single test
                    if arr.ndim == 2:
                        return float(np.mean(arr[-1, :]))
                    raise ValueError(f"{name} has unexpected shape {arr.shape} in {run_dir}")
                # last test, last iteration, mean over users
                return float(np.mean(arr[-1, -1, :]))

    raise FileNotFoundError(f"No Battery_mean.npy / BT_user_test(s).npy in {run_dir}")

import os
import numpy as np

def safe_mean(arr, axis=None):
    """Return nan if empty or all-nan; otherwise nanmean along axis."""
    arr = np.asarray(arr)
    if arr.size == 0:
        return np.nan
    good = np.isfinite(arr)
    if not np.any(good):
        return np.nan
    return np.nanmean(arr, axis=axis)

def load_battery_mean_one_folder(folder, final_only=True):
    """
    Tries to compute a single scalar 'battery mean' for a folder.
    Priority:
      1) Battery_mean.npy  (shape: [iterations] or [tests, iterations])
      2) BT_user_tests.npy (shape: [tests, iterations, users])
    final_only:
      - If True: use the last iteration (and last test if present).
      - If False: average across all available frames/tests/users.
    """
    # 1) Battery_mean.npy
    f1 = os.path.join(folder, "Battery_mean.npy")
    if os.path.isfile(f1):
        bm = np.load(f1)
        bm = np.asarray(bm)
        if bm.ndim == 0:
            return float(bm)
        if final_only:
            # last iteration; if 2-D take last test, last iter
            if bm.ndim == 1:
                return safe_mean(bm[-1])
            elif bm.ndim == 2:
                return safe_mean(bm[-1, -1])
            else:
                # unexpected rank; just nanmean everything
                return safe_mean(bm)
        else:
            return safe_mean(bm)

    # 2) BT_user_tests.npy
    f2 = os.path.join(folder, "BT_user_tests.npy")
    if os.path.isfile(f2):
        bt = np.load(f2)
        bt = np.asarray(bt)  # expected [tests, iterations, users]
        if bt.ndim == 3:
            if final_only:
                # last test, last iteration, average across users
                return safe_mean(bt[-1, -1, :])
            else:
                # average across all tests/iterations/users
                return safe_mean(bt)
        elif bt.ndim == 2:
            # [iterations, users] (less common)
            return safe_mean(bt[-1, :]) if final_only else safe_mean(bt)
        else:
            return safe_mean(bt)

    # Neither file exists → return NaN (so your plot still runs)
    return np.nan

# ====== MAIN ======
rows = []  # (PL, run_dir, final_aoi, final_batt)

for pl in PL_LIST:
    runs = find_run_dirs(BASE, pl)
    if not runs:
        print(f"⚠️ No directories found for PL{pl}")
        continue
    for r in runs:
        try:
            aoi = load_final_aoi(r)
        except Exception as e:
            print(f"  ⚠️ AOI skip {r}: {e}")
            aoi = np.nan
        try:
            batt = load_final_battery(r)
        except Exception as e:
            print(f"  ⚠️ Battery skip {r}: {e}")
            batt = np.nan
        rows.append((pl, r, aoi, batt))

if not rows:
    raise SystemExit("No data found. Check BASE path and file names.")

# Aggregate per PL (mean over multiple seeds/runs), keep std for error bars
pl_vals = sorted(set([pl for pl, _, _, _ in rows]))
AAoI_mean = []
AAoI_std  = []
Batt_mean = []
Batt_std  = []
for pl in pl_vals:
    a = np.array([aoi for p, _, aoi, _ in rows if p == pl], dtype=float)
    b = np.array([bt  for p, _, _, bt  in rows if p == pl], dtype=float)
    AAoI_mean.append(np.nanmean(a))
    AAoI_std.append(np.nanstd(a))
    m = load_battery_mean_one_folder(b, final_only=True)  # or False if you prefer overall mean
    Batt_mean.append(m)
    Batt_std.append(np.nanstd(b))

# Pretty print table
print("\n=== Final point (last test/last iteration) per Power Level ===")
print(f"{'PL':>4}  {'Final_AAoI':>12}  {'Mean_Battery':>13}  {'n_runs':>6}")
for pl, mA, mB in zip(pl_vals, AAoI_mean, Batt_mean):
    n = sum(1 for p, _, _, _ in rows if p == pl)
    print(f"{pl:>4}  {mA:12.4f}  {mB:13.4f}  {n:6d}")

# ========== PLOTS ==========
# (1) AAoI vs PL
plt.figure(figsize=(6.0, 4.0))
plt.errorbar(pl_vals, AAoI_mean, yerr=AAoI_std, fmt='o-', lw=2, ms=8, capsize=5)
plt.xlabel("Power Levels (PL)")
plt.ylabel("Final Average AoI (last test/iteration)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("PL_lastpoint_AAoI22.pdf", format="pdf", bbox_inches="tight")
plt.show()

# (2) Battery vs PL

plt.figure(figsize=(6.0, 4.0))
plt.errorbar(pl_vals, Batt_mean, yerr=Batt_std, fmt='s--', lw=2, ms=8, capsize=5)
plt.xlabel("Power Levels (PL)")
plt.ylabel("Mean Battery (final step)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("PL_lastpoint_Battery.pdf", format="pdf", bbox_inches="tight")
plt.show()
