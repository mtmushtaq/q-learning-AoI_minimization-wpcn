 #import sys
#import matplotlib
#matplotlib.use('Qt5Agg')  # Or TkAgg 'Qt5Agg', 'GTK3Agg' depending on your system
#from typing import Any
import random as rd

import matplotlib
import numpy as np
from numpy import ndarray, dtype
from scipy.signal import square
from State_User import * #generate_rician_fading, gamma_EH, compute_energy_harvested
from Discritize_state import get_dis_BT, get_dis_AT, CH_dist
from SIC import *
from User import User
from Data_IO import *
import os
import matplotlib.patches as patches
from scipy.stats import binned_statistic_2d
#import pandas as pd
from pandas import DataFrame
import scipy.interpolate

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_npy_io import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import Axes3D

# This code with an optimized Learning rate= 0.5, But we need to find the value of Epsilon for good convergence
# define training parameters
discount_factor = 0.99  # 0.001
test = 100
learning_rate = 0.0001
#define system parameters
mu_bu= 0.05 # one unit of battery
number_of_slots = 5
number_of_users = 15
time_duration = 0.01
p= 4
dist_min = 1
dist_max = 7
s_AAOI = []
Gain = []
Th= 0.2
iterations = 2500
Frame_size = []
STD_AoI_u_AT = []
STD_AoI_u_BT = []
Batch_size = 1
it_ind = 0
explore_count = []
exploit_count = []
explore = 0
exploit = 0
K_factor =  12
decay_rate = 0.005
#upsilon = 0.020 # One unit to transmit one replica
d_slot = 1
chg_slots = 80
#u = np.empty(number_of_users, dtype=object)  # define users array
#for i in range(number_of_users):
 #   u[i] = i + 1
# q_tables = np.zeros (k.size * x.size, a.size)
k = np.array([0, 1, 2, 3, 4, 5])  # possible power values
x = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # channel quality information
a = np.array([0, 1, 2, 3, 4, 5])
max_bt = 0.2
battery_bins = 10
upsilon = max_bt/battery_bins
L       = 5
Out_dir  = f"RNDPDNOMA_S_{number_of_slots}_U_{number_of_users}_PL{L}_BT{max_bt}_T{test}"
# S = ((), dtype=float)
#S = np.zeros((u.size, k.size, x.size), dtype=int)

#first Initialization of State
#battery_c = np.zeros (u.size, dtype=float)
#battery = battery_c +0.05
#D_U = np.zeros (u.size, dtype=int)

#for u_s in range(u.size):
 #   ch_user = generate_rician_fading (K_factor)
  #  gam_user = gamma_EH(ch_user, dist_min, dist_max)
   # EH_user = compute_energy_harvested(gam_user, time_duration, p)
    #CH_Raw [u_s,0]= gam_user
    #BT_Dis [u_s, 0], EH_Raw[u_s, 0] = get_dis_BT (EH_Raw[u_s,0], EH_user, mu_bu)
    #CH_Dis [u_s, 0] = CH_dist(gam_user)
# S[i][j][l] = np.random.randint(0, 2 , size=(u.size, k.size, x.size), dtype=int)
def get_row(pw, ch):
    if (pw == 0 and ch == 0):
        row = 0
        return row
    elif (pw == 0 and ch == 1):
        row = 1
        return row
    elif (pw == 0 and ch == 2):
        row = 2
        return row
    elif (pw == 0 and ch == 3):
        row = 3
        return row
    elif (pw == 0 and ch == 4):
        row = 4
        return row
    elif (pw == 0 and ch == 5):
        row = 5
        return row
    elif (pw == 0 and ch == 6):
        row = 6
        return row
    elif (pw == 0 and ch == 7):
        row = 7
        return row
    elif (pw == 1 and ch == 0):
        row = 8
        return row
    elif (pw == 1 and ch == 1):
        row = 9
        return row
    elif (pw == 1 and ch == 2):
        row = 10
        return row
    elif (pw == 1 and ch == 3):
        row = 11
        return row
    elif (pw == 1 and ch == 4):
        row = 12
        return row
    elif (pw == 1 and ch == 5):
        row = 13
        return row
    elif (pw == 1 and ch == 6):
        row = 14
        return row
    elif (pw == 1 and ch == 7):
        row = 15
        return row
    elif (pw == 2 and ch == 0):
        row = 16
        return row
    elif (pw == 2 and ch == 1):
        row = 17
        return row
    elif (pw == 2 and ch == 2):
        row = 18
        return row
    elif (pw == 2 and ch == 3):
        row = 19
        return row
    elif (pw == 2 and ch == 4):
        row = 20
        return row
    elif (pw == 2 and ch == 5):
        row = 21
        return row
    elif (pw == 2 and ch == 6):
        row = 22
        return row
    elif (pw == 2 and ch == 7):
        row = 23
        return row
    elif (pw == 3 and ch == 0):
        row = 24
        return row
    elif (pw == 3 and ch == 1):
        row = 25
        return row
    elif (pw == 3 and ch == 2):
        row = 26
        return row
    elif (pw == 3 and ch == 3):
        row = 27
        return row
    elif (pw == 3 and ch == 4):
        row = 28
        return row
    elif (pw == 3 and ch == 5):
        row = 29
        return row
    elif (pw == 3 and ch == 6):
        row = 30
        return row
    elif (pw == 3 and ch == 7):
        row = 31
        return row
    elif (pw == 4 and ch == 0):
        row = 32
        return row
    elif (pw == 4 and ch == 1):
        row = 33
        return row
    elif (pw == 4 and ch == 2):
        row = 34
        return row
    elif (pw == 4 and ch == 3):
        row = 35
        return row
    elif (pw == 4 and ch == 4):
        row = 36
        return row
    elif (pw == 4 and ch == 5):
        row = 37
        return row
    elif (pw == 4 and ch == 6):
        row = 38
        return row
    elif (pw == 4 and ch == 7):
        row = 39
        return row
    elif (pw == 5 and ch == 0):
        row = 40
        return row
    elif (pw == 5 and ch == 1):
        row = 41
        return row
    elif (pw == 5 and ch == 2):
        row = 42
        return row
    elif (pw == 5 and ch == 3):
        row = 43
        return row
    elif (pw == 5 and ch == 4):
        row = 44
        return row
    elif (pw == 5 and ch == 5):
        row = 45
        return row
    elif (pw == 5 and ch == 6):
        row = 46
        return row
    else:
        row = 47
        return row

