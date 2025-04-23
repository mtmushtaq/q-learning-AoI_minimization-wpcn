

def track_aoi_AFSIC(user, recovered, current_slot, last_recovered_slot):
    if recovered:
        # Use the formula: Rn(i) - Tn(i) + 1
        # Rn(i) = last_recovered_slot, Tn(i) = current_slot
        recovery_slot[user] = current_slot  # Update the recovery slot for the user
        return recovery_slot[user] - current_slot + 1  # AoI update when the user is recovered
    else:
        # If not recovered, simply increment AoI by 1
        return user_AoI[user] + 1

#def update_aoi_AFSIC(user, recovered, current_slot, last_recovered_slot):