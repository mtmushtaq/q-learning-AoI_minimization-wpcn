import os
import numpy as np
import pandas as pd

# -----------------------------
# Save Functions
# -----------------------------

def save_per_test_matrix(matrix, name, t, output_dir="data"):
    """
    Save a 2D matrix (e.g., iterations × users) for a given test index to CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{name}_t{t}.csv")
    pd.DataFrame(matrix).to_csv(file_path, index=False)


def save_per_test_vector(vector, name, t, output_dir="data"):
    """
    Save a 1D mean vector (e.g., user-level summary) for a given test index to CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{name}_mean_t{t}.csv")
    np.savetxt(file_path, vector, delimiter=",")


# -----------------------------
# Load Functions
# -----------------------------

def load_matrix_tests(name, test_count, input_dir="data"):
    """
    Load saved matrices for each test and return as a 3D array.
    Returns shape: (tests, iterations, users)
    """
    matrices = []
    for t in range(test_count):
        file_path = os.path.join(input_dir, f"{name}_t{t}.csv")
        df = pd.read_csv(file_path)
        matrices.append(df.to_numpy())
    return np.stack(matrices, axis=0)


def load_vector_tests(name, test_count, input_dir="data"):
    """
    Load saved vectors for each test and return as a 2D array.
    Returns shape: (tests, users)
    """
    vectors = []
    for t in range(test_count):
        file_path = os.path.join(input_dir, f"{name}_mean_t{t}.csv")
        vec = np.loadtxt(file_path, delimiter=",")
        vectors.append(vec)
    return np.vstack(vectors)
