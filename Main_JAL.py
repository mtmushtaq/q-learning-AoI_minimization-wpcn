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
test = 200
learning_rate = 0.0001
#define system parameters
mu_bu= 0.05 # initial one unit of battery
number_of_slots = 100
number_of_users = 100
time_duration = 0.02
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
K_factor =  12
decay_rate = 0.0009
upsilon = 0.02 # One unit to transmit one replica
d_slot = 1
chg_slots = 80
#u = np.empty(number_of_users, dtype=object)  # define users array
#for i in range(number_of_users):
 #   u[i] = i + 1
# q_tables = np.zeros (k.size * x.size, a.size)
k = np.array([0, 1, 2, 3, 4, 5])  # possible power values
x = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # channel quality information
a = np.array([0, 1, 2, 3, 4, 5])
Out_dir  = "JAL_S_100_U_100_c"
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
def get_rew(B_AOI, A_AOI, BT, act, ch, max_AOI=100, max_BT=5, w1=0.9, w2=0.6, w3=0.6):
    D_AOI = B_AOI - A_AOI
    D_AOI_norm = D_AOI / number_of_slots
    act_norm = act / 5
    ch_norm = ch / 7.0
    BT_norm = BT / 5
    reward = 0
    #np.clip(D_AOI, 0, number_of_slots)
    if act == BT and ch >= 4:
        reward = w1 * np.clip(D_AOI, 0, number_of_slots) + w2 * (act_norm / (ch_norm + 0.1)) + w3 * BT_norm
    else:
        reward = w1 * np.clip(D_AOI, 0, number_of_slots) + w2 * (2 * act_norm) + w3 * BT_norm
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

## Command to randomly pick values----->>>>> np.random.randint(0, 7, size=(k.size * x.size, a.size), dtype=int)
#reward = np.empty((number_of_users, iterations+1), dtype=float)
#AOI = np.zeros((number_of_users, iterations+1), dtype=int)

#discount_factor = 0.9
#learning_rate = 0.001
# step_size_ep= (1-0.4)/iterations

users = []
for i in range(number_of_users):  # popola il vettore degli utenti
    # users[i] = i + 1
    users.append(User(id=i, mu=upsilon, initial_battery_level=0.05))  # inizializza ogni utente con un livello di batteria di 0.005

q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=np.float32)
for user in range(np.size(users)):
    q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
#print(f"first Q Table {q_tables}")

