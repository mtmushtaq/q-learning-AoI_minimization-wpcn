import math


# User class definition
class User:

    def __init__(self, id: int, mu=0.005, initial_battery_level=0.005, max_bat = 0.005, AOI = 1):
        self.id = id
        self.mu = mu
        self.battery_level = initial_battery_level
        self.transmission_slots = {}
        self.channel = 0
        self.AOI = AOI
        self.max_bat = max_bat

    def add_EH(self, pw_u) -> None:
        self.battery_level += pw_u
        if self.battery_level > self.max_bat:
             self.battery_level = self.max_bat

    def AOI (self) -> int:
        return self.AOI

    def get_battery_level(self) -> float:
        return self.battery_level


    def decrease_EH(self, action) -> None:
       # pw_u = action * self.mu
        self.battery_level -= action

    def decrease_EH_cont(self, Bt_sp) -> None:
       # pw_u = action * self.mu
        self.battery_level -= Bt_sp
        if self.battery_level > self.max_bat:
             self.battery_level = self.max_bat

    def return_id(self) -> int:
        return self.id

    def BT_units(self, batter_bins) -> int:
        units = math.floor(self.battery_level / self.mu) # compute the number of packets that can be transmitted
        if units > batter_bins:
            units = batter_bins # our user can max save 5 units of battery, extra battery is overflow which cannot be saved
        return units

    def channel (self, channel) -> complex:
        self.channel = channel
        return self.channel

    def set_transmission_slots(self, frame, transmitting_slots):
        self.transmission_slots[frame] = transmitting_slots.tolist()

    def get_transmission_slots(self, frame):
        return self.transmission_slots[frame]

    def get_transmission_slots_dict(self):
        return self.transmission_slots