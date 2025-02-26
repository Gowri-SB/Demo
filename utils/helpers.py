import pandas as pd
import os

# --- Function to load data from an Excel file ---
def load_data(file_path, columns=None):
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=columns)
    return pd.read_excel(file_path) if columns is None else pd.read_excel(file_path, usecols=columns)

# --- Function to save data to an Excel file ---
def save_data(file_path, data):
    data.to_excel(file_path, index=False, engine='openpyxl')

# --- Function to generate unique Nurse IDs based on role ---
def generate_nurse_id(level):
    """
    Generate an ID based on the nurse's level.
    - Admin: AD**
    - Head Nurse: HN****
    - Nurse: NU***
    """
    from random import randint

    if level == "Admin":
        return f"AD{randint(10, 99)}"
    elif level == "Head Nurse":
        return f"HN{randint(1000, 9999)}"
    elif level == "Nurse":
        return f"NU{randint(100, 999)}"
    else:
        return f"XX{randint(100, 999)}"  # Fallback ID