#def get_rew(B_AOI, A_AOI, BT, act, ch):
 #   D_AOI = B_AOI - A_AOI
  #  rew = 0
   # if act == BT:
    #    rew = D_AOI + (act/(ch+0.1))
    #elif act < BT:
     #   rew = D_AOI + (2* act)
    #return rew
def get_rew(A_AOI, tot_energy):
    w1= 0.8
    w2= 0.6
    reward = - (w1*A_AOI) - (w2*tot_energy)
    #D_AOI = B_AOI - A_AOI
    #D_AOI_norm = D_AOI / number_of_slots
    #act_norm = act / 5
    #ch_norm = ch / 7.0
    #BT_norm = BT / 5
    #reward = 0
    #np.clip(D_AOI, 0, number_of_slots)
    #if act == BT and ch >= 4:
    #    reward = w1 * np.clip(D_AOI, 0, number_of_slots) + w2 * (act / (ch + 0.1)) + w3 * BT
    #else:
     #   reward = w1 * np.clip(D_AOI, 0, number_of_slots) + w2 * (2 * act) + w3 * BT
    return reward


def get_distr(pw):
    if pw == 0:
        distr = np.array([0])
        return distr
    if pw == 1:
        distr = np.array([1])
        return distr
    elif pw == 2:
        distr = np.array([0.75, 0.25])
        #distr = np.array([0.5, 0.5])
        return distr
    elif pw == 3:
        distr = np.array([0.7, 0.2, 0.1])
        #distr = np.array([0.34, 0.33, 0.33])
        return distr
    elif pw == 4:
        distr = np.array([0.625, 0.2083, 0.1042, 0.0625])
        #distr = np.array([0.25, 0.25, 0.25, 0.25])
        return distr
    elif pw == 5:
        distr = np.array([0.6, 0.2, 0.1, 0.06, 0.04])
        #distr = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        return distr

def to_scalar(x) -> float:
    """Robustly convert a numpy scalar/array/list/py-number to a Python float."""
    return float(np.asarray(x, dtype=float).reshape(-1)[0])



# ============================ PD-NOMA UPGRADE BLOCK ===========================
# --- Design / sim parameters (use your real values) --------------------------
gamma_th_db  = 2
Gamma       = 0.5 #10 ** (gamma_th_db / 10.0)        # target SINR for rate R: Gamma = 2^R - 1  (linear)
N0          = 1e-3        # noise power (linear) - match your sim units
delta_slot  = time_duration      # slot duration δ
omega_max   = 1.0          # max user battery energy (normalized to your debits)
        # number of PD-NOMA levels (a.k.a. K). 1 = highest, L = lowest

# If you still keep the old "1 unit per replica" constant, define it here for mapping:
upsilon     = 0.020        # legacy energy-per-replica used before (IRSA fixed); now only for mapping

# --- CSI reference & global repetition cap -----------------------------------
def gamma_ref_from_top_bin(csi_bin_edges: np.ndarray) -> float:
    """Use the upper edge of the top CSI bin as γ_ref (conservative, finite)."""
    return float(csi_bin_edges[-1])

def compute_l_cap(gamma_ref: float, Gamma: float, N0: float, delta_slot: float, omega_max: float) -> int:
    """
    e_min = (Gamma * N0 / gamma_ref) * delta_slot
    l_cap = floor(omega_max / e_min)
    """
    gamma_ref = max(gamma_ref, 1e-12)
    e_min = (Gamma * N0 / gamma_ref) * delta_slot
    e_min = max(e_min, 1e-18)
    l_cap = int(np.floor(omega_max / e_min))
    return max(l_cap, 0)

# Call this ONCE after your CSI bins are created (you already have csi_bin_edges):
# gamma_ref = gamma_ref_from_top_bin(csi_bin_edges)
# l_cap     = compute_l_cap(gamma_ref, Gamma, N0, delta_slot, omega_max)

# --- Received-power ladder μ_k (k=1..L, 1=highest, L=lowest) -----------------



# --- Action selection (explore/exploit) --------------------------------------
def masked_argmax(Q_slice: np.ndarray, mask: np.ndarray) -> tuple[int, int]:
    """
    Greedy selection among feasible only.
    Q_slice: (l_cap+1, L) for a given (user, state).
    """
    Qm = np.where(mask, Q_slice, -np.inf)
    a_id = int(np.nanargmax(Qm))
    l_sel, k_idx = a_id // Q_slice.shape[1], a_id % Q_slice.shape[1]
    return l_sel, k_idx


