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
#from Data_IO import *
import os
import matplotlib.patches as patches
from scipy.stats import binned_statistic_2d
#import pandas as pd
#from pandas import DataFrame
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
test = 3
learning_rate = 0.001
#define system parameters
mu_bu= 0.05 # one unit of battery
number_of_slots = 4
number_of_users = 2
time_duration = 0.025
p= 4.6
dist_min = 1
dist_max = 7
s_AAOI = []
Gain = []
Th= 0.2
iterations = 10000
Frame_size = []
STD_AoI_u_AT = []
STD_AoI_u_BT = []
Batch_size = 10
it_ind = 0
explore_count = []
exploit_count = []
explore = 0
exploit = 0
K_factor =  15
decay_rate = 0.0005
upsilon = 0.025 # One unit to transmit one replica
d_slot = 8


from pathlib import Path

# ————————————————
# 1) absolute base dir:
# ————————————————
BASE_DIR = Path(r"C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q learning Paper\Data July\JAL_U100")
if not BASE_DIR.exists():
    raise FileNotFoundError(f"{BASE_DIR!r} does not exist")
# ——————————————————————————————————
# 2) construct the per‐experiment subfolder
# ——————————————————————————————————
slots = 100
users = 100

#BASE_DIR_IL = Path (BASE_DIR / r"E:\IL_U100")

subfolder = f"JAL_S_{slots}_U_{users}_c"
Out_dir_2 = str(BASE_DIR / subfolder)
Out_dir = r'JAL_S_100_U_100_K3'
# (optional) if your load_… functions expect a str rather than a Path
Out_dir = str(Out_dir)

# sanity check
if not os.path.isdir(Out_dir):
    raise FileNotFoundError(f"Results folder not found: {Out_dir!r}")

Ch_Raw_tests = load_test_matrix_npy("Ch_Raw_tests", Out_dir) #K3
Ch_Raw_tests2 = load_test_matrix_npy("Ch_Raw_tests", Out_dir_2) #K3


import matplotlib.pyplot as plt

# Flatten the 3D matrices: tests × frames × users → 1D arrays
ch_k3 = Ch_Raw_tests.flatten()
ch_k12 = Ch_Raw_tests2.flatten()

# Optional: Normalize each dataset (if values are not already on a comparable scale)
# ch_k3 = ch_k3 / np.max(ch_k3)
# ch_k12 = ch_k12 / np.max(ch_k12)

# Plot histogram
plt.figure(figsize=(8, 5))
plt.hist(ch_k3, bins=100, density=True, alpha=0.6, label='K = 3', color='skyblue', edgecolor='black')
plt.hist(ch_k12, bins=100, density=True, alpha=0.6, label='K = 12', color='salmon', edgecolor='black')

plt.xlabel("Channel Gain (Rician + Path Loss)")
plt.ylabel("Probability Density")
plt.title("Normalized Histogram of Channel Gains (K=3 vs K=12)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
