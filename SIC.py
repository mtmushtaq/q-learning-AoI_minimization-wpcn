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



def capture_effect_SIC_realtime_PDNOMA(slot_aloc_f: np.ndarray,
                                       number_of_slots: int,
                                       number_of_users: int,
                                       L: int,
                                       verbose: bool = True) -> np.ndarray:
    """
    PD-NOMA SIC decoding with per-slot power levels in slot_aloc_f.
    slot_aloc_f[u, s] ∈ {0, 1..L}   (0 = no replica; 1 = highest level; L = lowest)
    Returns decoded_users: shape (U, 2)
       decoded_users[u, 0] = slot index where user u finally decoded, or -1 if unresolved
       decoded_users[u, 1] = first slot where u transmitted a replica (if any), else -1
    """

    # Work on a copy so we can zero-out replicas as users are decoded
    M = slot_aloc_f.copy()
    U = number_of_users
    S = number_of_slots

    # decoded_users[:,0] = decode slot (init -1), decoded_users[:,1] = first TX slot
    decoded_users = -1 * np.ones((U, 2), dtype=int)

    # Record each user's first transmission slot (any level > 0)
    for u in range(U):
        tx_slots = np.where(M[u, :] > 0)[0]
        if tx_slots.size > 0:
            decoded_users[u, 1] = int(tx_slots[0])

    received_slots = []

    # --- Helper: try to decode as much as possible in slot s (in-place). -----
    def process_slot(s: int) -> bool:
        """
        Apply PD-NOMA ladder in slot s:
          - For k from 1..L: a level-k user can be decoded iff
              (i) there are no *undecoded* users at any higher level < k in this slot, AND
             (ii) after removing users already decoded elsewhere, there is exactly one undecoded user at level k.
          - When a user is decoded in slot s, remove all its replicas across all slots.
        Returns True iff at least one new user was decoded in this call.
        """
        made_progress = False

        # Remove from this slot any users that have already been decoded elsewhere
        already_decoded_here = np.where((M[:, s] > 0) & (decoded_users[:, 0] != -1))[0]
        if already_decoded_here.size > 0:
            M[already_decoded_here, s] = 0
            if verbose:
                for u in already_decoded_here:
                    print(f"[SIC Clean] Removed already-decoded user {u} from slot {s}")

        # Ladder from highest (1) to lowest (L)
        for k in range(1, L + 1):
            # Block if *any* higher level has undecoded users in this slot
            higher_busy = False
            for h in range(1, k):
                if np.any((M[:, s] == h) & (decoded_users[:, 0] == -1)):
                    higher_busy = True
                    break
            if higher_busy:
                continue

            # Candidates at level k that are not decoded yet
            cand = np.where((M[:, s] == k) & (decoded_users[:, 0] == -1))[0]

            if cand.size == 0:
                # nothing at this level
                continue

            if cand.size > 1:
                # Collision at level k. Try to remove users that were decoded elsewhere.
                # (They are already excluded above; so if >1 remains, we cannot decode this level now.)
                # We leave collisions for future SIC propagation.
                if verbose:
                    print(f"[Collision] Slot {s}, level {k}: users {cand.tolist()}")
                continue

            # Exactly one undecoded user at this level AND all higher levels are clear -> decode!
            u = int(cand[0])
            decoded_users[u, 0] = s
            # Remove all replicas of u across all slots
            M[u, :] = 0
            made_progress = True
            if verbose:
                print(f"[Decode] User {u} at slot {s}, level {k}")

        return made_progress

    # ------------------ Main decoding loop (slot-by-slot) ---------------------
    for current_slot in range(S):
        received_slots.append(current_slot)
        if verbose:
            print(f"\n--- Slot {current_slot} Received ---")

        # First, process the current slot once
        progress = process_slot(current_slot)

        # Then, as in classic SIC, keep sweeping all received slots until no progress
        keep_going = True
        while keep_going:
            keep_going = False
            # After removing replicas due to new decodes, previous slots may have become decodable
            for s in received_slots:
                if process_slot(s):
                    keep_going = True
                    progress = True

        # If nothing got decoded here, it's fine; we proceed to next slot

    # Report unresolved users (optional)
    if verbose:
        for u in range(U):
            if decoded_users[u, 0] == -1:
                print(f"[Unresolved] User {u} not decoded")
            else:
                tx = decoded_users[u, 1]
                rx = decoded_users[u, 0]
                print(f"[Resolved] User {u}: first_tx={tx}, decoded_at={rx}")

    return decoded_users
