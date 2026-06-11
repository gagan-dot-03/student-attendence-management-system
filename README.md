# 📚 Student Attendance Management System

A simple and efficient attendance management system built using **Python** and **SQLite**. This mini project helps manage student records, courses, enrollments, and attendance tracking in an organized manner.

---

## 🚀 Features

- 👨‍🎓 Student Registration
- 📖 Course Creation
- 📝 Student Enrollment
- ✅ Attendance Marking
- 📅 Attendance History
- 📊 Attendance Percentage Calculation

---

## 🛠️ Technologies Used

- **Python**
- **SQLite**

---

## 📂 Project Structure

```
Student-Attendance-Management-System/
│
├── attendance_system.py
├── attendance.db
├── README.md
└── requirements.txt (optional)
```

---

## 🗄️ Database Schema

### 1. Students
Stores student information.

| Field | Description |
|---------|-------------|
| student_id | Unique ID of the student |
| student_name | Name of the student |
| email | Student email address |
| phone | Contact number |

### 2. Courses
Stores course details.

| Field | Description |
|---------|-------------|
| course_id | Unique ID of the course |
| course_name | Name of the course |
| course_code | Unique course code |

### 3. Enrollments
Maps students to courses.

| Field | Description |
|---------|-------------|
| enrollment_id | Unique enrollment ID |
| student_id | Reference to student |
| course_id | Reference to course |

### 4. Attendance
Stores attendance records.

| Field | Description |
|---------|-------------|
| attendance_id | Unique attendance ID |
| student_id | Reference to student |
| course_id | Reference to course |
| attendance_date | Date of attendance |
| status | Present / Absent |

---

## ⚙️ How to Run

### Prerequisites

- Python 3.x installed on your system.

### Steps

1. Clone the repository:

```bash
git clone https://github.com/your-username/student-attendance-management-system.git
```

2. Navigate to the project directory:

```bash
cd student-attendance-management-system
```

3. Run the application:

```bash
python attendance_system.py
```

---

## 💡 Usage

The system allows users to:

- Register new students.
- Create and manage courses.
- Enroll students in courses.
- Mark daily attendance.
- View attendance history.
- Calculate attendance percentages for each student.

---

## 📈 Future Enhancements

- Graphical User Interface (GUI)
- User Authentication and Authorization
- Export Attendance Reports to PDF/Excel
- Email Notifications
- Dashboard and Analytics
- Web-Based Deployment

---

## 🎯 Benefits

- Reduces manual errors in attendance tracking.
- Saves time and effort.
- Maintains attendance records efficiently.
- Generates attendance statistics instantly.
- Lightweight and easy to deploy using SQLite.

---

## 📄 License

This project is developed for **educational and learning purposes**. Feel free to modify and enhance it according to your requirements.

---

## 👨‍💻 Author

**Your Name**

Mini Project – Student Attendance Management System
