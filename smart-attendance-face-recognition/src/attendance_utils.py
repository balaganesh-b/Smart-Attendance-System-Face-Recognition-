import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ATTENDANCE_PATH = os.path.join(DATA_DIR, "attendance.csv")


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def initialize_attendance_file():
    ensure_data_dir()
    if not os.path.exists(ATTENDANCE_PATH):
        df = pd.DataFrame(columns=["name", "date", "time"])
        df.to_csv(ATTENDANCE_PATH, index=False)


def has_marked_today(name: str) -> bool:
    """Check if 'name' already has attendance for today's date."""
    initialize_attendance_file()
    df = pd.read_csv(ATTENDANCE_PATH)
    today = datetime.now().date().isoformat()
    if df.empty:
        return False
    mask = (df["name"] == name) & (df["date"] == today)
    return mask.any()


def mark_attendance(name: str):
    """Append a new attendance record if not already marked for today."""
    initialize_attendance_file()
    df = pd.read_csv(ATTENDANCE_PATH)
    now = datetime.now()
    today_str = now.date().isoformat()
    time_str = now.strftime("%H:%M:%S")

    if not has_marked_today(name):
        new_row = {"name": name, "date": today_str, "time": time_str}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(ATTENDANCE_PATH, index=False)
        print(f"[INFO] Attendance marked for {name} at {today_str} {time_str}")
    else:
        print(f"[INFO] {name} already marked for today.")
