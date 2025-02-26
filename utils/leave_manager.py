import pandas as pd
from utils.attendance_manager import load_data, save_data

LEAVE_FILE = "database/leave_requests.xlsx"

def submit_leave_request(nurse_id, start_date, end_date, reason):
    """Submits a leave request for a nurse."""
    leave_data = load_data(LEAVE_FILE, columns=["ID", "Nurse ID", "Start Date", "End Date", "Reason", "Status"])
    
    new_request = pd.DataFrame([[len(leave_data) + 1, nurse_id, start_date, end_date, reason, "Pending"]],
                               columns=["ID", "Nurse ID", "Start Date", "End Date", "Reason", "Status"])
    
    leave_data = pd.concat([leave_data, new_request], ignore_index=True)
    save_data(LEAVE_FILE, leave_data)
    return "✅ Leave request submitted successfully!"