# --- Battery debit helper (keeps backward compatibility) ---------------------
def energy_to_legacy_units(energy: float, upsilon: float) -> float:
    """
    If your user.decrease_EH(x) expects 'replica units', map energy -> units.
    """
    return energy / max(upsilon, 1e-12)


# --- Q-table allocation helper -----------------------------------------------
def allocate_q_table(number_of_users: int, B: int, C: int, l_cap: int, L: int) -> np.ndarray:
    """
    Q[user, state, l, k] with l in [0..l_cap], k in [0..L-1].
    """
    S = B * C
    q_tables = np.random.uniform(low=-0.01, high=0.1, size=(number_of_users, S, l_cap + 1, L)).astype(float)
    return q_tables


# ---- PD-NOMA ladder WITHOUT N0 ----------------------------------------------
def build_mu_ladder(Gamma_i: float, L: int) -> np.ndarray:
    """
    Noise-normalized PD-NOMA ladder (N0 absorbed into units):
      μ_k = Γ * (1+Γ)^(L-k),  k = 1..L  (return array index 0..L-1).
    """
    mu = np.empty(L, dtype=float)
    for k in range(1, L+1):
        mu[k-1] = Gamma_i * ((1.0 + Gamma_i) ** (L - k))
    return mu

mu_levels = build_mu_ladder(Gamma, L)  # shape (L,)

# ---- Per-level energy & masks ------------------------------------------------
def per_level_energy(mu_levels: np.ndarray, gamma_rep: float, delta_slot: float) -> np.ndarray:
    """
    e_k = (μ_k / γ_rep) * δ, for k index 0..L-1.
    """
    g = max(float(gamma_rep), 1e-12)
    return (mu_levels / g) * float(delta_slot)

def lmax_per_level_cont(omega_continuous, e_k: np.ndarray, l_cap: int) -> np.ndarray:
    """
    Per-level max replicas using *continuous* battery (same units as e_k):
      l_max(k) = min( floor(omega / e_k[k]), l_cap )
    """
    omega = max(float(omega_continuous), 0.0)
    denom = np.maximum(e_k, 1e-15)
    raw = np.floor(omega / denom).astype(int)
    raw[raw < 0] = 0
    return np.minimum(raw, l_cap)

def build_mask(lmax_k: np.ndarray, l_cap: int) -> np.ndarray:
    """
    Returns boolean mask over (l,k) with shape (l_cap+1, L).
    mask[l,k] = True iff 0 <= l <= l_max(k).
    """
    mask = np.zeros((l_cap + 1, L), dtype=bool)
    for k in range(L):
        mask[: lmax_k[k] + 1, k] = True
    return mask

# ---- Action selection (random baseline) --------------------------------------
_RNG = np.random.default_rng()  # seed here if you want reproducibility

def random_feasible_action(mask: np.ndarray, force_tx: bool = False) -> tuple[int, int]:
    """
    Uniform random (l,k) among feasible actions.
    If force_tx=True, exclude l==0 (always transmit when feasible).
    """
    feas = np.argwhere(mask)  # rows are [l, k]
    if feas.size == 0:
        return 0, 0
    if force_tx:
        feas = feas[feas[:, 0] > 0]
        if feas.size == 0:
            return 0, 0
    l, k = feas[_RNG.integers(len(feas))]
    return int(l), int(k)

# ---- Battery debit helper (continuous-first fallback to legacy) --------------
def debit_energy(user_obj, energy: float, upsilon_legacy: float = 0.020):
    """
    Prefer a real energy-based debit if available (user.spend_energy).
    Otherwise, convert to 'replica units' and call decrease_EH_cont(int_units).
    """
    e = float(energy)
    if e <= 0:
        return
    if hasattr(user_obj, "spend_energy"):
        user_obj.spend_energy(e)
    elif hasattr(user_obj, "decrease_EH_cont"):
        units = int(np.ceil(e / max(upsilon_legacy, 1e-12)))
        user_obj.decrease_EH_cont(max(units, 0))
    else:
        # Last resort: if only 'decrease_EH' (in replica units) exists
        units = int(np.ceil(e / max(upsilon_legacy, 1e-12)))
        user_obj.decrease_EH(max(units, 0))

# ---- Global repetition cap: fixed (as requested) -----------------------------
l_cap = 10
print(f"[PD-NOMA] Using noise-normalized ladder, l_cap={l_cap}, L={L}, Gamma={Gamma}")
# ========================== END PD-NOMA UPGRADE BLOCK =========================

# ========================== END PD-NOMA UPGRADE BLOCK =========================


## Command to randomly pick values----->>>>> np.random.randint(0, 7, size=(k.size * x.size, a.size), dtype=int)
#reward = np.empty((number_of_users, iterations+1), dtype=float)
#AOI = np.zeros((number_of_users, iterations+1), dtype=int)

#discount_factor = 0.9
#learning_rate = 0.001
# step_size_ep= (1-0.4)/iterations

users = []
for i in range(number_of_users):  # popola il vettore degli utenti
    # users[i] = i + 1
    users.append(User(id=i, mu=upsilon, initial_battery_level=0.005, max_bat = max_bt))  # inizializza ogni utente con un livello di batteria di 0.005

# ---- CSI bin definition consistent with get_channel() -----------------------
# Same breakpoints as used in get_channel()
csi_bin_edges = np.array([0.0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40], dtype=float)
C = len(csi_bin_edges) - 1   # number of CSI bins = 8
print(f"[INFO] CSI bins: {C}, edges = {csi_bin_edges}")

