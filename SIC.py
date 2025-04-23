import numpy as np

def capture_effect_SIC_realtime(slot_aloc_f, number_of_slots, number_of_users, G_raw, verbose=True):
    slot_aloc_f = slot_aloc_f.copy()
    decoded_users = -1 * np.ones((number_of_users, 2), dtype=int)

    for u in range(number_of_users):
        first_slots = np.where(slot_aloc_f[u, :] == 1)[0]
        if len(first_slots) > 0:
            decoded_users[u, 1] = first_slots[0]

    received_slots = []

    for current_slot in range(number_of_slots):
        received_slots.append(current_slot)
        decoded_this_round = []

        if verbose:
            print(f"\n--- Slot {current_slot} Received ---")

        # === Step 1: Try Capture Effect on current slot ===
        users_in_slot = np.where(slot_aloc_f[:, current_slot] == 1)[0]
        undecoded_users = [u for u in users_in_slot if decoded_users[u, 0] == -1]

        if len(undecoded_users) > 0:
            G_vals = G_raw[undecoded_users]
            max_idx = np.argmax(G_vals)
            max_user = undecoded_users[max_idx]
            max_val = G_vals[max_idx]
            sum_others = np.sum(G_vals) - max_val

            if max_val > sum_others:
                # Capture effect succeeded
                decoded_users[max_user, 0] = current_slot
                decoded_this_round.append(max_user)
                slot_aloc_f[max_user, :] = 0
                if verbose:
                    print(f"[Capture Effect] User {max_user} decoded at Slot {current_slot} (G={max_val:.2f}, sum_others={sum_others:.2f})")

        # === Step 2: If no capture, check for singleton in current slot ===
        if len(decoded_this_round) == 0:
            users_in_slot = np.where(slot_aloc_f[:, current_slot] == 1)[0]
            if len(users_in_slot) == 1:
                user = users_in_slot[0]
                if decoded_users[user, 0] == -1:
                    decoded_users[user, 0] = current_slot
                    decoded_this_round.append(user)
                    slot_aloc_f[user, :] = 0
                    if verbose:
                        print(f"[SIC Init] Singleton User {user} decoded at Slot {current_slot}")

        # === Step 3: Backward-propagate and recursively decode all replicas ===
        while len(decoded_this_round) > 0:
            next_decoded = []
            for user in decoded_this_round:
                # Remove all replicas of user (already done above, but safe)
                slot_aloc_f[user, :] = 0

                # Check all received slots for new singletons
                for s in received_slots:
                    users_in_s = np.where(slot_aloc_f[:, s] == 1)[0]
                    if len(users_in_s) == 1:
                        u = users_in_s[0]
                        if decoded_users[u, 0] == -1:
                            decoded_users[u, 0] = current_slot
                            next_decoded.append(u)
                            slot_aloc_f[u, :] = 0
                            if verbose:
                                print(f"[SIC Chain] User {u} decoded via singleton in Slot {s}, marked at {current_slot}")
            decoded_this_round = next_decoded

    # === Step 4: Report unresolved users ===
    for u in range(number_of_users):
        if decoded_users[u, 0] == -1:
            if verbose:
                print(f"[Unresolved] User {u} could not be decoded in this frame")

    return decoded_users
