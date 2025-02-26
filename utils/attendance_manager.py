import pandas as pd
import os

ATTENDANCE_FILE = "database/attendance.xlsx"

def load_data(file_path, columns=None):
    """Loads an Excel file, or creates a new one if it doesn't exist."""
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=columns) if columns else pd.DataFrame()
        save_data(file_path, df)
        return df

def save_data(file_path, data):
    """Saves data to an Excel file."""
    data.to_excel(file_path, index=False)

def mark_attendance(nurse_id):
    """Marks attendance for a nurse."""
    attendance_data = load_data(ATTENDANCE_FILE, columns=["ID", "Nurse ID", "Date", "Status"])
    
    new_attendance = pd.DataFrame([[len(attendance_data) + 1, nurse_id, pd.Timestamp.now().date(), "Present"]],
                                  columns=["ID", "Nurse ID", "Date", "Status"])
    
    attendance_data = pd.concat([attendance_data, new_attendance], ignore_index=True)
    save_data(ATTENDANCE_FILE, attendance_data)
    return "✅ Attendance marked successfully!"
