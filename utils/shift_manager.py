import pandas as pd
import random
from datetime import datetime, timedelta
from utils.attendance_manager import save_data  # Import save function

SHIFTS_FILE = "database/shifts.xlsx"

def generate_random_shifts(num_shifts):
    """Generates and saves random shifts."""
    departments = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics"]
    specialties = ["Surgeon", "Nurse", "Technician", "Anesthetist"]
    
    shifts = []
    for _ in range(num_shifts):
        date = datetime.today() + timedelta(days=random.randint(1, 30))
        start_time = datetime.today().replace(hour=random.randint(8, 18), minute=0, second=0)
        end_time = start_time + timedelta(hours=8)
        department = random.choice(departments)
        specialty = random.choice(specialties)

        shifts.append({
            "Shift ID": len(shifts) + 1,
            "Date": date.strftime("%Y-%m-%d"),
            "Start Time": start_time.strftime("%H:%M"),
            "End Time": end_time.strftime("%H:%M"),
            "Department": department,
            "Specialty": specialty
        })

    df = pd.DataFrame(shifts)
    save_data(SHIFTS_FILE, df)
    return shifts
