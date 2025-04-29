#import sys
#import matplotlib
#matplotlib.use('Qt5Agg')  # Or TkAgg 'Qt5Agg', 'GTK3Agg' depending on your system
#from typing import Any
import random as rd
import numpy as np
from numpy import ndarray, dtype
from State_User import * #generate_rician_fading, gamma_EH, compute_energy_harvested
from Discritize_state import get_dis_BT, get_dis_AT, CH_dist
from SIC import *
from User import User
#import pandas as pd
from pandas import DataFrame

# This code with an optimized Learning rate= 0.5, But we need to find the value of Epsilon for good convergence
# define training parameters
discount_factor = 0.9  # 0.001
test = 4
learning_rate = 0.01
#define system parameters
mu_bu= 0.05 # one unit of battery
number_of_slots = 20
number_of_users = 5
time_duration = 0.02
p= 4.6
dist_min = 1
dist_max = 30
s_AAOI = []
Gain = []
Th= 0.2
iterations = 25000
Frame_size = []
STD_AoI_u_AT = []
STD_AoI_u_BT = []
Batch_size = 250
it_ind = 0
explore = 0
exploit = 0
K_factor =  15
decay_rate = 0.0001
upsilon = 0.03 # One unit to transmit one replica
d_slot = 1
#u = np.empty(number_of_users, dtype=object)  # define users array
#for i in range(number_of_users):
 #   u[i] = i + 1
# q_tables = np.zeros (k.size * x.size, a.size)
k = np.array([0, 1, 2, 3, 4, 5])  # possible power values
x = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # channel quality information
a = np.array([0, 1, 2, 3, 4, 5])

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
def get_rew(B_AOI, A_AOI, BT, act, ch, max_AOI=100, max_BT=5, w1=0.7, w2=0.5, w3=0.5):
    D_AOI = B_AOI - A_AOI
    D_AOI_norm = D_AOI / number_of_slots
    act_norm = act / 5
    ch_norm = ch / 7.0
    BT_norm = BT / 5

    reward = 0
    if act == BT:
        reward = w1 * D_AOI_norm + w2 * (act_norm / (ch_norm + 0.1)) + w3 * BT_norm
    elif act < BT:
        reward = w1 * D_AOI_norm + w2 * (2 * act_norm) + w3 * BT_norm
    return reward


def get_distr(pw):
    #if pw == 0:
     #   distr = 0
      #  return distr
    if pw == 1:
        distr = np.array([1])
        return distr
    elif pw == 2:
        distr = np.array([0.75, 0.25])
        return distr
    elif pw == 3:
        distr = np.array([0.7, 0.2, 0.1])
        return distr
    elif pw == 4:
        distr = np.array([0.625, 0.2083, 0.1042, 0.0625])
        return distr
    elif pw == 5:
        distr = np.array([0.6, 0.2, 0.1, 0.06, 0.04])
        return distr


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

