import numpy as np
#import scipy as sp
#from scipy.linalg import pinv
beta_h = 10
#p= 46
alpha0 = 0.826
alpha1 = 0.399
#time_duration = 0.5

def generate_rician_fading(K_r):
    LOS_component = np.sqrt(K_r / (1 + K_r))  # Line-of-sight component
    scattered_component = np.sqrt(1 / (1 + K_r))   # Scattered component
    h = LOS_component + scattered_component * (np.random.normal(0, 1) + 1j * np.random.normal(0, 1))  # Total channel gain
    return h  # |h|^2 Power Gain


def gamma_EH(channel, d): #dist_l, dist_h):  # we utilize different distance for desired user and interference user since intereference will be coming from more than 30 meter from another cluster
    w = np.conjugate (channel) #precoding matrix
    #d = np.random.uniform(dist_l, dist_h)
    gamma_h = (np.abs ((np.sqrt(beta_h * d ** -2) * (w * channel)) ))** 2
    return gamma_h

def compute_energy_harvested(g_eh, time_duration, p):  # EQ 5
    eh = (alpha0 * p * time_duration * g_eh) / (alpha1 * p * g_eh + alpha1)  # Pass dist_l and dist_h
    return eh

def get_channel(ce):  # valuta un dato valore ce (channel evaluation) e ritorna il corrispondente grado del canale (ch) basato su un range predefinito
    #print(f"channel evaluation: {ce}:")
    if ce < 0.0025:
        ch = 0  # grado del canale
        return ch
    elif ce >= 0.0025 and ce < 0.005:
        ch = 1
        return ch
    elif ce >= 0.005 and ce < 0.07:
        ch = 2
        return ch
    elif ce >= 0.07 and ce < 0.1:
        ch = 3
        return ch
    elif ce >= 0.1 and ce < 0.5:
        ch = 4
        return ch
    elif ce >= 0.5 and ce < 1:
        ch = 5
        return ch
    elif ce >= 1 and ce < 1.75:
        ch = 6
        return ch
    else:
        ch = 7
        return ch