AOI_users = np.ones((iterations*test, number_of_users), dtype=int)
AOI_users_tests = np.empty((test, iterations,number_of_users), dtype=int)
#print(q_tables)
# print(f"All State matrix {S}")
G = np.empty(test, dtype = np.float32)


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
        S = np.empty((number_of_users, 1, 2), dtype=np.float32)  # To save state of all users in current frame
        EH_Raw = np.empty(number_of_users, dtype=np.float32)  # to save raw battery capacity of all users at current iteration/frame
        #EH_Raw[:, 0] = EH_Raw[:, 0] + 0.05
        BT_Dis = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
        CH_Raw = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
        CH_Dis = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
        G_Raw = np.empty(number_of_users, dtype=np.float32) # to save Gamma of current frame
        AC_users = np.empty(number_of_users, dtype=int) #to save action in current frame for reward calculation
        Rew_U = np.empty(number_of_users, dtype=np.float32)  #
        #Calculate the channel and update battery for current frame
        #for u in range (np.size(users)):

            #EH_Raw [u] = compute_energy_harvested(G_Raw, time_duration, p)
            #users[u] =
        randx = np.random.random()
        randx = round(randx, 5)
        if randx <= epsilon:  # Random Action Selection
            explore += 1
            for d in range (np.size(users)):
                CH_Raw[d] = generate_rician_fading(K_factor)
                users[d].channel = CH_Raw[d]
                G_Raw[d] = gamma_EH(CH_Raw[d], dist[d]) #dist_min, dist_max)
                BT_Dis[d] = users[d].BT_units()
                CH_Dis [d] = get_channel(G_Raw[d])
                bt_units = users[d].BT_units()
                if bt_units > number_of_slots:
                    bt_units = number_of_slots
                prob_dist = get_distr(bt_units)
                if bt_units == 0:
                    slot_aloc_f [d,:] = np.zeros ((1, number_of_slots), dtype=int)
                    AC_users [d] = 0
                    #print(f"Random Action of User {d} is {0}")
                else:
                    range_slot = np.array(range(0, number_of_slots), dtype=int) # to ask it to make a choice between first and last slot
                    range_action = np.array(range(1, len(prob_dist)+1), dtype=int) # to choose an action between 1 and max_battery unit with prob_dist
                    user_action = np.random.choice(range_action, size=1, p=prob_dist) # choose an action based on prob_dist
                    if user_action > a.size:
                        user_action  = a.size
                    slot_indices = np.random.choice(range_slot, size=user_action, replace=False) #choose random slots to send the packet
                    slot_aloc_f[d, slot_indices] = 1  #Make selected slots 1 for user's row
                    users[d].decrease_EH(user_action)
                    #BT_Dis[d] = users[d].BT_units()
                    AC_users[d] = user_action[0]
                    #print(f"Random Action of User {d} is {user_action}")
                #slot_aloc_f [d-1, :]
                #reward[d][it_ind] = get_rew(action)
                #Remove action unit of energy from total energy
                #EH_Raw[d, it_ind] = get_dis_AT (EH_Raw[d-1, 0], action, mu_bu)
                # print(f"Explore")

                # print(f"d: {d}")
                # print(f"User {d} has state : {S[d-1]}")
        else:
            # do the max action from Q table
            # value = q_tables[d - 1][current_row][0:(pw+1)].max()
            # values[d] = value
            # index = np.where(q_tables[d + 1][current_row][0:(pw+1)] == value)
            # action = a[index].max()
            # actions[d] = action
            exploit += 1
            #### Before going into explore or exploit factor, calculate the energy harvested, Channel, Current battery and other factor of each user.
            for d in range(np.size(users)):
                CH_Raw[d] = generate_rician_fading(K_factor)
                users[d].channel = CH_Raw[d]
                G_Raw[d] = gamma_EH(CH_Raw[d], dist[d])  # dist_min, dist_max)
                BT_Dis[d] = users[d].BT_units()
                CH_Dis[d] = get_channel(G_Raw[d])
                bt_units = users[d].BT_units()
                row_act = get_row(BT_Dis[d], CH_Dis[d])

                #print(f"Power from State: {S[0][0]}")
                #print(f"Channel from State: {S[0][1]}")
                #print(f"Action Row {row_act}")
                value = q_tables[d][row_act][:].max()
                #print(f"Max Q table for PW: {S[0][0]} and Ch {S[0][1]} of user {d}: {value}")
                # values[d] = value
                index = np.where(q_tables[d][row_act][:] == value)
                #print(f"Index: {index}")
                #print(f"Action Vector: {a}")
                #action = int(a[index])
                action = a[index][0].item()  # Extract the first element as a pure integer
                #print(f"Q-Max Action of User {d} is {action}")
                if action == 0:
                    slot_aloc_f [d,:] = np.zeros ((1, number_of_slots), dtype=int)
                else:
                    if action > number_of_slots:
                        action = number_of_slots
                    if action > a.size:
                        action  = a.size
                    if action > BT_Dis[d]:
                        action= BT_Dis[d]
                    ind_u = np.random.choice(number_of_slots , size= action, replace=False) #rd.sample(range(number_of_slots), action)
                    slot_aloc_f[d , ind_u] = 1
                    users[d].decrease_EH(action) #update battery
                    #BT_Dis[d] = users[d].BT_units()
                AC_users[d] = action
                #print(f"take action: {action}")
                #reward[d][it_ind] = get_rew(action)
                # Remove action unit of energy from total energy
                #EH_Raw[d, it_ind] = get_dis_AT(EH_Raw[d - 1, 0], action, mu_bu)
                #Get NEXT STATE
                #d = d + 1
        #use free slots for energy harvesting
        for i in range(number_of_slots):
            if np.sum(slot_aloc_f[:, i]) == 0:

                idle_slots [it_ind] += 1 #track idle slots each iteration
                # Normalize AOI to form probabilities (avoid zero-sum issue)
                if np.sum(AOI_af) == 0:
                    prob_aoi = np.ones(number_of_users) / number_of_users  # uniform fallback
                else:
                    prob_aoi = AOI_af / np.sum(AOI_af)
                u = np.random.choice(np.arange(number_of_users), p=prob_aoi)
                #u = rd.randint(0, number_of_users - 1)
                # for u in range(number_of_users):
                #    if u == user_to_transmit:
                pw_u = compute_energy_harvested(G_Raw[u], time_duration, p)
                users[u].add_EH(pw_u)
                #BT_Dis[u] = users[u].BT_units()

        # apply SIC
        decoded_users = capture_effect_SIC_realtime(slot_aloc_f, number_of_slots, number_of_users, G_Raw, verbose=False) # Rearly-n method

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
            Rew_U [u] = get_rew (Bf_aoi [u], Af_aoi[u] , BT_Dis[u] , AC_users[u], CH_Dis[u])
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
        if (it_ind + 1) % Batch_size == 0:
            # Get new State and update Q-Table
            dist = np.random.uniform(dist_min, dist_max, size=number_of_users)
            BT_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
            CH_Raw_next = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
            CH_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
            G_Raw_next = np.empty(number_of_users, dtype=float)  # to save Gamma of current frame
            Cumulative_Rew = np.sum(Rew_U)
            for u in range(number_of_users):
                CH_Raw_next[u] = generate_rician_fading(K_factor)
                users[u].channel = CH_Raw_next[u]
                G_Raw_next[u] = gamma_EH(CH_Raw_next[u], dist[u]) #dist_min, dist_max)
                BT_Dis_next[u] = users[u].BT_units()
                CH_Dis_next[u] = get_channel(G_Raw[u])
                row_act = get_row(BT_Dis_next[u], CH_Dis_next[u])
                best_next_action_value = q_tables[u][row_act][:].max()
                temporal_difference = Cumulative_Rew + discount_factor * best_next_action_value - q_tables[u, row_act, AC_users[u]]
                q_tables[u, row_act, AC_users[u]] += learning_rate * temporal_difference

        #Collect Data
        AC_user_f [it_ind, :] = AC_users
        Ch_f [it_ind, :] = CH_Dis
        Battery_f [it_ind, :] = BT_Dis
        Rew_u_f[it_ind, :] = Rew_U
        G_Raw_f[it_ind, :] = G_Raw
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

    # write 1D mean vectors
    ACmean_mm[idx] = np.mean(AC_user_f, axis=1)
    CHmean_mm[idx] = np.mean(Ch_f, axis=1)
    BTmean_mm[idx] = np.mean(Battery_f, axis=1)
    REWmean_mm[idx] = np.mean(Rew_u_f, axis=1)

    # drop local references and force collection
    del (AOI_test_iter,
         AC_user_f, Ch_f, Battery_f, Rew_u_f, G_Raw_f, CH_raw_f)
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
    min_epsilon += 0.05
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
}

vectors_to_save = {
    "AC_user_Mean_all": ACmean_mm,
    "CH_mean":      CHmean_mm,
    "Battery_mean": BTmean_mm,
    "Rew_u_mean_all":   REWmean_mm,
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