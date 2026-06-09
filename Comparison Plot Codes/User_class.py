import numpy as np


class Irsa_IL:
    def __init__(self, discount_factor, frames=10, epsilon=1):
        discount_factor = 0.99  # 0.001
        number_of_slots = 2
        number_of_users = 2

    def linear_decay(self, step):
        return max(0, self.epsilon - self.decay_rate * step)
