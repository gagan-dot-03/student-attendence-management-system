import sqlite3
import sys
from datetime import date

DB_NAME = "attendance.db"

def initate_database():
    """Builds the database tables directly within this script to avoid import errors."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Students Table for student information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    
    # 2. Courses Table for course information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL
        )
    ''')
    
    # 3. Enrollments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    ''')
    
    # 4. Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            attendance_date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# CRITICAL FIX: Explicitly call the initialization function at startup
initate_database()


def get_int_input(prompt):
    """Utility helper to prevent program crashes on invalid or empty numerical inputs."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(" Invalid input! Please enter a valid numerical ID number.")


def add_student():
    print("\n--- Add New Student Record ---")
    name = input("Enter Student Name: ").strip()
    department = input("Enter Department: ").strip()

    if not name or not department:
        print(" Error: Both Student Name and Department fields are required.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, department) VALUES (?, ?)",
        (name, department)
    )
    conn.commit()
    conn.close()
    print(f" Student '{name}' added successfully!")

def add_course():
    print("\n--- Add New Course ---")
    course_name = input("Enter Course Name: ").strip()

    if not course_name:
        print(" Error: Course Name cannot be left blank.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (course_name) VALUES (?)",
        (course_name,)
    )
    conn.commit()
    conn.close()
    print(f" Course '{course_name}' added successfully!")


def view_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, department FROM students")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Registered Students Directory ---")
    if not rows:
        print("No student records found in the database.")
        return

    print(f"{'ID':<6} | {'Student Name':<25} | {'Department'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<6} | {row[1]:<25} | {row[2]}")


def view_courses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM courses")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Available Institutional Courses ---")
    if not rows:
        print("No course tracks found in the database.")
        return

    print(f"{'ID':<6} | {'Course Name'}")
    print("-" * 35)
    for row in rows:
        print(f"{row[0]:<6} | {row[1]}")


def enroll_student():
    print("\n--- Enroll Student in Course Track ---")
    view_students()
    view_courses()

    student_id = get_int_input("\nEnter Student ID to enroll: ")
    course_id = get_int_input("Enter target Course ID: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
            (student_id, course_id)
        )
        conn.commit()
        print(" Student enrolled successfully!")
    except sqlite3.IntegrityError:
        print(" Foreign Key Error: Verify that both Student ID and Course ID exist before enrolling.")
    finally:
        conn.close()


def mark_attendance():
    print("\n--- Log Daily Class Attendance ---")
    student_id = get_int_input("Enter Student ID: ")
    course_id = get_int_input("Enter Course ID: ")

    status = input("Enter Attendance (P/A): ").strip().upper()
    if status not in ['P', 'A']:
        print(" Error: Invalid input marker. Use 'P' for Present or 'A' for Absent.")
        return

    attendance_date = str(date.today())

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO attendance (student_id, course_id, attendance_date, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, course_id, attendance_date, status))
        conn.commit()
        print(f" Attendance marked successfully as '{status}' for today ({attendance_date})!")
    except sqlite3.IntegrityError:
        print(" Operational Error: Could not mark entry. Double-check that IDs are valid.")
    finally:
        conn.close()


def attendance_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name,
               c.course_name,
               a.attendance_date,
               a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN courses c ON a.course_id = c.course_id
        ORDER BY a.attendance_date DESC
    """)
    records = cursor.fetchall()
    conn.close()

    print("\n--- Historical Attendance Ledger Reports ---")
    if not records:
        print("No attendance records found.")
    else:
        print(f"{'Student Name':<20} | {'Course Track Name':<25} | {'Date':<12} | {'Status'}")
        print("-" * 70)
        for row in records:
            status_label = "Present" if row[3] == 'P' else "Absent"
            print(f"{row[0]:<20} | {row[1]:<25} | {row[2]:<12} | {status_label}")


def attendance_percentage():
    print("\n--- Academic Metrics Analysis ---")
    student_id = get_int_input("Enter Student ID: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id = ?
    """, (student_id,))
    total_classes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id = ?
        AND status = 'P'
    """, (student_id,))
    present_count = cursor.fetchone()[0]

    conn.close()

    if total_classes == 0:
        print(" No logged attendance records tracked for this student ID.")
    else:
        percentage = (present_count / total_classes) * 100
        print(f" Total Tracked Sessions: {total_classes}")
        print(f" Attended Count:        {present_count}")
        print(f" Attendance Percentage:  {percentage:.2f}%")


while True:
    print("\n========== STUDENT ATTENDANCE MANAGEMENT SYSTEM ==========")
    print("1. Add Student")
    print("2. Add Course")
    print("3. View Students")
    print("4. View Courses")
    print("5. Enroll Student")
    print("6. Mark Attendance")
    print("7. Attendance History")
    print("8. Attendance Percentage")
    print("9. Exit")

    choice = input("\nEnter your choice (1-9): ").strip()

    if choice == "1": add_student()
    elif choice == "2": add_course()
    elif choice == "3": view_students()
    elif choice == "4": view_courses()
    elif choice == "5": enroll_student()
    elif choice == "6": mark_attendance()
    elif choice == "7": attendance_history()
    elif choice == "8": attendance_percentage()
    elif choice == "9":
        print("Thank You!")
        break
    else:
        print(" Invalid Choice! Please select a valid parameter code between 1 and 9.")