import streamlit as st
import pandas as pd
import os
from utils.ui import set_page_style
from utils.helpers import load_data, save_data, generate_nurse_id

# --- File Paths ---
NURSES_FILE = "database/nurses.xlsx"
PATIENTS_FILE = "database/patients.xlsx"
SHIFTS_FILE = "database/shifts.xlsx"
ATTENDANCE_FILE = "database/attendance.xlsx"
LEAVE_REQUESTS_FILE = "database/leave_requests.xlsx"

# --- User Roles ---
USER_CREDENTIALS = {
    "admin": "Admin",
    "head": "Head Nurse",
    "nurse": "Nurse"
}

# --- UI Setup ---
set_page_style()

# --- Login Page ---
def login_page():
    st.image("static/logo.png", width=180)  # Display the logo
    st.markdown("<h1 style='text-align: center; color: black;'>NURSING SYSTEM</h1>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["role"] = None

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if password in USER_CREDENTIALS:
            st.session_state["logged_in"] = True
            st.session_state["role"] = USER_CREDENTIALS[password]
            st.success(f"✅ Logged in as {st.session_state['role']}")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# --- Admin Dashboard ---
def admin_dashboard():
    st.title("👨‍⚕️ Admin Dashboard")

    action = st.selectbox("Choose an action:", 
                          ["Manage Nurses", "Manage Patients", "Allocate Shifts", "View Attendance", "Leave Requests"])

    # Manage Nurses
    if action == "Manage Nurses":
        st.header("🩺 Manage Nurses")
        nurses_data = load_data(NURSES_FILE, columns=["Nurse ID", "Name", "Level", "Department"])

        # Display Nurses Table
        if not nurses_data.empty:
            st.dataframe(nurses_data)

        # Add Nurse Form
        with st.form("add_nurse_form"):
            name = st.text_input("Name")
            level = st.selectbox("Level", ["Admin", "Head Nurse", "Nurse"])
            dept = st.text_input("Department")

            if st.form_submit_button("Add Nurse"):
                nurse_id = generate_nurse_id(level)
                new_nurse = pd.DataFrame([[nurse_id, name, level, dept]], columns=["Nurse ID", "Name", "Level", "Department"])
                nurses_data = pd.concat([nurses_data, new_nurse], ignore_index=True)
                save_data(NURSES_FILE, nurses_data)
                st.success(f"✅ Nurse {name} added successfully! (ID: {nurse_id})")
                st.rerun()

                 # Custom CSS for the button
            st.markdown("""
                <style>
                div.stButton > button:first-child {
                    color: white;
                }
                </style>
                """, unsafe_allow_html=True)
                
    elif action == "Manage Patients":
        st.header("🏥 Manage Patients")
        patients_data = load_data(PATIENTS_FILE, columns=["Patient ID", "Name", "Condition", "Assigned Nurse"])
        st.dataframe(patients_data)

        # Display Patients Table
        if not patients_data.empty:
            st.dataframe(patients_data)

        # Add Patient Form
        with st.form("add_patient_form"):
            name = st.text_input("Patient Name")
            condition = st.text_input("Condition")
            assigned_nurse = st.text_input("Assigned Nurse")

            if st.form_submit_button("Add Patient"):
                patient_id = generate_patient_id()
                new_patient = pd.DataFrame([[patient_id, name, condition, assigned_nurse]], columns=["Patient ID", "Name", "Condition", "Assigned Nurse"])
                patients_data = pd.concat([patients_data, new_patient], ignore_index=True)
                save_data(PATIENTS_FILE, patients_data)
                st.success(f"✅ Patient {name} added successfully! (ID: {patient_id})")
                st.rerun()

    elif action == "Allocate Shifts":
        st.header("📅 Allocate Shifts")
        nurses_data = load_data(NURSES_FILE)
        shift_date = st.date_input("Select Date")
        nurse_id = st.selectbox("Select Nurse", nurses_data["Nurse ID"].tolist())

        if st.button("Allocate Shift"):
            shifts_data = load_data(SHIFTS_FILE, columns=["Nurse ID", "Date"])
            new_shift = pd.DataFrame([[nurse_id, shift_date]], columns=["Nurse ID", "Date"])
            shifts_data = pd.concat([shifts_data, new_shift], ignore_index=True)
            save_data(SHIFTS_FILE, shifts_data)
            st.success(f"✅ Shift allocated for {nurse_id} on {shift_date}")
            st.rerun()

             # Display Shifts Table
        shifts_data = load_data(SHIFTS_FILE)
        st.dataframe(shifts_data)
        

    elif action == "View Attendance":
        st.header("📊 Attendance Records")
        attendance_data = load_data(ATTENDANCE_FILE)
        st.dataframe(attendance_data)

# --- Head Nurse Dashboard ---
def head_nurse_dashboard():
    st.title("👩‍⚕️ Head Nurse Dashboard")

    action = st.selectbox("Choose an action:", ["View Nurses", "View Attendance", "View Schedules"])

    if action == "View Nurses":
        st.header("🩺 Nurses List")
        nurses_data = load_data(NURSES_FILE)
        st.dataframe(nurses_data)

    elif action == "View Attendance":
        st.header("📊 Attendance Records")
        attendance_data = load_data(ATTENDANCE_FILE)
        st.dataframe(attendance_data)

    elif action == "View Schedules":
        st.header("📅 Nurse Schedules")
        shifts_data = load_data(SHIFTS_FILE)
        st.dataframe(shifts_data)

# --- Nurse Dashboard ---
def nurse_dashboard():
    st.title("👩‍⚕️ Nurse Dashboard")

    action = st.selectbox("Choose an action:", ["Mark Attendance", "Submit Leave Request", "View Schedule"])

    if action == "Mark Attendance":
        st.header("✅ Mark Attendance")
        nurse_id = st.text_input("Enter your Nurse ID")

        if nurse_id and st.button("Mark Present"):
            attendance_data = load_data(ATTENDANCE_FILE, columns=["ID", "Nurse ID", "Date", "Status"])
            new_attendance = pd.DataFrame([[len(attendance_data) + 1, nurse_id, pd.Timestamp.now().date(), "Present"]],
                                          columns=["ID", "Nurse ID", "Date", "Status"])
            attendance_data = pd.concat([attendance_data, new_attendance], ignore_index=True)
            save_data(ATTENDANCE_FILE, attendance_data)
            st.success("✅ Attendance marked successfully!")
            st.rerun()

    elif action == "View Schedule":
        st.header("📅 Your Schedule")
        shifts_data = load_data(SHIFTS_FILE)
        st.dataframe(shifts_data)

# --- Main Function ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["role"] = None

    if not st.session_state["logged_in"]:
        login_page()
    else:
        if st.session_state["role"] == "Admin":
            admin_dashboard()
        elif st.session_state["role"] == "Head Nurse":
            head_nurse_dashboard()
        elif st.session_state["role"] == "Nurse":
            nurse_dashboard()

        # Logout Button
        if st.sidebar.button("🔴 Logout"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()

if __name__ == "__main__":
    main()
