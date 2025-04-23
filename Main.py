#import sys

#from typing import Any
import random as rd
import numpy as np
from numpy import ndarray, dtype
from State_User import * #generate_rician_fading, gamma_EH, compute_energy_harvested
from Discritize_state import get_dis_BT, get_dis_AT, CH_dist
from SIC import *
from User import User
import pandas as pd
from pandas import DataFrame

# This code with an optimized Learning rate= 0.5, But we need to find the value of Epsilon for good convergence
# define training parameters
discount_factor = 0.99  # 0.001
test = 0
learning_rate = 0.0001
#define system parameters
mu_bu= 0.05 # one unit of battery
number_of_slots = 3
number_of_users = 10
time_duration = 0.01
p= 4.6
dist_min = 1
dist_max = 10
s_AAOI = []
Gain = []
Th= 0.2
iterations = 10
Frame_size = []
STD_AoI_u_AT = []
STD_AoI_u_BT = []

#u = np.empty(number_of_users, dtype=object)  # define users array
#for i in range(number_of_users):
 #   u[i] = i + 1
# q_tables = np.zeros (k.size * x.size, a.size)
k = np.array([0, 1, 2, 3, 4, 5])  # possible power values
x = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # channel quality information
a = np.array([0, 1, 2, 3, 4])

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

def get_rew(act):
    rew = 0
    if act == 0:
        rew= -5
    elif action == 1:
        rew = 5
    elif action == 2:
        rew = 7
    elif action == 3:
        rew = 9
    return rew


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
## Command to randomly pick values----->>>>> np.random.randint(0, 7, size=(k.size * x.size, a.size), dtype=int)
reward = np.empty((number_of_users, iterations+1), dtype=float)
AOI = np.zeros((number_of_users, iterations+1), dtype=int)
it_ind = 0
explore = 0
exploit = 0
K_factor =  10
#discount_factor = 0.9
#learning_rate = 0.001
# step_size_ep= (1-0.4)/iterations
min_epsilon = 0.1
max_epsilon = 0.7
decay_rate = 0.0001
upsilon = 0.05 # One unit to transmit one replica
users = []
for i in range(number_of_users):  # popola il vettore degli utenti
    # users[i] = i + 1
    users.append(User(id=i, mu=upsilon, initial_battery_level=0.05))  # inizializza ogni utente con un livello di batteria di 0.005

q_tables = np.empty([number_of_users, k.size * x.size, a.size], dtype=float)
for user in range(np.size(users)):
    q_tables[user, :, :] = np.random.rand(k.size * x.size, a.size)
print(q_tables)

#print(q_tables)
# print(f"All State matrix {S}")
for it_ind in range(0, iterations):
    print(f"Iteration: {it_ind}")
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * it_ind)
    epsilon = round(epsilon, 5)
    slot_aloc_f = np.zeros ((np.size(users), number_of_slots), dtype=int)
    S = np.empty((number_of_users, 1, 2), dtype=float)  # To save state of all users in current frame
    EH_Raw = np.empty(number_of_users, dtype=float)  # to save raw battery capacity of all users at current iteration/frame
    #EH_Raw[:, 0] = EH_Raw[:, 0] + 0.05
    BT_Dis = np.empty(number_of_users, dtype=int)  # to save discrete battery capacity of all users at current iteration/frame
    CH_Raw = np.empty(number_of_users, dtype=complex)  # to save raw channel gamma of all users at current iteration/frame
    CH_Dis = np.empty(number_of_users, dtype=int)  # to save discrete channel gamma of all users at current iteration/frame
    G_Raw = np.empty(number_of_users, dtype=float)
    #Calculate the channel and update battery for current frame
    #for u in range (np.size(users)):

        #EH_Raw [u] = compute_energy_harvested(G_Raw, time_duration, p)
        #users[u] =
    for d in range (np.size(users)):
        CH_Raw[d] = generate_rician_fading(K_factor)
        users[d].channel = CH_Raw[d]
        G_Raw[d] = gamma_EH(CH_Raw[d], dist_min, dist_max)
        BT_Dis[d] = users[d].BT_units()
        CH_Dis [d] = get_channel(CH_Raw[d])
        randx = np.random.random()
        randx = round(randx, 5)
        if randx >= epsilon: #Random Action Selection
            explore += 1
            bt_units = users[d].BT_units()
            prob_dist = get_distr(bt_units)
            if bt_units == 0:
                slot_aloc_f [d,:] = np.zeros ((1, number_of_slots), dtype=int)
                #print(f"Random Action of User {d} is {0}")
            else:
                range_slot = np.array(range(0, number_of_slots), dtype=int) # to ask it to make a choice between first and last slot
                range_action = np.array(range(1, len(prob_dist)+1), dtype=int) # to choose an action between 1 and max_battery unit with prob_dist
                user_action = np.random.choice(range_action, size=1, p=prob_dist) # choose an action based on prob_dist
                slot_indices = np.random.choice(range_slot, size=user_action, replace=False) #choose random slots to send the packet
                slot_aloc_f[d, slot_indices] = 1  #Make selected slots 1 for user's row
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
                ind_u = rd.sample(range(number_of_slots), action)
                slot_aloc_f[d , ind_u] = 1
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
    # apply SIC
    decoded_users = capture_effect_SIC_realtime(slot_aloc_f, number_of_slots, number_of_users, G_Raw, verbose=True)
    #Successive_IC (u.size, slot_aloc_f, number_of_slots ) # Rearly-n method
    Bf_aoi = np.ones(number_of_users, dtype=int) #Before update
    for u in range(number_of_users):
        Bf_aoi [u] = users[u].AOI
        Recovery = decoded_users [u, 0]
        Tx_slot = decoded_users [u, 1]
        if Tx_slot == -1 or Recovery == -1:
            users[u].AOI = Bf_aoi [u] + number_of_slots
        else:
            users[u].AOI = Recovery - Tx_slot + 1
        print(f"user {u} AOI is {users[u].AOI}")
    # Update AOI using current frame AOI and add it into next frame AOI so that it can be used for next frame
    #Update Next State
