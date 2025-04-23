#!/usr/bin/env python
# coding: utf-8
import numpy as np
import random
import pandas as pd
import math
import matplotlib.pyplot as plt
import logging
from State import *

# This code with an optimized Learning rate= 0.5, But we need to find the valued of Epsilon for good convergence
# define training parameters
discount_factor = 0.9  # 0.001
number_of_slots = 30
number_of_users = 20
s_AAOI = []
Gain = []
Frame_size = []
STD_AoI_u_AT = []  # STD Age of Information After Training
STD_AoI_u_BT = []  # STD Age of Information Before Training
test = 0
test_max = 3
global  explore   # quante volte l'algoritmo decide di esplorare (scoprire nuove informazioni)
global  exploit
AAoI_global = np.zeros(test_max)  # array per memorizzare l'AAoI del sistema per ogni test
iterations = 100000
AAOI_all = np.empty((test_max, iterations), dtype=float)
while test < test_max:
    # SET PARAMETERS
    learning_rate = 0.0001
    u = np.empty(number_of_users, dtype=object)  # define users array

    for i in range(number_of_users):  # popola il vettore degli utenti
        u[i] = i + 1

    k = np.array([0, 1, 2, 3, 4, 5])  # possible power values
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7])  # channel quality information
    # SET EH PARAMETERS (Energy Harvesting)
    beta_ch = 10  # massimo numero di pacchetti trasmessi da un utente
    alpha0 = 0.339  # learing rate factor
    alpha1 = 0.826  # learning rate factor
    p = 46
    delta = 0.5

    k_factor = 5  # energia consumata per inviare un pacchetto
    meank = np.sqrt(k_factor / (2 * (1 + k_factor)))  # media della distribuzione di k
    varK = np.sqrt(1 / (2 * (1 + k_factor)))  # deviazione standard delle componenti casuali nella distribuzione k

    # max = 0.9
    # min_e = 0.1
    # decay_rate = 1/iterations

    # Create STATE array

    S = np.empty((u.size, k.size, x.size), dtype=object)  # array tridimensionale
    for i in range(u.size):  # itera per ogni utente
        for j in range(k.size):  # itera per ogni possibile valore di energia
            for l in range(x.size):  # itera per ogni informazione della qualità di canale
                S[i][j][l] = [j, l]  # ad ogni elemento viene assagnato una lista con i valori [valore energia,informazione qualità del canale]

    # Definte possible actions : possible number of replicas sent by each device which depends on power levels

    a = np.array([0, 1, 2, 3, 4, 5])  # array delle azioni

    state_space_size = (6, 8)  # 6 livelli di potenza e 8 livelli di qualità del canale
    action_space = [0, 1, 2, 3, 4, 5]  # azioni disponibili per un singolo dispositivo

    # Q-Table globale
    q_table = np.random.uniform(0, 7, size=(number_of_users, k.size * x.size, a.size))


    # print(f"Global Q-table: {q_table.shape()}")

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
    # funzione per convertire stati in indici globali
    def state_to_index(states):
        index = []  # lista di indici
        for user_state in states:
            pw, ch = user_state
            index.append(pw * state_space_size[1] + ch)
        return index


    # funzione per convertire azioni in indici globali
    def action_to_index(actions):
        index = 0
        for action in actions:
            index = index * len(action_space) + action
        return index


    # funzione per calcolare una ricompensa globale basata sull'azione e lo stato
    def compute_reward(prev_AoI, curr_AoI, action):
        if action == 0:
            return 0  # Penalizza per inattività
        elif curr_AoI < prev_AoI:
            return 5  # Premia la riduzione dell'AoI
        elif curr_AoI == prev_AoI:
            return 1  # Ricompensa più bassa se AoI rimane invariato
        else:
            return -5  # Penalizza l'aumento dell'AoI


    explore = 0
    exploit = 0


    # funzione per la epsilon-greedy policy

    def get_distr(pw):
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


    def epsilon_greedy_policy(rows_u, epsilon, d_p, explore, exploit):
        # Exploration
        randx = round(np.random.random(), 5)
        if randx >= epsilon:
            explore += 1
            joint_action = []
            for ij in range(number_of_users):
                if d_p[ij] == 0:
                    joint_action.append(0)
                else:
                    jj=get_distr(d_p[ij])
                    kk= np.array(range(1, len(jj) + 1), dtype=int)
                    rc= np.random.choice(kk, size=1, p=jj)
                    joint_action.append(rc)
            return joint_action
        # Exploitation
        else:
            exploit += 1
            joint_action = []
            for user in range(number_of_users):
                # print(f"Dim Q-table: {q_table.shape}")
                # print(f"Current State Index :{state_index[user]} ")
                joint_action_index = np.argmax(q_table[user, int(rows_u[user]), :])  # trova l'indice dell'azione congiunta con il valore Q massimo
                # converti l'indice dell'azione congiunta in una lista di azioni
                joint_action.append(joint_action_index)
            return joint_action

            # 5) DEF. GET POWER METHOD (get remaining power int. units 'pw' from remaining energy 're')


    def get_power(re):  # associa un valore di potenza discreto (pw) a un intervallo continuo di en.rimanente (re)
        if re < 0.01:
            pw = 0
            return pw
        elif re >= 0.01 and re < 0.02:
            pw = 1
            return pw
        elif re >= 0.02 and re < 0.03:
            pw = 2
            return pw
        elif re >= 0.03 and re < 0.04:
            pw = 3
            return pw
        elif re >= 0.04 and re < 0.05:
            pw = 4
            return pw
        else:
            pw = 5
            return pw


    # Get probability distribution 'distr' from remaining pw units
    def get_distr(pw):  # genera la distribuzione di probabilità basata sul valore pw
        if pw == 1:  # solo un valore è possibile
            distr = np.array([1])  # quindi distr = [1]
            return distr
        elif pw == 2:  # abbiamo 2 valori
            distr = np.array([0.75, 0.25])  # distribuzione su due valori
            return distr
        elif pw == 3:
            distr = np.array([0.7, 0.2, 0.1])
            return distr
        elif pw == 4:
            distr = np.array([0.625, 0.2083, 0.1042, 0.0625])
            return distr
        elif pw == 5:
            distr = np.array([0.2, 0.2, 0.3, 0.2, 0.1])
            return distr

        # 4) DEF. GET COLUMN METHOD (get channel grade 'ch' from channel evaluation 'ce')


    def get_channel(ce):  # valuta un dato valore ce (channel evaluation) e ritorna il corrispondente grado del canale (ch) basato su un range predefinito
        if ce < 0.25:
            ch = 0  # grado del canale
            return ch
        elif ce >= 0.25 and ce < 0.5:
            ch = 1
            return ch
        elif ce >= 0.5 and ce < 0.75:
            ch = 2
            return ch
        elif ce >= 0.75 and ce < 1:
            ch = 3
            return ch
        elif ce >= 1 and ce < 1.25:
            ch = 4
            return ch
        elif ce >= 1.25 and ce < 1.5:
            ch = 5
            return ch
        elif ce >= 1.5 and ce < 1.75:
            ch = 6
            return ch
        else:
            ch = 7
            return ch


    # Packet losing probability method
    def get_losing_prob(channel_grade):
        if channel_grade == 0:
            l_prob = 0  # probabilità di perdere il pacchetto
            return l_prob  # il fatto che ritorni sempre 0 fa la ridondanza logica
        elif channel_grade == 1:
            l_prob = 0
            return l_prob
        elif channel_grade == 2:
            l_prob = 0
            return l_prob
        elif channel_grade == 3:
            l_prob = 0
            return l_prob
        elif channel_grade == 4:
            l_prob = 0
            return l_prob
        elif channel_grade == 5:
            l_prob = 0
            return l_prob
        elif channel_grade == 6:
            l_prob = 0
            return l_prob
        elif channel_grade == 7:
            l_prob = 0
            return l_prob


    # print(q_tables)
    # q_tab_init= q_tables #definiamo la variabile q_tab_init al valore della q_tables

    # Arrays useful to update q-tables
    rows = np.empty(u.size, dtype=object)  # array delle righe della dimensione del numero di utenti
    values = np.empty(u.size, dtype=object)  # array dei valori della dimensione del numero di utenti
    actions = np.empty(u.size, dtype=object)  # array delle azioni della dimensione del numero di utenti

    # Other useful arrays
    final_AoI_BT = np.zeros(iterations, dtype=object)  # AoI end frame (age of information) before training
    final_AoI_AT = np.zeros(iterations, dtype=object)  # AoI end frame (age of information) after training
    remaining_powers = np.empty(u.size, dtype=object)  # array energia rimasta della dimensione del numero di utenti
    n_of_is = np.empty(iterations, dtype=object)  # n of idle slots (slot inattivi)
    transmission_slot = np.zeros(u.size, dtype=object)  # slot di trasmissione

    rp_ind = 0  # remaining powers index
    for rp in remaining_powers:  # per ogni indice di energia rimanente nell'array dell'energia rimasta
        remaining_powers[rp_ind] = 0.005  # setto a 0.005 l'indice di energia rimanente per tutti
        rp_ind += 1

        # We evaluate channel for each user
    # z = np.random.normal(meank, varK, size=(u.size, 2)).view(np.complex128) #genera numeri casuali da una #distribuzione normale, np.complex128 converte l'array in numeri complessi
    # dist=np.random.uniform(0.8,2, size=(u.size, 1)) #genera una distanza random tra 0.8 e 2 per ogni utente
    # ch_ev = np.absolute(z) #calcola la magnitudine per ogni valore complesso in z
    # h_cnj = np.conjugate(z) #calcola il complesso coniugato di z
    # sq_p= np.absolute(np.sqrt(beta_ch* (1/dist**2))*(h_cnj*z))**2  # Gamma
    # eh = (alpha0*p*delta*sq_p)/(alpha1*p*sq_p+(alpha1)**2) # Equation (7)

    # epsilon = 1
    # batch = 0
    # while batch < 29: #Only one batch with constant epsilon
    # Indipendent Learner algorithm

    it_ind = 0  # iteration index
    total_AoI = 0  # Inizializza AoI totale
    min_epsilon = 0.01  # minimo per l'epsilon-greedy exploration
    max_epsilon = 0.9  # massimo per l'epsilon-greedy exploration
    decay_rate = 0.0001  # tasso di decadimento di epsilon nelle iterazioni
    #epsilon = max_epsilon  # inizializzo epsilon al suo valore
    curr_AoI = np.zeros(u.size)
    for iteration in range(iterations):
        # 1. Aggiorna epsilon per ridurre l'esplorazione nel tempo
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * iteration)
        epsilon = round(epsilon, 5)

        decoding_table = np.zeros(shape=(u.size, number_of_slots))
        rewards = np.zeros(shape=u.size)
        total_reward = 0

        # Stato iniziale casuale per tutti i dispositivi
        ce_u = np.zeros(u.size)
        pw_u = np.zeros(u.size)
        di_ce = np.zeros(u.size)
        di_pw = np.zeros(u.size)
        rows_u = np.zeros(u.size)
        for n in range(number_of_users):
            ce_u[n] = gamma_EH(k_factor)
            di_ce[n] = get_channel(ce_u[n])
            pw_u[n] = compute_energy_harvested(ce_u[n])
            di_pw[n] = get_power(di_ce[n])
            rows_u[n] = int(get_row(di_pw[n], di_ce[n]))

        # print(f"joint state: {joint_state}")
        # state_index = state_to_index(joint_state)
        # print(f"State index: {state_index}")

        # Inizializza la riga nella tabella Q se lo stato non esiste
        # if state_index not in q_table:
        # q_table[state_index] = np.zeros(len(action_space) ** number_of_users)

        # Seleziona un'azione congiunta usando epsilon-greedy
        joint_action = epsilon_greedy_policy(rows_u, epsilon, di_pw, explore, exploit)
        action_index = action_to_index(joint_action)
        # print(f"Action index : {action_index}")

        # Simula la ricompensa e lo stato successivo
        prev_AoI = curr_AoI.copy()  # Memorizza l'AoI della precedente iterazione
        # Calcola il nuovo AoI basato sulle azioni selezionate
        curr_AoI = np.zeros(u.size)  # Reset dell'AoI per questa iterazione

        # DECODING TABLE PER CAPIRE L'UTENTE IN QUALE SLOT HA INVIATO I SUOI PACCHETTI
        for user in range(number_of_users):
            action = joint_action[user]  # Prendiamo l'azione per ogni utente (numero di pacchetti da trasmettere)
            if action >= number_of_slots:
                action = number_of_slots - 1
            index = np.random.choice(np.arange(number_of_slots), size=action, replace=False)  # Scegliamo randomicamente lo slot in cui trasmettere ogni pacchetto
            #print(user, index)
            decoding_table[user, index] = 1  # Segnamo con 1 gli slot in cui l'utente ha trasmesso
        # print(f"Joint Action {joint_action}")
        # print(f"Decoding table: {decoding_table}")

        # DECODING TABLE CON COLLISIONI SEGNALATE
        T = np.full(u.size, -1)  # Ogni elemento rappresenta lo slot in cui l'utente ha trasmesso il primo pacchetto
        R = np.full(u.size, -1)  # Ogni elemento rappresenta lo slot in cui viene decodificato il pacchetto dell'utente
        for slot in range(number_of_slots):
            # print(f"Decoding table step {slot} : \n {decoding_table} ")
            if (decoding_table[:, slot].sum() > 1):
                transmission_users = np.where(decoding_table[:, slot] == [1])[0]  # elemento della colonna pari a 1 -> indice degli utenti che hanno inviato il pacchetto
                for t_u in transmission_users:
                    if T[t_u] == -1:
                        T[t_u] = slot

            elif (decoding_table[:, slot].sum() == 1):
                recovery_users = np.where(decoding_table[:, slot] == [1])[0]  # elemento della colonna pari a 1 -> indice dell'utente che ha inviato con successo il pacchetto
                # print(f"Recovery users:{recovery_users}")
                for r_u in recovery_users:
                    R[r_u] = slot
                    if T[r_u] == -1:
                        T[r_u] = slot

                decoding_table[recovery_users[0],
                :] = 0  # pongo la riga dell'utente che è risucito a decodificare il pacchetto a 0
        for user in range(number_of_users):
            if (R[user] == -1):
                curr_AoI[user] = prev_AoI[user] + 1

            else:
                curr_AoI[user] = R[user] - T[user] + 1

        # print(f"Transmission : {T}")
        # print(f"Recovery : {R}")
        # print(f"Prev AoI: {prev_AoI}")
        # print(f"Current AoI: {curr_AoI}")
        # print(f"Decoding table with collision signed : {decoding_table}")

        next_joint_state = [(random.randint(0, state_space_size[0] - 1), random.randint(0, state_space_size[1] - 1)) for
                            _ in range(number_of_users)]
        next_state_index = state_to_index(next_joint_state)
        # print(f"Next state index: {next_state_index}")

        # Calcolo la ricompensa per ogni utente e la ricompensa complessiva (total_reward)
        for user in range(number_of_users):
            rewards[user] = compute_reward(prev_AoI[user], curr_AoI[user],  joint_action[user])  # Usa la funzione di reward

        total_reward = rewards.sum()

        # Inizializza lo stato successivo nella tabella Q se non esiste
        # if next_state_index not in q_table:
        # q_table[next_state_index] = np.zeros(len(action_space) ** number_of_users)

        # Aggiorna la tabella Q usando l'equazione di Bellman
        for user in range(number_of_users):
            #print(user)
            best_next_action_value = np.max(q_table[user, int(rows_u[user]), :])
            temporal_difference = total_reward + discount_factor * best_next_action_value - q_table[user, int(rows_u[user]), joint_action[user]]
            q_table[user, int(rows_u[user]),joint_action[user]] += learning_rate * temporal_difference

        # Memorizza l'AoI totale per il sistema in questa iterazione
        final_AoI_BT[iteration] = (curr_AoI.sum()) / number_of_users  # Media dell'AoI per il sistema
        # print(f"Final AoI: {final_AoI}")


    print(f"learning rate = {learning_rate}, discount factor = {discount_factor}, epsilon = {epsilon}, slots {number_of_slots}, Explore: {explore}, Exploit: {exploit}")  # stampa i principali parametri del modello
    s_AAOI.append(sum(final_AoI_BT) / iterations)
    Gain_t = number_of_users / number_of_slots  # guadagno per iterazione
    Gain.append(Gain_t)  # aggiunge Gain_t alla lista Gain per monitoare l'andamento del guadagno nel tempo
    Frame_size.append(number_of_slots)  # memorizza number_of_slots nella lista Frame_size in modo da tracciare il numero di slot utilizzati in ciascuna iterazione
    # number_of_users += 1
    number_of_slots -= 2  # in questo modo il numero di slot non può essere inferiore ad 1
    AAOI_all [test, :] = final_AoI_BT

    test += 1

