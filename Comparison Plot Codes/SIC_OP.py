import numpy as np


def Successive_IC(users_total, d_matrix, slots):
    """
    Perform Successive Interference Cancellation (SIC) on a binary matrix of user replicas.

    Parameters:
      users_total (int): total number of users.
      d_matrix (np.array): A binary matrix (users_total x slots) with entries 0/1.
      slots (int): total number of slots.

    Returns:
      np.array: A matrix where each row corresponds to a user and contains:
                [User ID, First slot where the user appeared, Slot where the user was decoded]
                If a user is never decoded, the decode slot is -1.
    """
    # Ensure d_matrix is a numpy array
    d_matrix = np.array(d_matrix)

    # Compute first appearance (first replica) for each user.
    # If a user never transmits, we leave its first slot as -1.
    first_appearance = np.full(users_total, -1, dtype=int)
    for user in range(users_total):
        slot_indices = np.where(d_matrix[user] == 1)[0]
        if slot_indices.size > 0:
            first_appearance[user] = slot_indices[0]

    # Initialize the decoded information: each row [user_id, first_replica_slot, decode_slot]
    # decode_slot is initialized to -1 meaning not yet decoded.
    decoded_info = np.array([[user, first_appearance[user], -1] for user in range(users_total)])

    # Make a copy of the matrix that we will update as we cancel decoded users.
    residual = d_matrix.copy()

    new_decoded = True
    while new_decoded:
        new_decoded = False
        # For each slot, check if exactly one user is transmitting (singleton slot)
        for slot in range(slots):
            col = residual[:, slot]
            if np.sum(col) == 1:  # Slot is singleton, thus decodable.
                # Identify which user is present.
                user_idx = np.where(col == 1)[0][0]
                # If the user hasn't already been decoded, record the slot and cancel its other replicas.
                if decoded_info[user_idx, 2] == -1:
                    decoded_info[user_idx, 2] = slot
                    new_decoded = True
                    # Cancel this user's transmissions from all slots.
                    residual[user_idx, :] = 0
    return decoded_info


# -----------------------------------------------------------------------------
# Scenario 1: All users are eventually decodable.
# For example, suppose we have 4 users and 5 slots.
# The matrix below (rows = users, columns = slots) is designed so that some slots
# have a single transmission while collisions can be resolved via SIC.

# User 0: appears in slots 0 and 2  (first replica slot: 0)
# User 1: appears in slots 0 and 3  (first replica slot: 0)
# User 2: appears in slot 1         (first replica slot: 1)
# User 3: appears in slots 1 and 4  (first replica slot: 1)
d_matrix1 = [
    [1, 0, 1, 0, 0],  # User 0
    [1, 0, 0, 1, 0],  # User 1
    [0, 1, 0, 0, 0],  # User 2
    [0, 1, 0, 0, 1]  # User 3
]
users_total1 = 4
slots1 = 5

print("Scenario 1: All users eventually decoded")
decoded_users1 = Successive_IC(users_total1, d_matrix1, slots1)
print("Decoded user information:")
print("UserID | First Replica Slot | Decoded Slot")
print(decoded_users1)

# -----------------------------------------------------------------------------
# Scenario 2: Two users remain unrecovered.
# In this scenario, 4 users and 4 slots are used.
# Users 0 and 1 each transmit in the same two slots,
# causing collisions that cannot be resolved because no slot has a singleton.
# Users 2 and 3 are decodable.
# Expected:
#   User 0: first replica slot = 0, decoded slot = -1 (never decoded)
#   User 1: first replica slot = 0, decoded slot = -1 (never decoded)
#   User 2: first replica slot = 1, decoded slot = 1
#   User 3: first replica slot = 3, decoded slot = 3
d_matrix2 = [
    [1, 0, 1, 0],  # User 0: collision in slots 0 and 2
    [1, 0, 1, 0],  # User 1: collision in slots 0 and 2
    [0, 1, 0, 0],  # User 2: singleton in slot 1
    [0, 0, 0, 1]  # User 3: singleton in slot 3
]
users_total2 = 4
slots2 = 4

print("\nScenario 2: Two users unrecoverable due to persistent collisions")
decoded_users2 = Successive_IC(users_total2, d_matrix2, slots2)
print("Decoded user information:")
print("UserID | First Replica Slot | Decoded Slot")
print(decoded_users2)