# ---- Compute global design-time PD-NOMA parameters --------------------------
# --- once, after CSI bin edges are set ---
gamma_ref = gamma_ref_from_top_bin(csi_bin_edges)
#l_cap     = compute_l_cap(gamma_ref, Gamma, N0, delta_slot, omega_max)
# --- Global repetition cap (fixed) ---
l_cap = 10
print(f"[PD-NOMA] l_cap fixed to {l_cap}")



# Replace your old q_tables = ... line with:
q_tables = allocate_q_table(number_of_users, B=battery_bins, C=C, l_cap=l_cap, L=L)


#q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=float)
#for user in range(np.size(users)):
#    q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
#print(f"first Q Table {q_tables}")

AOI_users = np.ones((iterations*test, number_of_users), dtype=int)
AOI_users_tests = np.empty((test, iterations,number_of_users), dtype=int)
#print(q_tables)
# print(f"All State matrix {S}")
G = np.empty(test, dtype = float)


epsilon_t = np.zeros((test, iterations), dtype=np.float32)
#AOI_test_iter = np.ones((test, iterations, number_of_users), dtype=float)
AOI_test = np.ones((test, number_of_users), dtype=np.float32)

import os, gc
import numpy as np

# ensure output directory exists
os.makedirs(Out_dir, exist_ok=True)

# dimensions
num_tests = test                 # total number of tests
n_iters, n_users = iterations, number_of_users

shape2d = (num_tests, n_iters, n_users)
shape1d = (num_tests, n_iters)