# print(f"DIM Gain {len(Gain)}")
# print(f"Len S_AAOI {len(s_AAOI)}")
# print(f"Frame size {Frame_size}")
# print(f"final_AoI {final_AoI}")
# print(f"sAAOI {s_AAOI}")

## Confronto fra Frame Size e Gain in termini di dimensioni e di Tipo Pipio
# Questo grafico visualizza come cambia l'AAoI del sistema in funzione del guadagno, utilizzando i valori nelle liste Frame_size(numero di slot) e s_AAoI (AAOI per ogni guadagno)
fig, ax = plt.subplots(1, 1)
ax.plot(Gain, s_AAOI, 'b-', lw=2, alpha=0.6)
ax.set_title('System AoI comparison at different gains')
ax.set_ylabel('System AoI')
ax.set_xlabel('Gain')
plt.tight_layout()
fig.show()


xv = np.linspace(0, iterations, iterations)
fig, ax = plt.subplots(1, 1)
ax.plot(xv, final_AoI_BT, 'b-', lw=2, alpha=0.6, label='AoI per Iteration')  # AoI medio del sistema per ogni iterazione
# ax.plot(xv, summ_AAoI/iterations, 'r--', lw=2, alpha=0.6, label ='Cumulative AAoI') # AAoI cumulativo normalizzato, calcolato dividendo summ_AAoI per il numero di iterazioni considerate fino a quel punto
ax.set_title('AoI Evolvement vs Iterations')
ax.set_ylabel('System AoI')
ax.set_xlabel('Iterations')
ax.legend()
plt.tight_layout()
fig.show()

xv = np.linspace(0, iterations, iterations)
fig, ax = plt.subplots(1, 1)
ax.plot(xv, AAOI_all [0, :] , 'b-', lw=2, alpha=0.6, label='AoI per Iteration S= 30, U-20')  # AoI medio del sistema per ogni iterazione
ax.plot(xv, AAOI_all [1, :] , 'k--', lw=2, alpha=0.6, label='AoI per Iteration S= 28, U-20')  # AoI medio del sistema per ogni iterazione
ax.plot(xv, AAOI_all [2, :] , 'm*', lw=2, alpha=0.6, label='AoI per Iteration S= 26, U-20')  # AoI medio del sistema per ogni iterazione
#ax.plot(xv, xv, AAOI_all [1, :], 'r--', lw=2, alpha=0.6, label ='AoI per Iteration S= 10, U-2') # AAoI cumulativo normalizzato, calcolato dividendo summ_AAoI per il numero di iterazioni considerate fino a quel punto
ax.set_title('AoI Evolvement vs Iterations')
ax.set_ylabel('System AoI')
ax.set_xlabel('Iterations')
ax.legend()
plt.tight_layout()
fig.show()