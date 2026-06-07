# Smart Attendance System using Face Recognition

This is a simple **Smart Attendance System** built with Python, OpenCV, and the `face_recognition` library.
It detects faces from a webcam, recognizes known students/employees from pre-saved images,
and automatically marks their attendance in a CSV file with a timestamp.

## ✨ Features

- Detects faces live from webcam.
- Recognizes known faces from the `data/known_faces` folder.
- Marks attendance in `data/attendance.csv` with:
  - Name
  - Date
  - Time
- Avoids duplicate entries for the same person on the same day.

## 🧱 Project Structure

```text
smart-attendance-face-recognition/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py
│   └── attendance_utils.py
└── data/
    ├── known_faces/
    │   └── (put images here)
    └── attendance.csv
```

- Put face images in `data/known_faces/`.
- File name format example: `Bala.jpg`, `Ravi.png`.
- The file name (without extension) is treated as the **person's name**.

## 🛠 Requirements

- Python 3.8+
- OpenCV
- face_recognition (built on dlib)
- numpy
- pandas

Install dependencies:

```bash
pip install -r requirements.txt
```

> Note: On some systems, installing `face_recognition` may require CMake and build tools.
> You can follow instructions on the `face_recognition` GitHub page if you get errors.

## ▶️ How to Run

1. Clone the repository or download the project.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add images of people to `data/known_faces/`.
   - Example: `data/known_faces/Bala.jpg`
   - The script uses the filename (`Bala`) as the person's name.

5. Run the main script:

   ```bash
   python src/main.py
   ```

6. A window will open showing your webcam feed.
   - Recognized faces will be displayed with their names.
   - Attendance will be written to `data/attendance.csv` automatically.

## 📁 Attendance File Format

`data/attendance.csv`:

| name | date       | time     |
|------|------------|----------|
| Bala | 2025-12-10 | 10:05:23 |

- Each person is marked once per day.
- If you re-run the script the same day, it will not duplicate existing entries.

## 🧪 Testing with Sample Names

- Put 2–3 images in `data/known_faces`:
  - `Bala.jpg`
  - `Ravi.jpg`
  - `Priya.png`
- Run the script and show your face (matching those images) to the webcam.

## 🧩 Customization Ideas

- Save attendance into a database (MySQL / SQLite) instead of CSV.
- Build a small Flask / Django web dashboard to view attendance.
- Add subject / period / classroom fields to attendance.
- Export attendance report for a specific date range.

## 📜 License

This project is provided as a simple educational example.
You are free to modify and use it in your own portfolio or GitHub profile.
