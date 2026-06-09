import numpy as np

beta_h = 0.5
p = 46
alpha0 = 0.826
alpha1 = 0.399
time_duration = 0.5
#def generate_rician_fading(K_r):



def gamma_EH(K_r):  # we utilize different distance for desired user and interference user since intereference will be coming from more than 30 meter from another cluster
	LOS_component = np.sqrt(K_r / (1 + K_r))  # Line-of-sight component
	scattered_component = np.sqrt(1 / (1 + K_r))  # Scattered component
	h = LOS_component + scattered_component ** (np.random.normal(0, 1) + 1j * np.random.normal(0, 1))  # Total channel gain

	w = np.conjugate(h)  # precoding matrix
	d = np.random.uniform(1, 10)
	gamma_h = (np.abs((np.sqrt(beta_h * d ** -2) * (w * h)))) ** 2
	return gamma_h


def compute_energy_harvested(g_eh):  # EQ 5
	eh = (alpha0 * p * time_duration * g_eh) / (alpha1 * p * g_eh + alpha1)  # Pass dist_l and dist_h
	return eh



class User:
	def __init__(self, id, initial_battery_level=0):
		self.id = id
		self.battery_level = initial_battery_level

	def add_EH(self):
		return