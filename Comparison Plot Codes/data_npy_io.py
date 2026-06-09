import numpy as np
import os
import glob

# -----------------------------
# SAVE FUNCTIONS
# -----------------------------

def save_all_test_data_npy(
    matrices_dict: dict,
    vectors_dict: dict,
    output_dir: str = "data"
):
    """
    Save all test data to .npy files in the specified output directory.

    Parameters:
    - matrices_dict: dict of {name: list of 2D arrays}
    - vectors_dict: dict of {name: list of 1D arrays}
    """
    os.makedirs(output_dir, exist_ok=True)

    for name, data_list in matrices_dict.items():
        arr = np.array(data_list)
        np.save(os.path.join(output_dir, f"{name}.npy"), arr)

    for name, vec_list in vectors_dict.items():
        arr = np.array(vec_list)
        np.save(os.path.join(output_dir, f"{name}.npy"), arr)


# -----------------------------
# LOAD FUNCTIONS
# -----------------------------

def load_test_matrix_npy(name: str, input_dir: str ):
    """Load saved 3D matrix from .npy file."""
    return np.load(os.path.join(input_dir, f"{name}.npy"))

def load_test_vector_npy(name: str, input_dir: str ):
    """Load saved 2D vector matrix from .npy file."""
    return np.load(os.path.join(input_dir, f"{name}.npy"))


# -----------------------------
# CLEANUP
# -----------------------------

def delete_csv_files(folder: str = "data"):
    """Delete all CSV files from a directory (optional cleanup)."""
    for file in glob.glob(os.path.join(folder, "*.csv")):
        os.remove(file)
