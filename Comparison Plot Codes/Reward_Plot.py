#!/usr/bin/env python3
import os, glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# ── IEEE figure settings ─────────────────────────────────────────────────────
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

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE        = "./"
PL_LIST     = [2, 3, 4, 5]
PNG_OUT     = "PL_rewards_episodewise_IEEE.png"
SMOOTH_WIN  = 5         # centered moving-average window
SKIP_FIRST  = 15        # skip first N episodes/tests (e.g., burn-in)

# ── Helpers ──────────────────────────────────────────────────────────────────
def find_run_dirs(base, pl):
    pat = os.path.join(base, f"TILPDNOMA_S_5_U_10_PL{pl}_BT0.2_T1000")
    paths = sorted(glob.glob(pat))
    return [p for p in paths if os.path.isdir(p)]

def load_reward_series_episodewise(run_dir):
    """
    Load REW_user_tests.npy and return a 1D array of episode-wise avg rewards.
    Target logic (like your example):
      - If shape is [tests, iterations, users]: avg over iterations, then users -> [tests]
      - If shape is [episodes, users]: avg over users -> [episodes]
      - If shape is [tests, episodes]: avg over tests -> [episodes]
      - If shape is [episodes]: return as is
    """
    primary = os.path.join(run_dir, "REW_user_tests.npy")
    cand = [primary] + glob.glob(os.path.join(run_dir, "**", "REW_user_tests.npy"), recursive=True)
    cand = [c for c in cand if os.path.isfile(c)]
    if not cand:
        raise FileNotFoundError(f"No REW_user_tests.npy in {run_dir}")
    arr = np.load(cand[0])

    if arr.ndim == 3:
        # [tests, iterations, users] -> mean over iterations then users => [tests]
        return np.nanmean(np.nanmean(arr, axis=1), axis=1)
    elif arr.ndim == 2:
        e0, e1 = arr.shape
        # Heuristic: if users dimension is likely the smaller one, treat axis=1 as users
        # else treat axis=0 as tests. This keeps us robust across dumps.
        if e1 <= 64:            # typical users count
            return np.nanmean(arr, axis=1)     # [episodes, users] -> [episodes]
        else:
            return np.nanmean(arr, axis=0)     # [tests, episodes] -> [episodes]
    elif arr.ndim == 1:
        return arr.astype(float)
    else:
        raise ValueError(f"Unexpected reward shape {arr.shape} in {run_dir}")

def centered_moving_average(x, win):
    if win <= 1 or len(x) == 0:
        return x
    # Use pandas centered rolling to match your sample logic
    return pd.Series(x, dtype=float).rolling(window=win, min_periods=1, center=True).mean().to_numpy()

# ── Load & aggregate ─────────────────────────────────────────────────────────
series_per_pl = {}  # pl -> list of 1D arrays (one per run)
for pl in PL_LIST:
    runs = find_run_dirs(BASE, pl)
    if not runs:
        print(f"⚠️ No directory for PL{pl}")
        continue
    seqs = []
    for r in runs:
        try:
            seq = load_reward_series_episodewise(r)
            seqs.append(np.asarray(seq, dtype=float))
        except Exception as e:
            print(f"  ⚠️ Skip {r}: {e}")
    if seqs:
        # Align lengths across runs for the same PL: truncate to minimum length
        Lmin = min(len(s) for s in seqs)
        seqs = [s[:Lmin] for s in seqs]
        # Optionally skip first episodes (burn-in)
        if SKIP_FIRST > 0 and Lmin > SKIP_FIRST:
            seqs = [s[SKIP_FIRST:] for s in seqs]
        series_per_pl[pl] = seqs

if not series_per_pl:
    raise SystemExit("No reward data found. Check BASE path and file names.")

pl_vals   = sorted(series_per_pl.keys())
ep_means  = {}   # pl -> 1D array (episodes after alignment/skip)
for pl in pl_vals:
    stack = np.vstack(series_per_pl[pl])  # [runs, episodes]
    ep_means[pl] = np.nanmean(stack, axis=0)

# Determine a consistent x-axis length after alignment/skip
X = np.arange(len(next(iter(ep_means.values()))))

# ── Plot (faded raw + solid smoothed) ────────────────────────────────────────
plt.figure(figsize=(IEEE_WIDTH, IEEE_HEIGHT))
cmap = plt.get_cmap("tab10")   # bright, distinct

for i, pl in enumerate(pl_vals):
    raw = ep_means[pl]
    sma = centered_moving_average(raw, SMOOTH_WIN)
    color = cmap(i % 10)
    # Faded raw curve
    plt.plot(X, raw, color=color, alpha=0.35, linewidth=1.0)
    # Solid moving average
    plt.plot(X, sma, color=color, linewidth=1.6, label=fr"$k$ = {pl}")

plt.xlabel("Episode")
plt.ylabel("Average Reward")
#plt.title("Episode-wise Average Reward (Raw & Smoothed)")
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(ncol=2, frameon=False, handlelength=2.8)
plt.tight_layout()
plt.savefig(PNG_OUT, format="png", dpi=600, bbox_inches="tight")
plt.show()