# 3D on‑disk buffers for each per‑test 2D array
AOI_mm    = np.memmap(os.path.join(Out_dir, 'AOI_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
AC_mm     = np.memmap(os.path.join(Out_dir, 'AC_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
CH_mm     = np.memmap(os.path.join(Out_dir, 'CH_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
BT_mm     = np.memmap(os.path.join(Out_dir, 'BT_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
REW_mm    = np.memmap(os.path.join(Out_dir, 'REW_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
G_mm      = np.memmap(os.path.join(Out_dir, 'G_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)
CHRAW_mm  = np.memmap(os.path.join(Out_dir, 'CHRAW_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)

Total_energy_mm = np.memmap(os.path.join(Out_dir, 'total_energy_all.dat'),
                      dtype=np.float32, mode='w+', shape=shape2d)

# 2D on‑disk buffers for each per‑test mean vector
ACmean_mm  = np.memmap(os.path.join(Out_dir, 'AC_mean.dat'),
                       dtype=np.float32, mode='w+', shape=shape1d)
CHmean_mm  = np.memmap(os.path.join(Out_dir, 'CH_mean.dat'),
                       dtype=np.float32, mode='w+', shape=shape1d)
BTmean_mm  = np.memmap(os.path.join(Out_dir, 'Battery_mean.dat'),
                       dtype=np.float32, mode='w+', shape=shape1d)
REWmean_mm = np.memmap(os.path.join(Out_dir, 'Rew_u_mean.dat'),
                       dtype=np.float32, mode='w+', shape=shape1d)


#slot_aloc_test = []  # List of (users × slots) matrices
for t in range(1, test+1):
    #AC_user_Mean = np.empty((iterations), dtype=float)
    #CH_mean = np.empty((iterations), dtype=float)
    #Battery_mean = np.empty((iterations), dtype=float)
    #Rew_u_mean = np.empty((iterations), dtype=float)
    #AC_user_tests = np.empty((iterations, number_of_users), dtype=float)
    #CH_user_tests = np.empty((iterations, number_of_users), dtype=float)
    #BT_user_tests = np.empty((iterations, number_of_users), dtype=float)
    #REW_user_tests = np.empty((iterations, number_of_users), dtype=float)
    #G_user_tests = np.empty((iterations, number_of_users), dtype=float)
    #Ch_Raw_tests = np.empty((iterations, number_of_users), dtype=float)
    slot_aloc_test = np.zeros((number_of_users), dtype=np.float32)
    idle_slots = np.zeros(iterations, dtype=int)
    slot_aloc_it = np.zeros((iterations, np.size(users), number_of_slots), dtype=int)
    min_epsilon = 0.3
    max_epsilon = 0.9
    reward = np.empty((number_of_users, iterations + 1), dtype=np.float32)
    AOI = np.zeros((number_of_users, iterations + 1), dtype=int)
    AOI_af= np.ones(number_of_users, dtype=int)
    #users = []
    #for i in range(number_of_users):  # popola il vettore degli utenti
        # users[i] = i + 1
     #   users.append(User(id=i, mu=upsilon,initial_battery_level=0.05))  # inizializza ogni utente con un livello di batteria di 0.005
    Battery_f = np.empty((iterations, number_of_users), dtype=np.float32)  # To save state of all users in current frame
    Ch_f = np.empty((iterations, number_of_users), dtype=np.float32)
    AC_user_f = np.empty((iterations, number_of_users), dtype=int)
    Rew_u_f = np.empty((iterations, number_of_users), dtype=np.float32)
    G_Raw_f = np.empty((iterations, number_of_users), dtype=np.float32)
    CH_raw_f = np.empty((iterations, number_of_users), dtype=np.float32)
    Total_energy_f = np.empty((iterations, number_of_users), dtype=np.float32)
    dist = np.random.uniform(dist_min, dist_max, size= number_of_users)
    AOI_cumsum = np.zeros((number_of_users,), dtype=np.float32)
    AOI_test_iter = np.zeros((iterations, number_of_users), dtype=np.float32)
    #q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=float)
    #for user in range(np.size(users)):
     #   q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
    for it_ind in range(0, iterations):
        #print(f"Iteration: {it_ind}")
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * it_ind)
        epsilon = round(epsilon, 5)
        epsilon_t[t-1, it_ind] = epsilon
        slot_aloc_f = np.zeros ((np.size(users), number_of_slots), dtype=int)
        S = np.empty((number_of_users, 1, 2), dtype=float)  # To save state of all users in current frame
        EH_Raw = np.empty(number_of_users, dtype=float)  # to save raw battery capacity of all users at current iteration/frame
        #EH_Raw[:, 0] = EH_Raw[:, 0] + 0.05
        BT_Dis = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
        CH_Raw = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
        CH_Dis = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
        G_Raw = np.empty(number_of_users, dtype=float) # to save Gamma of current frame
        AC_users = np.empty(number_of_users, dtype=int) #to save action in current frame for reward calculation
        Rew_U = np.empty(number_of_users, dtype=float)  #
        total_energy = np.zeros(number_of_users, dtype=float)
        #Calculate the channel and update battery for current frame
        #for u in range (np.size(users)):

            #EH_Raw [u] = compute_energy_harvested(G_Raw, time_duration, p)
            #users[u] =

        # slot_aloc_f holds power level per slot; initialize outside loop:
        # slot_aloc_f = np.zeros((np.size(users), number_of_slots), dtype=int)

        # ===================== UPDATED PER-USER DECISION BLOCK ======================
        # ===================== UPDATED PER-USER DECISION BLOCK ======================
        for d in range(np.size(users)):
            # --- Sense channel & discretize state ------------------------------------
            CH_Raw[d] = generate_rician_fading(K_factor)
            users[d].channel = CH_Raw[d]
            G_Raw[d] = gamma_EH(CH_Raw[d], dist[d])  # instantaneous γ (linear)
            BT_Dis[d] = users[d].BT_units(battery_bins)  # discrete battery (for state only)
            CH_Dis[d] = get_channel(G_Raw[d])  # CSI bin index
            row_act = get_row(BT_Dis[d], CH_Dis[d])  # state index in Q (if you log it)

            # --- Build feasibility at current state (battery+CSI aware) ---------------
            gamma_rep = float(G_Raw[d])  # actual γ this frame
            e_k_now = per_level_energy(mu_levels, gamma_rep, delta_slot)  # (L,)
            omega_now = users[d].get_battery_level()  # continuous battery
            lmax_now = lmax_per_level_cont(omega_now, e_k_now, l_cap)  # (L,)
            mask_now = build_mask(lmax_now, l_cap)  # (l_cap+1, L)

            # --- RANDOM BASELINE: uniform over feasible (no epsilon/QL) ---------------
            l_sel, k_idx = (0, 0) if not mask_now.any() else random_feasible_action(mask_now, force_tx=False)

            # --- Allocate exactly l_sel slots and debit energy ------------------------
            if l_sel <= 0:
                AC_users[d] = 0
                total_energy[d] = 0.0
            else:
                l_exec = int(min(l_sel, number_of_slots))
                slot_indices = np.random.choice(np.arange(number_of_slots, dtype=int),
                                                size=l_exec, replace=False)

                power_level_to_write = k_idx + 1  # 1..L (1 = highest)
                total_energy[d] = float(l_sel) * float(e_k_now[k_idx])

                # Battery guard — DO NOT overwrite after cancel
                if users[d].get_battery_level() + 1e-12 < total_energy[d]:
                    # cancel TX: keep zeros, no debit
                    slot_aloc_f[d, slot_indices] = 0
                    AC_users[d] = 0
                    total_energy[d] = 0.0
                else:
                    # write only if feasible and energy available
                    slot_aloc_f[d, slot_indices] = power_level_to_write

                    # Prefer Joule-based debit; NEVER cast to int
                    if hasattr(users[d], "spend_energy"):
                        users[d].spend_energy(total_energy[d])  # Joules
                    else:
                        users[d].decrease_EH_cont(total_energy[d])  # keep float

                    AC_users[d] = int(l_sel)

            # Book-keeping
            AC_users[d] = int(l_sel)
        # =================== END UPDATED PER-USER DECISION BLOCK =====================

        # =================== END UPDATED PER-USER DECISION BLOCK =====================

        #use free slots for energy harvesting
        for i in range(number_of_slots):
            if np.sum(slot_aloc_f[:, i]) == 0:

                idle_slots [it_ind] += 1 #track idle slots each iteration
                # Normalize AOI to form probabilities (avoid zero-sum issue)
                #if np.sum(AOI_af) == 0:
                #    prob_aoi = np.ones(number_of_users) / number_of_users  # uniform fallback
                #else:
                #    prob_aoi = AOI_af / np.sum(AOI_af)
                #u = np.random.choice(np.arange(number_of_users), p=prob_aoi)
                #u = rd.randint(0, number_of_users - 1)
                # for u in range(number_of_users):
                #    if u == user_to_transmit:
                for u in range(np.size(users)):
                    pw_u = compute_energy_harvested(G_Raw[u], time_duration, p)
                    users[u].add_EH(pw_u)
                #BT_Dis[u] = users[u].BT_units()

        # apply SIC
        decoded_users = capture_effect_SIC_realtime_PDNOMA(slot_aloc_f, number_of_slots, number_of_users, L, verbose=False) # Rearly-n method

        #Calculate AOI
        Bf_aoi = np.ones(number_of_users, dtype=int)  # Before AOI update
        Af_aoi = np.ones(number_of_users, dtype=int)  # After AOI update
        for u in range(number_of_users):
            Bf_aoi [u] = users[u].AOI
            Recovery = decoded_users [u, 0]
            Tx_slot = decoded_users [u, 1]
            if Tx_slot == -1 or Recovery == -1:
                users[u].AOI = Bf_aoi [u] + number_of_slots
            else:
                users[u].AOI = Recovery - Tx_slot + 1 + (number_of_slots - Recovery)
            Af_aoi[u] = users[u].AOI
            Rew_U [u] = get_rew ( Af_aoi[u] , total_energy[u])
            #print(f"user {u} AOI is {users[u].AOI}")
            #print(f"user {u} BT is {users[u].battery_level}")
            #print(f"user {u} REW is {Rew_U [u]}")

        AOI_af = Af_aoi
        AOI_users [t*it_ind, :] = Af_aoi
        AOI_users_tests [t-1, it_ind, :] = Af_aoi
        #AOI_test_iter [t-1, it_ind, :] = Af_aoi
        if it_ind > 0:
            AOI_cumsum += Af_aoi  # assuming Af_aoi is the AoI at this iteration
            AOI_test_iter[it_ind, :] = AOI_cumsum / (it_ind + 1)
            #AOI_test_iter [t-1, it_ind, :] = (AOI_test_iter [t-1, it_ind-1, :] + AOI_test_iter [t-1, it_ind, :])/it_ind
        '''''''''
        if (it_ind + 1) % Batch_size == 0:
            # Get new State and update Q-Table
            dist = np.random.uniform(dist_min, dist_max, size=number_of_users)
            BT_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
            CH_Raw_next = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
            CH_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
            G_Raw_next = np.empty(number_of_users, dtype=float)  # to save Gamma of current frame
            for u in range(number_of_users):
                CH_Raw_next[u] = generate_rician_fading(K_factor)
                users[u].channel = CH_Raw_next[u]
                G_Raw_next[u] = gamma_EH(CH_Raw_next[u], dist[u]) #dist_min, dist_max)
                BT_Dis_next[u] = users[u].BT_units(battery_bins)
                CH_Dis_next[u] = get_channel(G_Raw[u])
                row_act = get_row(BT_Dis_next[u], CH_Dis_next[u])
                best_next_action_value = q_tables[u][row_act][:].max()
                temporal_difference = Rew_U[u] + discount_factor * best_next_action_value - q_tables[u, row_act, AC_users[u]]
                q_tables[u, row_act, AC_users[u]] += learning_rate * temporal_difference
         '''
        #Collect Data
        AC_user_f [it_ind, :] = AC_users
        Ch_f [it_ind, :] = CH_Dis
        Battery_f [it_ind, :] = BT_Dis
        Rew_u_f[it_ind, :] = Rew_U
        G_Raw_f[it_ind, :] = G_Raw
        Total_energy_f[it_ind, :] = total_energy
        CH_raw_f [it_ind, :] = abs(CH_Raw)
        slot_aloc_it[it_ind, :, :] = slot_aloc_f
        explore_count.append(explore)
        exploit_count.append(exploit)
        # Update AOI using current frame AOI and add it into next frame AOI so that it can be used for next frame
        #Update Next State

    idx = t - 1  # if your loop is for t in range(1, test+1)

    # write full (iters × users) arrays into the memmaps
    AOI_mm[idx] = AOI_test_iter
    AC_mm[idx] = AC_user_f
    CH_mm[idx] = Ch_f
    BT_mm[idx] = Battery_f
    REW_mm[idx] = Rew_u_f
    G_mm[idx] = G_Raw_f
    CHRAW_mm[idx] = CH_raw_f
    Total_energy_mm[idx] = Total_energy_f


    # write 1D mean vectors
    ACmean_mm[idx] = np.mean(AC_user_f, axis=1)
    CHmean_mm[idx] = np.mean(Ch_f, axis=1)
    BTmean_mm[idx] = np.mean(Battery_f, axis=1)
    REWmean_mm[idx] = np.mean(Rew_u_f, axis=1)


    # drop local references and force collection
    del (AOI_test_iter,
         AC_user_f, Ch_f, Battery_f, Rew_u_f, G_Raw_f, CH_raw_f,Total_energy_f)
    gc.collect()

    #AC_user_tests [ :, :] = AC_user_f
    #CH_user_tests [ :, :] = Ch_f
    #BT_user_tests [ :, :] = Battery_f
    #REW_user_tests [:, :] = Rew_u_f
    #G_user_tests[ :, :] = G_Raw_f
    #Ch_Raw_tests[ :, :] = CH_raw_f
    #AC_user_Mean [ :] = np.mean(AC_user_f, axis=1)
    #CH_mean [:] = np.mean(Ch_f, axis=1)
    #Battery_mean [:] = np.mean(Battery_f, axis=1)
    #Rew_u_mean [:] = np.mean(Rew_u_f, axis=1)

    #save_per_test_matrix(G_user_tests, "G_user_tests", t-1, output_dir="data")
    #save_per_test_matrix(AC_user_tests, "AC_user_tests", t-1, output_dir="data")
    #save_per_test_matrix(CH_user_tests, "CH_user_tests", t-1, output_dir="data")
    #save_per_test_matrix(BT_user_tests, "BT_user_tests", t-1, output_dir="data")
    #save_per_test_matrix(REW_user_tests, "REW_user_tests", t-1, output_dir="data")
    #save_per_test_matrix(Ch_Raw_tests, "Ch_Raw_tests", t-1, output_dir="data")

    #save_per_test_vector(AC_user_Mean, "AC_user_Mean", t-1, output_dir="data")
    #save_per_test_vector(CH_mean, "CH_mean", t-1, output_dir="data")
    #save_per_test_vector(Battery_mean, "Battery_mean", t-1, output_dir="data")
    #save_per_test_vector(Rew_u_mean, "Rew_u_mean", t-1, output_dir="data")

    #AOI_test [t-1, :] = np.mean(AOI_test_iter[t-1, :, :], axis=0)
    # mean over iterations and slots → gives 1 number per user
    #slot_aloc_test[t - 1, :] = np.mean(slot_aloc_it, axis=(0, 2))
    #mean_slot = np.mean(slot_aloc_it[t], axis=0)  # shape: (users, slots_t)
    #slot_aloc_test.append(mean_slot)
    G [t-1]= number_of_users / number_of_slots
    #if t % chg_slots == 0:
     #   number_of_slots -= d_slot
      #  print(f"Slots Changed at test {t}: {number_of_slots}")
    #min_epsilon += 0.05
    #number_of_users += 1
    #dist_max += 0.03
    #K_factor -= 0.01
   # learning_rate -= 0.000005
    #learning_rate = round(learning_rate, 6)
    #K_factor = round(K_factor, 2)
    #dist_max = round(dist_max, 2)
    print(f"Test {t} Finished")
    #print(f"Distance: {dist_max}")
    #print(f"Updated Learning Rate: {learning_rate}")
    #print(f"Updated K factor: {K_factor}")

#print(f"Last Q Table {q_tables}")

for mm in (AOI_mm, AC_mm, CH_mm, BT_mm, REW_mm, G_mm, CHRAW_mm,
           ACmean_mm, CHmean_mm, BTmean_mm, REWmean_mm):
    mm.flush()



# —————————————————————————————————————————————————————
# 4) SAVE ALL MEMMAPS DIRECTLY TO .npy
# —————————————————————————————————————————————————————

# map of output filename (without “.npy”) → memmap object
matrices_to_save = {
    "AOI_test_iter": AOI_mm,
    "AC_user_tests": AC_mm,
    "CH_user_tests": CH_mm,
    "BT_user_tests": BT_mm,
    "REW_user_tests": REW_mm,
    "G_user_tests": G_mm,
    "Ch_Raw_tests": CHRAW_mm,
    "Total_energy_tests": Total_energy_mm,
}

vectors_to_save = {
    "AC_user_mean": ACmean_mm,
    "CH_mean":      CHmean_mm,
    "Battery_mean": BTmean_mm,
    "Rew_u_mean":   REWmean_mm,
}

for name, arr in matrices_to_save.items():
    out_path = os.path.join(Out_dir, f"{name}.npy")
    # this writes the full shape‑(test, iters, users) array to disk
    np.save(out_path, arr)

for name, arr in vectors_to_save.items():
    out_path = os.path.join(Out_dir, f"{name}.npy")
    # shape‑(test, users) mean vectors
    np.save(out_path, arr)




#output_dir = "data"


#AC_user_tests = load_matrix_tests("AC_user_tests", test, input_dir=output_dir)
#CH_user_tests = load_matrix_tests("CH_user_tests", test, input_dir=output_dir)
#BT_user_tests = load_matrix_tests("BT_user_tests", test, input_dir=output_dir)
#REW_user_tests = load_matrix_tests("REW_user_tests", test, input_dir=output_dir)
#G_user_tests = load_matrix_tests("G_user_tests", test, input_dir=output_dir)
#Ch_Raw_tests = load_matrix_tests("Ch_Raw_tests", test, input_dir=output_dir)

# Precomputed mean vectors from earlier save
#AC_user_Mean = load_vector_tests("AC_user_Mean", test, input_dir=output_dir)
#CH_mean = load_vector_tests("CH_mean", test, input_dir=output_dir)
#Battery_mean = load_vector_tests("Battery_mean", test, input_dir=output_dir)
#Rew_u_mean = load_vector_tests("Rew_u_mean", test, input_dir=output_dir)

# If you want to compute the mean over iterations → (tests, users)



#plot_aoi_block_avg(AOI_mean, number_of_slots, number_of_users, block_size=100)

AOI_test_means = []
AOI_test_stds = []
#G_values = []
#current_slots = number_of_slots

# Plot with error bars
#plt.figure(figsize=(8, 6))
#plt.errorbar(G_v, AOI_test_means, yerr=AOI_test_stds, fmt='-o', capsize=5, label='Avg AOI ± StdDev')

#plot_channel_gain_histograms(G_user_tests, user_indices=2, bins=10, bin_range=(0, 5))

xf = np.linspace(0, iterations, iterations)
fig2, ax = plt.subplots(1, 1)
ax.plot(xf, epsilon_t[0,:], 'b-', lw=1, alpha=1, label=f'Epsilon')  # AoI medio del sistema per ogni iterazione
ax.set_title('Epsilon vs Frames')
ax.set_ylabel('Epsilon')
ax.set_xlabel('Frames')
ax.legend()
plt.tight_layout()
#fig.show()
ax.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(explore_count, label="Exploration", color='red', linewidth=2)
plt.plot(exploit_count, label="Exploitation", color='blue', linewidth=2)

plt.xlabel("Frame")
plt.ylabel("Cumulative Count")
plt.title("Exploration vs Exploitation Over Time")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


slots = []
for t in range(test):
    slots.append(number_of_slots + d_slot*test - d_slot*t)
#for t in range(test):
 #   plot_action_reward_relations(AC_user_Mean[t, :], CH_mean [t, :], Battery_mean [t, :], Rew_u_mean [t, :], slots[t], smoothing_span=50)
  #  plot_3d_action_vs_channel_battery(AC_user_Mean [t, :], CH_mean [t, :], Battery_mean [t, :], slots[t])
   # plot_actions_vs_channel_contour(CH_mean[t, :], AC_user_Mean[t, :], Battery_mean[t, :], slots[t])
    #plot_reward_vs_actions_contour(AC_user_Mean [t, :], Rew_u_mean [t, :], CH_mean [t, :], slots[t])
    #slots -= d_slot

#xf = np.linspace(0, iterations, iterations)
#fig1, ax = plt.subplots(1, 1)
#ax.plot(xf, AOI_avg_all[:,0], 'o', lw=1, alpha=1, label=f'Average AoI S= {slots[0]}, U = {0}')  # AoI medio del sistema per ogni iterazione
#ax.plot(xf, AOI_avg_all[:,1], 'k*', lw=3, alpha=1, label=f'Average AoI S= {slots[0]}, U = {1}')  # AoI medio del sistema per ogni iterazione
#ax.plot(xf, AOI_avg_all[:,2], '+', lw=1, alpha=1, label=f'Average AoI S= {slots[0]}, U = {2}')  # AoI medio del sistema per ogni iterazione
#ax.set_title('AoI Evolvement vs Iterations')
#ax.set_ylabel('Users AoI')
#ax.set_xlabel('Frames')
#ax.legend()
#plt.tight_layout()
#fig.show()
#ax.grid(True)
#plt.show()

#plot_reward_vs_actions_contour_all_tests (AC_user_Mean, Rew_u_mean, CH_mean, slots)

#plot_action_vs_channel_battery_all_tests(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50)

#plot_action_vs_channel_battery_contour_highres(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50, save_pdf=True)

#plot_action_vs_channel_battery_3d(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50, save_pdf=True)

#plot_action_vs_channel_battery_3d_subplots(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50)

#plot_userwise_contours_all_tests(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots, smooth_span=50)

#plot_userwise_density_all_tests(CH_user_tests, BT_user_tests, slots, smooth_span=50, bins=100)


#plot_userwise_reward_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots,
   #                                       smooth_span=50, bins=100)

#plot_userwise_action_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, slots,
  #                                        smooth_span=50, bins=100)


#plot_userwise_reward_density_barplot(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots, smooth_span=50, bins=30)

#plot_userwise_action_density_barplot(AC_user_tests, CH_user_tests, BT_user_tests, slots, smooth_span=50, bins=30)


#plot_userwise_reward_bar_grid_all_tests(CH_user_tests, BT_user_tests, REW_user_tests, slots,
      #                                      user_index=0, bins=10, smooth_span=50)


#plot_userwise_action_bar_grid_all_tests(CH_user_tests, BT_user_tests, AC_user_tests, slots,
 #                                           user_index=0, bins=10, smooth_span=50)

#plot_action_histograms_per_test(AC_user_tests, num_bins=10)

#plot_combined_action_histogram_all_users(AC_user_tests, num_bins=10)

#for t in range(test):

 #   plot_contour_action(CH_user_tests, BT_user_tests, AC_user_tests, t, smooth_span=50)

  #  plot_contour_reward(CH_user_tests, BT_user_tests, REW_user_tests, t, smooth_span=50)


#plot_hexbin_all_tests(CH_user_tests, BT_user_tests, AC_user_tests, label="Action", title="Action Hexbin")

#plot_hexbin_all_tests(CH_user_tests, BT_user_tests, REW_user_tests, label="Reward", title="Reward Hexbin")


#plot_bar_grid_all_tests(CH_user_tests, BT_user_tests, AC_user_tests, label="Action", title="Action Bar Grid")

#plot_bar_grid_all_tests(CH_user_tests, BT_user_tests, REW_user_tests, label="Reward", title="Reward Bar Grid")

#plot_action_vs_battery(CH_user_tests, BT_user_tests, AC_user_tests)
#plot_reward_vs_action(AC_user_tests, REW_user_tests)
#plot_battery_evolution(BT_user_tests)

#plot_avg_battery_evolution(BT_user_tests, [0, 3, 5])
#plot_battery_delta_over_frames(BT_user_tests)

#plot_action_vs_battery_combined(CH_user_tests, BT_user_tests, AC_user_tests, smooth_span=50, num_bins=20)
#plot_userwise_action_histograms(AC_user_tests, num_bins=10)
#plot_userwise_avg_action_heatmaps(AC_user_tests, num_actions=6)
#plot_user_slot_activity_histograms(slot_aloc_it)
#plot_idle_slot_trend(idle_slots)

#plot_testwise_action_evolution(AC_user_tests, smoothing_window=3)

#plot_testwise_reward_evolution(REW_user_tests, smoothing_window=3)

#plot_testwise_battery_evolution(BT_user_tests, smoothing_window=3)

#plot_aoi_evolution(AOI_test_iter, smoothing_window=1000)

#AOI_test_iter_all = load_test_matrix_npy("AOI_test_iter", Out_dir)

#plot_aoi_testwise(AOI_test_iter_all, smoothing_window=30)

#plot_final_aoi_per_test(AOI_test_iter_all, smoothing_window=30)

#plot_action_reward_contour(CH_user_tests, BT_user_tests, REW_user_tests, mode="global", value_label="Reward")
#plot_action_reward_contour(CH_user_tests, BT_user_tests, AC_user_tests, mode="global", value_label="Action")

print (f"Explore: {explore}")
print (f"Exploit: {exploit}")