def plot_action_reward_relations(AC_user_Mean, CH_mean, Battery_mean, Rew_u_mean, slots, smoothing_span=50):
    frames = np.arange(len(AC_user_Mean))

    # --- SMOOTHING ---
    AC_user_Mean_smooth = pd.Series(AC_user_Mean).ewm(span=smoothing_span).mean()
    CH_mean_smooth = pd.Series(CH_mean).ewm(span=smoothing_span).mean()
    Battery_mean_smooth = pd.Series(Battery_mean).ewm(span=smoothing_span).mean()
    Rew_u_mean_smooth = pd.Series(Rew_u_mean).ewm(span=smoothing_span).mean()

    # --- 1. Smoothed Channel & Battery over Frames ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Frame')
    ax1.set_ylabel('Mean Channel (Smoothed)', color=color)
    ax1.plot(frames, CH_mean_smooth, color=color, label=f"Channel, Slots = {slots}")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Mean Battery (Smoothed)', color=color)
    ax2.plot(frames, Battery_mean_smooth, color=color, label=f"Battery , Slots = {slots}")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Channel and Battery vs Frames, Slots = {slots}')
    fig.tight_layout()
    plt.show()

    # --- 2. Smoothed Actions vs Channel ---
    plt.figure(figsize=(10, 6))
    plt.scatter(CH_mean_smooth, AC_user_Mean_smooth, c=Battery_mean_smooth, cmap='viridis', alpha=0.7)
    plt.colorbar(label=f"Mean Battery , Slots = {slots}")
    plt.xlabel("Mean Channel")
    plt.ylabel("Mean Actions (Replicas) ")
    plt.title(f"Actions vs Channel, Slots = {slots}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- 3. Smoothed Reward vs Actions ---
    plt.figure(figsize=(10, 6))
    plt.scatter(AC_user_Mean_smooth, Rew_u_mean_smooth, c=CH_mean_smooth, cmap='plasma', alpha=0.7)
    plt.colorbar(label="Mean Channel")
    plt.xlabel("Mean Actions")
    plt.ylabel("Mean Reward")
    plt.title(f"Reward vs Actions, Slots = {slots}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- 4. 3D Scatter Plot: Reward vs Channel vs Battery (Smoothed) ---
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(CH_mean_smooth, Battery_mean_smooth, Rew_u_mean_smooth, c=Rew_u_mean_smooth, cmap='coolwarm', s=40)

    ax.set_xlabel('Mean Channel')
    ax.set_ylabel('Mean Battery')
    ax.set_zlabel('Mean Reward')
    ax.set_title(f'Reward Surface w.r.t Channel and Battery, Slots = {slots}')
    ax.view_init(elev=30, azim=135)
    plt.tight_layout()
    plt.show()

    # --- 5. Correlation Heatmap ---
    df = pd.DataFrame({
        'Actions': AC_user_Mean_smooth,
        'Channel': CH_mean_smooth,
        'Battery': Battery_mean_smooth,
        'Reward': Rew_u_mean_smooth
    })

    corr_matrix = df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    plt.title(f"Correlation Heatmap, Slots = {slots}")
    plt.tight_layout()
    plt.show()

def plot_3d_action_vs_channel_battery(AC_user_Mean, CH_mean, Battery_mean, slots):
    """
    Plots a 3D scatter plot: Actions vs Channel vs Battery
    to visualize how the agent selects actions depending on channel and battery.

    Args:
        AC_user_Mean (np.ndarray): Mean actions taken across users per frame.
        CH_mean (np.ndarray): Mean channel quality across users per frame.
        Battery_mean (np.ndarray): Mean battery level across users per frame.
        title (str): Title of the plot.
    """
    # --- Smoothing the curves using Exponential Moving Average (EMA) ---
    span = 50
    ac_smooth = np.array(pd.Series(AC_user_Mean).ewm(span=span).mean())
    ch_smooth = np.array(pd.Series(CH_mean).ewm(span=span).mean())
    bat_smooth = np.array(pd.Series(Battery_mean).ewm(span=span).mean())

    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')

    # --- Scatter plot ---
    p = ax.scatter(ch_smooth, bat_smooth, ac_smooth, c=ac_smooth, cmap='viridis', s=40)

    ax.set_xlabel("Mean Channel Quality")
    ax.set_ylabel("Mean Battery Level")
    ax.set_zlabel("Mean Action (Replicas)")
    ax.set_title(f"Action vs Channel vs Battery {slots}")
    fig.colorbar(p, ax=ax, shrink=0.5, aspect=10, label='Mean Action Level')
    ax.view_init(elev=30, azim=135)
    plt.tight_layout()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

from scipy.interpolate import griddata
def plot_actions_vs_channel_contour(CH_mean, AC_user_Mean, Battery_mean, slots, smooth_span=50):
    # Smooth inside
    CH_mean_smooth = pd.Series(CH_mean).ewm(span=smooth_span).mean().to_numpy()
    AC_user_Mean_smooth = pd.Series(AC_user_Mean).ewm(span=smooth_span).mean().to_numpy()
    Battery_mean_smooth = pd.Series(Battery_mean).ewm(span=smooth_span).mean().to_numpy()

    # Grid for contour
    xi = np.linspace(min(CH_mean_smooth), max(CH_mean_smooth), 100)
    yi = np.linspace(min(Battery_mean_smooth), max(Battery_mean_smooth), 100)
    Xi, Yi = np.meshgrid(xi, yi)

    # Interpolate Actions onto grid
    zi = griddata((CH_mean_smooth, Battery_mean_smooth),AC_user_Mean_smooth, (Xi, Yi), method='cubic')

    plt.figure(figsize=(10, 6))
    contour = plt.contourf(Xi, Yi, zi, levels=20, cmap='viridis')
    plt.colorbar(contour, label="Mean Actions (Replicas)")
    plt.xlabel("Mean Channel (Smoothed)")
    plt.ylabel("Mean Battery (Smoothed)")
    plt.title(f"Actions vs Channel and Battery {slots}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_reward_vs_actions_contour(AC_user_Mean, Rew_u_mean, CH_mean, slots, smooth_span=50):
    # Smooth inside
    AC_user_Mean_smooth = pd.Series(AC_user_Mean).ewm(span=smooth_span).mean().to_numpy()
    Rew_u_mean_smooth = pd.Series(Rew_u_mean).ewm(span=smooth_span).mean().to_numpy()
    CH_mean_smooth = pd.Series(CH_mean).ewm(span=smooth_span).mean().to_numpy()

    # Grid for contour
    xi = np.linspace(min(AC_user_Mean_smooth), max(AC_user_Mean_smooth), 100)
    yi = np.linspace(min(CH_mean_smooth), max(CH_mean_smooth), 100)
    Xi, Yi = np.meshgrid(xi, yi)

    # Interpolate Reward onto grid
    zi = griddata((AC_user_Mean_smooth, CH_mean_smooth), Rew_u_mean_smooth,(Xi, Yi), method='cubic')

    plt.figure(figsize=(10, 6))
    contour = plt.contourf(Xi, Yi, zi, levels=20, cmap='plasma')
    plt.colorbar(contour, label="Mean Reward")
    plt.xlabel("Mean Actions (Smoothed)")
    plt.ylabel("Mean Channel (Smoothed)")
    plt.title(f"Reward vs Actions and Channel {slots}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_reward_vs_actions_contour_all_tests(AC_user_Mean, Rew_u_mean, CH_mean, slots_list, smooth_span=50):
    num_tests = AC_user_Mean.shape[0]
    fig, axs = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)

    if num_tests == 1:
        axs = [axs]  # Make it iterable even for 1 subplot

    for t in range(num_tests):
        AC_user_Mean_smooth = pd.Series(AC_user_Mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Rew_u_mean_smooth = pd.Series(Rew_u_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        CH_mean_smooth = pd.Series(CH_mean[t]).ewm(span=smooth_span).mean().to_numpy()

        xi = np.linspace(min(AC_user_Mean_smooth), max(AC_user_Mean_smooth), 100)
        yi = np.linspace(min(CH_mean_smooth), max(CH_mean_smooth), 100)
        Xi, Yi = np.meshgrid(xi, yi)

        zi = griddata((AC_user_Mean_smooth, CH_mean_smooth), Rew_u_mean_smooth, (Xi, Yi), method='cubic')

        cs = axs[t].contourf(Xi, Yi, zi, levels=20, cmap='plasma')
        fig.colorbar(cs, ax=axs[t])
        axs[t].set_xlabel("Mean Actions (Smoothed)")
        axs[t].set_ylabel("Mean Channel (Smoothed)")
        axs[t].set_title(f"Slots={slots_list[t]}")

    fig.suptitle("Reward vs Actions and Channel across Tests", fontsize=16)
    plt.show()

def plot_action_vs_channel_battery_all_tests(CH_mean, Battery_mean, AC_user_Mean, slots_list, smooth_span=50):
    """
    Plot contour plots showing how Actions depend on Channel and Battery across multiple tests.
    Now adds value labels inside contours!
    """
    num_tests = AC_user_Mean.shape[0]
    fig, axs = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)

    if num_tests == 1:
        axs = [axs]  # make it iterable

    for t in range(num_tests):
        # Smooth
        CH_smooth = pd.Series(CH_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Battery_smooth = pd.Series(Battery_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Action_smooth = pd.Series(AC_user_Mean[t]).ewm(span=smooth_span).mean().to_numpy()

        # Grid
        xi = np.linspace(min(CH_smooth), max(CH_smooth), 100)
        yi = np.linspace(min(Battery_smooth), max(Battery_smooth), 100)
        Xi, Yi = np.meshgrid(xi, yi)

        # Interpolate
        zi = griddata((CH_smooth, Battery_smooth), Action_smooth, (Xi, Yi), method='cubic')

        # Plot filled contour
        cs = axs[t].contourf(Xi, Yi, zi, levels=20, cmap='viridis')
        fig.colorbar(cs, ax=axs[t])

        # 🧠 Add numeric labels inside
        cs2 = axs[t].contour(Xi, Yi, zi, levels=10, colors='black', linewidths=0.5)
        axs[t].clabel(cs2, inline=True, fontsize=8, fmt="%.1f")  # fmt formats the numbers

        axs[t].set_xlabel("Mean Channel (Smoothed)")
        axs[t].set_ylabel("Mean Battery (Smoothed)")
        axs[t].set_title(f"Actions | Slots={slots_list[t]}")

    fig.suptitle("Actions vs Channel and Battery across Tests", fontsize=16)
    plt.show()


def plot_action_vs_channel_battery_contour_highres(CH_mean, Battery_mean, AC_user_Mean, slots_list, smooth_span=50, save_pdf=False):
    """
    High-resolution contour plots for Actions vs Channel and Battery across multiple tests.
    Option to export as PDF.
    """
    num_tests = AC_user_Mean.shape[0]
    fig, axs = plt.subplots(1, num_tests, figsize=(6 * num_tests, 6), constrained_layout=True, dpi=300)

    if num_tests == 1:
        axs = [axs]

    for t in range(num_tests):
        # Smooth
        CH_smooth = pd.Series(CH_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Battery_smooth = pd.Series(Battery_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Action_smooth = pd.Series(AC_user_Mean[t]).ewm(span=smooth_span).mean().to_numpy()

        # Grid
        xi = np.linspace(min(CH_smooth), max(CH_smooth), 150)
        yi = np.linspace(min(Battery_smooth), max(Battery_smooth), 150)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = griddata((CH_smooth, Battery_smooth), Action_smooth, (Xi, Yi), method='cubic')

        # Plot
        cs = axs[t].contourf(Xi, Yi, zi, levels=30, cmap='viridis')
        fig.colorbar(cs, ax=axs[t])

        # Add lines and labels
        cs2 = axs[t].contour(Xi, Yi, zi, levels=10, colors='black', linewidths=0.7)
        axs[t].clabel(cs2, inline=True, fontsize=7, fmt="%.1f")

        axs[t].set_xlabel("Mean Channel (Smoothed)", fontsize=10)
        axs[t].set_ylabel("Mean Battery (Smoothed)", fontsize=10)
        axs[t].set_title(f"Actions vs Channel & Battery (Slots={slots_list[t]})", fontsize=11)
        axs[t].grid(True)

    fig.suptitle("Actions vs Channel and Battery across Tests", fontsize=14)

    if save_pdf:
        fig.savefig("contour_actions_vs_channel_battery.pdf", format='pdf', bbox_inches='tight')
        print("✅ PDF Saved: contour_actions_vs_channel_battery.pdf")

    plt.show()


def plot_action_vs_channel_battery_3d(CH_mean, Battery_mean, AC_user_Mean, slots_list, smooth_span=50, save_pdf=False):
    """
    High-quality 3D plot for Actions vs Channel and Battery across multiple tests.
    """
    num_tests = AC_user_Mean.shape[0]

    for t in range(num_tests):
        # Smooth
        CH_smooth = pd.Series(CH_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Battery_smooth = pd.Series(Battery_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Action_smooth = pd.Series(AC_user_Mean[t]).ewm(span=smooth_span).mean().to_numpy()

        # Grid
        xi = np.linspace(min(CH_smooth), max(CH_smooth), 100)
        yi = np.linspace(min(Battery_smooth), max(Battery_smooth), 100)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = griddata((CH_smooth, Battery_smooth), Action_smooth, (Xi, Yi), method='cubic')

        fig = plt.figure(figsize=(10, 7), dpi=300)
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(Xi, Yi, zi, cmap='viridis', edgecolor='k', linewidth=0.2, antialiased=True)

        ax.set_xlabel("Mean Channel (Smoothed)")
        ax.set_ylabel("Mean Battery (Smoothed)")
        ax.set_zlabel("Mean Actions (Replicas)")
        ax.set_title(f"3D Surface: Actions vs Channel & Battery (Slots={slots_list[t]})")

        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.view_init(elev=30, azim=135)

        if save_pdf:
            fig.savefig(f"3D_surface_actions_slots_{slots_list[t]}.pdf", format='pdf', bbox_inches='tight')
            print(f"✅ PDF Saved: 3D_surface_actions_slots_{slots_list[t]}.pdf")

        plt.show()


def plot_action_vs_channel_battery_3d_subplots(CH_mean, Battery_mean, AC_user_Mean, slots_list, smooth_span=50):
    num_tests = AC_user_Mean.shape[0]
    fig = plt.figure(figsize=(6 * num_tests, 6), dpi=300)

    for t in range(num_tests):
        ax = fig.add_subplot(1, num_tests, t + 1, projection='3d')

        # Smooth
        CH_smooth = pd.Series(CH_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Battery_smooth = pd.Series(Battery_mean[t]).ewm(span=smooth_span).mean().to_numpy()
        Action_smooth = pd.Series(AC_user_Mean[t]).ewm(span=smooth_span).mean().to_numpy()

        # Grid
        xi = np.linspace(min(CH_smooth), max(CH_smooth), 100)
        yi = np.linspace(min(Battery_smooth), max(Battery_smooth), 100)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = griddata((CH_smooth, Battery_smooth), Action_smooth, (Xi, Yi), method='cubic')

        surf = ax.plot_surface(Xi, Yi, zi, cmap='viridis', edgecolor='k', linewidth=0.2, antialiased=True)

        ax.set_xlabel("Mean Channel")
        ax.set_ylabel("Mean Battery")
        ax.set_zlabel("Actions")
        ax.set_title(f"Slots={slots_list[t]}", fontsize=10)
        ax.view_init(elev=30, azim=135)

    fig.suptitle("3D Surface Comparison: Actions vs Channel and Battery", fontsize=16)
    plt.tight_layout()
    plt.show()


def plot_userwise_contours_all_tests(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots_list,
                                     smooth_span=50):
    """
    Plot contour plots for each user showing evolution over multiple tests.
    Plots:
        - Actions vs Channel & Battery
        - Reward vs Channel & Battery
    """
    num_tests, num_frames, num_users = AC_user_tests.shape

    for u in range(num_users):
        print(f"🧩 Plotting User {u}...")

        # -------------- Plot 1: Actions vs Channel & Battery --------------
        fig1, axs1 = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)

        if num_tests == 1:
            axs1 = [axs1]

        for t in range(num_tests):
            ch = pd.Series(CH_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            bt = pd.Series(BT_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            ac = pd.Series(AC_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()

            xi = np.linspace(min(ch), max(ch), 100)
            yi = np.linspace(min(bt), max(bt), 100)
            Xi, Yi = np.meshgrid(xi, yi)

            zi = griddata((ch, bt), ac, (Xi, Yi), method='cubic')

            try:
                zi = griddata((ch, bt), ac, (Xi, Yi), method='cubic')
            except Exception as e:
                print(f"⚠️ Skipping User {u}, Test {t} due to flat input: {e}")
                continue

            cs = axs1[t].contourf(Xi, Yi, zi, levels=20, cmap='viridis')
            fig1.colorbar(cs, ax=axs1[t])
            cs2 = axs1[t].contour(Xi, Yi, zi, levels=10, colors='black', linewidths=0.5)
            axs1[t].clabel(cs2, inline=True, fontsize=8, fmt="%.1f")

            axs1[t].set_xlabel("Channel (Smoothed)")
            axs1[t].set_ylabel("Battery (Smoothed)")
            axs1[t].set_title(f"User {u} | Slots={slots_list[t]}")

        fig1.suptitle(f"User {u}: Actions vs Channel and Battery across Tests", fontsize=16)
        plt.show()

        # -------------- Plot 2: Reward vs Channel & Battery --------------
        fig2, axs2 = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)

        if num_tests == 1:
            axs2 = [axs2]

        for t in range(num_tests):
            ch = pd.Series(CH_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            bt = pd.Series(BT_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            rew = pd.Series(REW_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()

            xi = np.linspace(min(ch), max(ch), 100)
            yi = np.linspace(min(bt), max(bt), 100)
            Xi, Yi = np.meshgrid(xi, yi)

            zi = griddata((ch, bt), rew, (Xi, Yi), method='cubic')

            try:
                zi = griddata((ch, bt), rew, (Xi, Yi), method='cubic')
            except Exception as e:
                print(f"⚠️ Skipping Reward plot for User {u}, Test {t} due to flat input: {e}")
                continue

            cs = axs2[t].contourf(Xi, Yi, zi, levels=20, cmap='plasma')
            fig2.colorbar(cs, ax=axs2[t])
            cs2 = axs2[t].contour(Xi, Yi, zi, levels=10, colors='black', linewidths=0.5)
            axs2[t].clabel(cs2, inline=True, fontsize=8, fmt="%.1f")

            axs2[t].set_xlabel("Channel (Smoothed)")
            axs2[t].set_ylabel("Battery (Smoothed)")
            axs2[t].set_title(f"User {u} | Slots={slots_list[t]}")

        fig2.suptitle(f"User {u}: Reward vs Channel and Battery across Tests", fontsize=16)
        plt.show()


from scipy.stats import binned_statistic_2d

def plot_userwise_density_all_tests(CH_user_tests, BT_user_tests, slots_list, smooth_span=50, bins=100):
    """
    Plot sample density heatmaps for each user across tests.
    Shows how often each (Channel, Battery) combination occurs.
    """
    num_tests, num_frames, num_users = CH_user_tests.shape

    for u in range(num_users):
        print(f"📊 Density Heatmap for User {u}...")

        fig, axs = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)
        if num_tests == 1:
            axs = [axs]

        for t in range(num_tests):
            ch = pd.Series(CH_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            bt = pd.Series(BT_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()

            # Compute 2D histogram / sample density
            stat, x_edge, y_edge, _ = binned_statistic_2d(
                ch, bt, None, statistic='count', bins=bins
            )

            x_centers = 0.5 * (x_edge[:-1] + x_edge[1:])
            y_centers = 0.5 * (y_edge[:-1] + y_edge[1:])
            Xi, Yi = np.meshgrid(x_centers, y_centers)

            cs = axs[t].contourf(Xi, Yi, stat.T, levels=20, cmap='Blues')
            fig.colorbar(cs, ax=axs[t])
            axs[t].set_xlabel("Channel (Smoothed)")
            axs[t].set_ylabel("Battery (Smoothed)")
            axs[t].set_title(f"User {u} | Slots={slots_list[t]}\nSample Density")

        fig.suptitle(f"User {u}: Sample Density across Tests", fontsize=16)
        plt.show()


def plot_userwise_reward_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots_list,
                                          smooth_span=50, bins=100):
    """
    Combined plot: Reward contour (plasma) overlaid with Sample Density heatmap (Blues)
    """
    num_tests, num_frames, num_users = REW_user_tests.shape

    for u in range(num_users):
        print(f"🌀 Reward + Density for User {u}")

        fig, axs = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)
        if num_tests == 1:
            axs = [axs]

        for t in range(num_tests):
            ch = pd.Series(CH_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            bt = pd.Series(BT_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            rew = pd.Series(REW_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()

            # Grid for contour
            xi = np.linspace(min(ch), max(ch), 100)
            yi = np.linspace(min(bt), max(bt), 100)
            Xi, Yi = np.meshgrid(xi, yi)

            try:
                zi = griddata((ch, bt), rew, (Xi, Yi), method='cubic')
            except Exception as e:
                print(f"⚠️ Skipping reward for User {u}, Test {t}: {e}")
                continue

            # Reward contours
            cs = axs[t].contourf(Xi, Yi, zi, levels=20, cmap='plasma', alpha=0.8)
            fig.colorbar(cs, ax=axs[t], label="Reward")

            # Density overlay
            stat, x_edge, y_edge, _ = binned_statistic_2d(ch, bt, None, statistic='count', bins=bins)
            x_centers = 0.5 * (x_edge[:-1] + x_edge[1:])
            y_centers = 0.5 * (y_edge[:-1] + y_edge[1:])
            Xi_d, Yi_d = np.meshgrid(x_centers, y_centers)
            axs[t].contour(Xi_d, Yi_d, stat.T, levels=10, cmap='Blues', linewidths=0.8)

            axs[t].set_title(f"User {u} | Slots={slots_list[t]}")
            axs[t].set_xlabel("Channel (Smoothed)")
            axs[t].set_ylabel("Battery (Smoothed)")

        fig.suptitle(f"User {u}: Reward + Density Overlay", fontsize=16)
        plt.show()


def plot_userwise_action_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, slots_list,
                                          smooth_span=50, bins=100):
    """
    Combined plot: Action contour (viridis) overlaid with Sample Density heatmap (Blues)
    """
    num_tests, num_frames, num_users = AC_user_tests.shape

    for u in range(num_users):
        print(f"🎯 Action + Density for User {u}")

        fig, axs = plt.subplots(1, num_tests, figsize=(5 * num_tests, 5), constrained_layout=True)
        if num_tests == 1:
            axs = [axs]

        for t in range(num_tests):
            ch = pd.Series(CH_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            bt = pd.Series(BT_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()
            ac = pd.Series(AC_user_tests[t, :, u]).ewm(span=smooth_span).mean().to_numpy()

            xi = np.linspace(min(ch), max(ch), 100)
            yi = np.linspace(min(bt), max(bt), 100)
            Xi, Yi = np.meshgrid(xi, yi)

            try:
                zi = griddata((ch, bt), ac, (Xi, Yi), method='cubic')
            except Exception as e:
                print(f"⚠️ Skipping action for User {u}, Test {t}: {e}")
                continue

            # Action contours
            cs = axs[t].contourf(Xi, Yi, zi, levels=20, cmap='viridis', alpha=0.8)
            fig.colorbar(cs, ax=axs[t], label="Action")

            # Density overlay
            stat, x_edge, y_edge, _ = binned_statistic_2d(ch, bt, None, statistic='count', bins=bins)
            x_centers = 0.5 * (x_edge[:-1] + x_edge[1:])
            y_centers = 0.5 * (y_edge[:-1] + y_edge[1:])
            Xi_d, Yi_d = np.meshgrid(x_centers, y_centers)
            axs[t].contour(Xi_d, Yi_d, stat.T, levels=10, cmap='Blues', linewidths=0.8)

            axs[t].set_title(f"User {u} | Slots={slots_list[t]}")
            axs[t].set_xlabel("Channel (Smoothed)")
            axs[t].set_ylabel("Battery (Smoothed)")

        fig.suptitle(f"User {u}: Action + Density Overlay", fontsize=16)
        plt.show()

## Command to randomly pick values----->>>>> np.random.randint(0, 7, size=(k.size * x.size, a.size), dtype=int)
reward = np.empty((number_of_users, iterations+1), dtype=float)
AOI = np.zeros((number_of_users, iterations+1), dtype=int)

#discount_factor = 0.9
#learning_rate = 0.001
# step_size_ep= (1-0.4)/iterations

users = []
for i in range(number_of_users):  # popola il vettore degli utenti
    # users[i] = i + 1
    users.append(User(id=i, mu=upsilon, initial_battery_level=0.05))  # inizializza ogni utente con un livello di batteria di 0.005

q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=float)
for user in range(np.size(users)):
    q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
#print(f"first Q Table {q_tables}")

AOI_users = np.empty((iterations*test, number_of_users), dtype=int)
#print(q_tables)
# print(f"All State matrix {S}")
G = np.empty(test, dtype = float)

AC_user_Mean = np.empty((test, iterations), dtype=float)
CH_mean = np.empty((test, iterations), dtype=float)
Battery_mean = np.empty((test, iterations), dtype=float)
Rew_u_mean =np.empty((test, iterations), dtype=float)
AC_user_tests = np.empty((test, iterations, number_of_users), dtype=float)
CH_user_tests = np.empty((test, iterations, number_of_users), dtype=float)
BT_user_tests = np.empty((test, iterations, number_of_users), dtype=float)
REW_user_tests = np.empty((test, iterations, number_of_users), dtype=float)

for t in range(1, test+1):
    min_epsilon = 0.1
    max_epsilon = 0.6
    Battery_f = np.empty((iterations, number_of_users), dtype=float)  # To save state of all users in current frame
    Ch_f = np.empty((iterations, number_of_users), dtype=float)
    AC_user_f = np.empty((iterations, number_of_users), dtype=int)
    Rew_u_f = np.empty((iterations, number_of_users), dtype=float)
    #q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=float)
    #for user in range(np.size(users)):
     #   q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
    for it_ind in range(0, iterations):
        #print(f"Iteration: {it_ind}")
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * it_ind)
        epsilon = round(epsilon, 5)
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
        #Calculate the channel and update battery for current frame
        #for u in range (np.size(users)):

            #EH_Raw [u] = compute_energy_harvested(G_Raw, time_duration, p)
            #users[u] =
        for d in range (np.size(users)):
            CH_Raw[d] = generate_rician_fading(K_factor)
            users[d].channel = CH_Raw[d]
            G_Raw[d] = gamma_EH(CH_Raw[d], dist_min, dist_max)
            BT_Dis[d] = users[d].BT_units()
            CH_Dis [d] = get_channel(G_Raw[d])
            randx = np.random.random()
            randx = round(randx, 5)
            if randx >= epsilon: #Random Action Selection
                explore += 1
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
                    BT_Dis[d] = users[d].BT_units()
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
                    ind_u = rd.sample(range(number_of_slots), action)
                    slot_aloc_f[d , ind_u] = 1
                    users[d].decrease_EH(action) #update battery
                    BT_Dis[d] = users[d].BT_units()
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
                u = rd.randint(0, number_of_users - 1)
                # for u in range(number_of_users):
                #    if u == user_to_transmit:
                pw_u = compute_energy_harvested(G_Raw[u], time_duration, p)
                users[u].add_EH(pw_u)
                BT_Dis[u] = users[u].BT_units()

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
                users[u].AOI = Recovery - Tx_slot + 1
            Af_aoi[u] = users[u].AOI
            Rew_U [u] = get_rew (Bf_aoi [u], Af_aoi[u] , BT_Dis[u] , AC_users[u], CH_Dis[u])
            #print(f"user {u} AOI is {users[u].AOI}")
            #print(f"user {u} BT is {users[u].battery_level}")
            #print(f"user {u} REW is {Rew_U [u]}")

        AOI_users [t*it_ind, :] = Af_aoi

        if (it_ind + 1) % Batch_size == 0:
            # Get new State and update Q-Table
            BT_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
            CH_Raw_next = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
            CH_Dis_next = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
            G_Raw_next = np.empty(number_of_users, dtype=float)  # to save Gamma of current frame
            for u in range(number_of_users):
                CH_Raw_next[u] = generate_rician_fading(K_factor)
                users[u].channel = CH_Raw_next[u]
                G_Raw_next[u] = gamma_EH(CH_Raw_next[u], dist_min, dist_max)
                BT_Dis_next[u] = users[u].BT_units()
                CH_Dis_next[u] = get_channel(G_Raw[u])
                row_act = get_row(BT_Dis_next[u], CH_Dis_next[u])
                best_next_action_value = q_tables[u][row_act][:].max()
                temporal_difference = Rew_U[u] + discount_factor * best_next_action_value - q_tables[u, row_act, AC_users[u]]
                q_tables[u, row_act, AC_users[u]] += learning_rate * temporal_difference

        #Collect Data
        AC_user_f [it_ind, :] = AC_users
        Ch_f [it_ind, :] = CH_Dis
        Battery_f [it_ind, :] = BT_Dis
        Rew_u_f[it_ind, :] = Rew_U
        # Update AOI using current frame AOI and add it into next frame AOI so that it can be used for next frame
        #Update Next State

    AC_user_tests [t-1, :, :] = AC_user_f
    CH_user_tests [t-1, :, :] = Ch_f
    BT_user_tests [t-1, :, :] = Battery_f
    REW_user_tests [t-1, :, :] = Rew_u_f
    AC_user_Mean [t-1, :] = np.mean(AC_user_f, axis=1)
    CH_mean [t-1, :] = np.mean(Ch_f, axis=1)
    Battery_mean [t-1, :] = np.mean(Battery_f, axis=1)
    Rew_u_mean [t-1, :] = np.mean(Rew_u_f, axis=1)
    G [t-1]= number_of_users / number_of_slots
    number_of_slots -= d_slot
    #number_of_users += 1
    print(f"Test {t} Finished")

#print(f"Last Q Table {q_tables}")

AOI_mean  = np.mean(AOI_users, axis=1)

import matplotlib.pyplot as plt

xv = np.linspace(0, AOI_mean.shape[0] - 1, AOI_mean.shape[0])
fig, ax = plt.subplots(1, 1)
ax.plot(xv, pd.Series(AOI_mean).ewm(span=100).mean(), 'b-', lw=1, alpha=1, label=f'Average AoI S= {number_of_slots}, U = {number_of_users}')  # AoI medio del sistema per ogni iterazione
#ax.plot(xv, np.mean(AAOI_all[1, :, :], axis=0), 'k--', lw=1, alpha=1, label=f'Average AoI S= {n_slot-14}, U = {number_of_users}')  # AoI medio del sistema per ogni iterazione
#ax.plot(xv, np.mean(AAOI_all[4, :, :], axis=0), 'm*', lw=1, alpha=1, label=f'Average AoI S= {n_slot-28}, U = {number_of_users}')  # AoI medio del sistema per ogni iterazione
# ax.plot(xv, xv, AAOI_all [1, :], 'r--', lw=2, alpha=0.6, label ='AoI per Iteration S= 10, U-2') # AAoI cumulativo normalizzato, calcolato dividendo summ_AAoI per il numero di iterazioni considerate fino a quel punto
ax.set_title('AoI Evolvement vs Iterations')
ax.set_ylabel('Average AoI')
ax.set_xlabel('Iterations')
ax.legend()
plt.tight_layout()
#fig.show()
ax.grid(True)
plt.show()

AOI_test_means = []
G_values = []
current_slots = number_of_slots
for t in range(test):
    start_idx = t * iterations
    end_idx = (t + 1) * iterations

    # Extract AOI block for this test
    aoi_block = AOI_users[start_idx:end_idx, :]  # Shape: (iterations, number_of_users)

    # Mean over users (axis=1), then mean over iterations (axis=0)
    mean_per_iteration = np.mean(aoi_block, axis=1)  # Shape: (iterations,)
    final_mean = np.mean(mean_per_iteration)         # Scalar

    AOI_test_means.append(final_mean)

    current_slots -= 2  # N -= 2 for next test


# Convert to numpy arrays for plotting
AOI_test_means = np.array(AOI_test_means)
G_values = np.array(G_values)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(G, AOI_test_means, marker='o')
plt.xlabel(r"Normalized Channel Gain $G$")
plt.ylabel(r"Average AoI $\bar{A}$")
plt.title("AoI")
plt.grid(True)
plt.tight_layout()
plt.show()

slots = []
for t in range(test):
    slots.append(number_of_slots + d_slot*test - d_slot*t)
#for t in range(test):
 #   plot_action_reward_relations(AC_user_Mean[t, :], CH_mean [t, :], Battery_mean [t, :], Rew_u_mean [t, :], slots, smoothing_span=50)
  #  plot_3d_action_vs_channel_battery(AC_user_Mean [t, :], CH_mean [t, :], Battery_mean [t, :], slots)
   # plot_actions_vs_channel_contour(CH_mean[t, :], AC_user_Mean[t, :], Battery_mean[t, :], slots)
    #plot_reward_vs_actions_contour(AC_user_Mean [t, :], Rew_u_mean [t, :], CH_mean [t, :], slots)
    #slots -=2

#plot_reward_vs_actions_contour_all_tests (AC_user_Mean, Rew_u_mean, CH_mean, slots)

#plot_action_vs_channel_battery_all_tests(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50)

#plot_action_vs_channel_battery_contour_highres(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50, save_pdf=True)

#plot_action_vs_channel_battery_3d(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50, save_pdf=True)

#plot_action_vs_channel_battery_3d_subplots(CH_mean, Battery_mean, AC_user_Mean, slots, smooth_span=50)

#plot_userwise_contours_all_tests(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots, smooth_span=50)

plot_userwise_density_all_tests(CH_user_tests, BT_user_tests, slots, smooth_span=50, bins=100)


plot_userwise_reward_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, REW_user_tests, slots,
                                          smooth_span=50, bins=100)

plot_userwise_action_density_combined(AC_user_tests, CH_user_tests, BT_user_tests, slots,
                                          smooth_span=50, bins=100)


print (f"Explore: {explore}")
print (f"Exploit: {exploit}")