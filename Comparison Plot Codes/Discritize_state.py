import numpy as np

def get_dis_BT(B_C_BT, Har_E, mu): # Before Transmission
    B_C_BT= B_C_BT + Har_E
    D_U = np.floor (B_C_BT / mu)
    if D_U > 5:
        D_U = 5
    return D_U, B_C_BT

def get_dis_AT( B_C_BT, act, mu): # After Transmission
    B_C_AT= B_C_BT - act* mu
    return B_C_AT

def CH_dist(ce):
    if ce < 0.25:
        ch = 0
        return ch
    elif ce >= 0.25 and ce < 0.75:
        ch = 1
        return ch
    elif ce >= 0.76 and ce < 1.25:
        ch = 2
        return ch
    elif ce >= 1.76 and ce < 2.25:
        ch = 3
        return ch
    elif ce >= 2.26 and ce < 2.75:
        ch = 4
        return ch
    #elif ce >= 1.25 and ce < 1.5:
     #   ch = 5
      #  return ch
    #elif ce >= 1.5 and ce < 1.75:
     #   ch = 6
      #  return ch
    else:
        ch = 5
        return ch