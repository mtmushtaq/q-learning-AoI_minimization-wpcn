import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

# -----------------------------
# Robust helpers
# -----------------------------
def safe_mean(x):
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return np.nan
    good = np.isfinite(x)
    return np.nanmean(x[good]) if np.any(good) else np.nan

def load_final_aaoi_one_folder(folder: str) -> float:
    """
    Loads final AAoI from a results folder.
    Prefers: AOI_test_iter.npy with shape [tests, iterations, users].
    Returns mean across users at the last [test, iteration].
    """
    f = Path(folder) / "AOI_test_iter.npy"
    if not f.is_file():
        return np.nan
    A = np.load(f)
    A = np.asarray(A)
    if A.ndim == 3:         # [tests, iterations, users]
        return safe_mean(A[-1, -1, :])
    elif A.ndim == 2:       # [iterations, users] (fallback)
        return safe_mean(A[-1, :])
    else:                   # any other shape → global mean
        return safe_mean(A)

def discover_folders_by_pl(base_dir: str, S: int, U: int, pl_list: List[int]) -> Dict[int, List[str]]:
    """
    Finds result folders for each PL using patterns:
      ILPDNOMA_S_{S}_U_{U}_PL{pl}_I  and ILPDNOMA_S_{S}_U_{U}_PL{pl}_I*
    Returns {pl: [folder paths]}.
    """
    base = Path(base_dir)
    out: Dict[int, List[str]] = {}
    for pl in pl_list:
        exact = list(base.glob(f"ILPDNOMA_S_{S}_U_{U}_PL{pl}_I"))
        loose = list(base.glob(f"ILPDNOMA_S_{S}_U_{U}_PL{pl}_I*"))
        # keep only directories, unique, sorted
        all_dirs = sorted({str(p) for p in exact + loose if p.is_dir()})
        out[pl] = all_dirs
    return out

def compute_aaoi_points_from_folders(folders_by_pl: Dict[int, List[str]]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    For each PL, load AAoI from all matching folders and compute mean/std.
    Returns (pls_sorted, aaoi_mean, aaoi_std).
    """
    pls = sorted(folders_by_pl.keys())
    aaoi_mean, aaoi_std = [], []
    for pl in pls:
        vals = [load_final_aaoi_one_folder(fd) for fd in folders_by_pl[pl]]
        vals = np.asarray(vals, dtype=float)
        aaoi_mean.append(safe_mean(vals))
        aaoi_std.append(np.nanstd(vals[np.isfinite(vals)]) if np.any(np.isfinite(vals)) else np.nan)
    return np.array(pls), np.array(aaoi_mean), np.array(aaoi_std)

# -----------------------------
# Plot: AAoI vs PL for two gains
# -----------------------------
def plot_aaoi_two_gains(
    base_dir: str,
    pl_list=(3,4,5),
    caseA=(8,5),  # (S, U)
    caseB=(8,6),  # (S, U)
    out_pdf="IL_AAoI_vs_PL_two_gains.pdf"
):
    """
    Draws Final Average AoI vs PL for two (S,U) cases on one figure.
    caseA, caseB are tuples (S, U).
    """
    S1, U1 = caseA
    S2, U2 = caseB

    # Discover folders and compute AAoI points
    folders_A = discover_folders_by_pl(base_dir, S=S1, U=U1, pl_list=pl_list)
    folders_B = discover_folders_by_pl(base_dir, S=S2, U=U2, pl_list=pl_list)

    pls_A, aaoi_m_A, aaoi_s_A = compute_aaoi_points_from_folders(folders_A)
    pls_B, aaoi_m_B, aaoi_s_B = compute_aaoi_points_from_folders(folders_B)

    gainA = U1 / S1
    gainB = U2 / S2

    # Plot
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)

    # Case A
    ax.errorbar(pls_A, aaoi_m_A, yerr=aaoi_s_A, fmt='o-', linewidth=2, capsize=4,
                label=f"U={U1}, S={S1} (G={gainA:.3f})")
    # Case B
    ax.errorbar(pls_B, aaoi_m_B, yerr=aaoi_s_B, fmt='s--', linewidth=2, capsize=4,
                label=f"U={U2}, S={S2} (G={gainB:.3f})")

    ax.set_xlabel("Number of Power Levels (PL)")
    ax.set_ylabel("Final Average AoI (slots)")
    ax.set_title("Final Average AoI vs Power Levels (IL, two gains)")
    ax.grid(True, linestyle='--', alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_pdf}")

# -----------------------------
# Example call
# -----------------------------
base_dir = "/Users/muhammadtauseefmushtaq/Documents/GitHub/AOI_JAL_IL/PD_NOMA_PL"   # contains ILPDNOMA_S_8_U_5_PL*_I* etc.
plot_aaoi_two_gains(base_dir, pl_list=[2,3,4,5], caseA=(8,5), caseB=(8,6),
                     out_pdf="IL_AAoI_vs_PL_U5vsU6_S8_G2.pdf")
