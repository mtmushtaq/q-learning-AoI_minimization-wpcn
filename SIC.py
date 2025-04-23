import numpy as np


def capture_effect_SIC_realtime(slot_aloc_f, number_of_slots, number_of_users, G_raw, verbose=True):
    slot_aloc_f = slot_aloc_f.copy()
    slot_aloc_ff = slot_aloc_f.copy()
    # Initialize: column 0 = decoding slot, column 1 = first transmission slot
    decoded_users = -1 * np.ones((number_of_users, 2), dtype=int)

    # Fill column 1 with the first slot where each user transmitted
    for u in range(number_of_users):
        user_slots = np.where(slot_aloc_f[u, :] == 1)[0]
        if len(user_slots) > 0:
            decoded_users[u, 1] = user_slots[0]  # first transmission slot

    received_slots = set()

    for current_slot in range(number_of_slots):
        received_slots.add(current_slot)

        #if verbose:
         #   print(f"\n--- Slot {current_slot} Received ---")

        # Step 1: Try Capture Effect ONCE on this slot
        users_in_slot = np.where(slot_aloc_f[:, current_slot] == 1)[0]
        users_in_slot = [u for u in users_in_slot if decoded_users[u, 0] == -1]

        if users_in_slot:
            G_values = G_raw[users_in_slot]
            max_idx = np.argmax(G_values)
            max_user = users_in_slot[max_idx]
            max_value = G_values[max_idx]
            sum_others = np.sum(G_values) - max_value

            if max_value > sum_others:
                decoded_users[max_user, 0] = current_slot
                slot_aloc_f[max_user, :] = 0
                #if verbose:
                 #   print(f"[Capture Effect] User {max_user} decoded in Slot {current_slot}")

        # Step 2: Apply SIC across all received slots iteratively
        while True:
            progress = False
            slot_sums = np.sum(slot_aloc_f[:, list(received_slots)], axis=0)
            singleton_slots = np.where(slot_sums == 1)[0]

            for local_idx in singleton_slots:
                slot = list(received_slots)[local_idx]
                user = np.where(slot_aloc_f[:, slot] == 1)[0][0]
                if np.size(user) == 0:
                    continue  # No user transmitting in this slot, skip
                if decoded_users[user, 0] == -1:
                    decoded_users[user, 0] = current_slot
                    slot_aloc_f[user, :] = 0
                    #if verbose:
                     #   print(
                      #      f"[SIC] User {user} decoded via singleton in Slot {slot} (marked as recovered at Slot {current_slot})")
                    progress = True

            if not progress:
                break

    # Step 3: Post-processing for unresolved users
    for u in range(number_of_users):
        if decoded_users[u, 0] == -1 and np.any(slot_aloc_f[u, :] == 1):
            decoded_users[u, 0] = number_of_slots - 1
            #if verbose:
             #   print(
              #      f"[Unresolved] User {u} not decoded, marked as recovered at end of frame (Slot {number_of_slots - 1})")

    #if verbose:
     #   print("\nFinal Decoding Result:")
      #  for u in range(number_of_users):
       #     print(f"User {u}: Decoded Slot = {decoded_users[u, 0]}, First Replica Slot = {decoded_users[u, 1]}")

    return decoded_users
