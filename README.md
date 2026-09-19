# 🎓 Student Management API

A secure and modular **RESTful backend API** for managing students, courses, enrollments, attendance, assignments, notifications, and user activity.

Built with **FastAPI, SQLAlchemy, MySQL, JWT Authentication, and Pydantic**, this project demonstrates real-world backend development concepts including authentication, role-based authorization, relational database design, validation, pagination, soft deletion, and API documentation.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* User registration and login
* JWT-based authentication
* Password hashing using Passlib
* Role-based access control
* Protected API routes

### 👨‍🎓 Student Management

* Create, read, update and delete students
* Search students
* Sorting
* Pagination
* Soft delete functionality
* User-to-student relationship

### 📚 Course Management

* Create and manage courses
* Course description and duration
* Course-based assignment management
* Course enrollment support

### 🎓 Enrollment Management

* Enroll students into courses
* View all enrollments
* View enrollments for a specific student
* View students enrolled in a specific course
* Delete enrollments
* Student ↔ Course relationship through Enrollment

### 📝 Attendance Management

* Mark student attendance
* View student attendance records
* Calculate attendance statistics
* Present/absent count
* Attendance percentage

### 📖 Assignment Management

* Create assignments
* Update assignments
* Get all assignments
* Get assignment by ID
* Get assignments for a course
* Get assignments available to a student through course enrollment
* Delete assignments

### 🔔 Notifications

* Create notifications for users
* Get all notifications
* Get user-specific notifications
* Get unread notifications
* Mark notifications as read

### 📝 Activity / Audit Logs

* Record user activities
* Store action and description
* Track activity creation time
* View all activity logs
* View activity logs for a specific user

### 📊 Dashboard & Statistics

* Student-related statistics
* Attendance statistics
* Data retrieval using relational database queries

### 📖 API Documentation

* Interactive Swagger UI
* OpenAPI documentation
* API testing directly from `/docs`

---

## 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Programming Language            |
| FastAPI           | Backend REST API Framework      |
| SQLAlchemy        | ORM and Database Interaction    |
| MySQL             | Relational Database             |
| PyMySQL           | MySQL Database Driver           |
| Pydantic          | Data Validation & Serialization |
| Pydantic Settings | Environment Configuration       |
| JWT               | Authentication                  |
| python-jose       | JWT Token Handling              |
| Passlib           | Password Hashing                |
| bcrypt            | Password Hashing Algorithm      |
| Uvicorn           | ASGI Server                     |
| python-multipart  | Form Data Support               |
| email-validator   | Email Validation                |

---

## 🏗️ Project Architecture

The project follows a modular FastAPI structure:

```text
student_management_api/
│
├── app/
│   ├── main.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   ├── attendance.py
│   │   ├── assignment.py
│   │   ├── notification.py
│   │   └── activity_log.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   ├── attendance.py
│   │   ├── assignment.py
│   │   ├── notification.py
│   │   └── activity_log.py
│   │
│   ├── routers/
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   ├── attendance.py
│   │   ├── assignment.py
│   │   └── notification.py
│   │
│   └── utils/
│       └── security.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Design

The application uses **MySQL** with SQLAlchemy ORM.

Main tables:

```text
users
students
courses
enrollments
attendance
assignments
notifications
activity_logs
```

### Main Relationships

```text
User
 │
 ├── Student
 │
 ├── Notification
 │
 └── ActivityLog
       
Student
 │
 └── Enrollment
          │
          └── Course
                 │
                 └── Assignment
```

The enrollment table acts as the connection between students and courses.

This allows a student to enroll in multiple courses and a course to contain multiple students.

---

## 🔄 Student → Course → Assignment Flow

Assignments belong to courses rather than directly to students.

The relationship works like this:

```text
Student
   ↓
Enrollment
   ↓
Course
   ↓
Assignment
```

Therefore, when retrieving assignments for a student, the API uses the enrollment relationship to find the courses of that student and then retrieves the assignments belonging to those courses.

This avoids unnecessarily storing `student_id` inside the assignment table.

---

## 🔑 Authentication Flow

The authentication process works approximately as follows:

```text
Register
   ↓
Password Hashing
   ↓
User stored in MySQL
   ↓
Login
   ↓
Credentials verified
   ↓
JWT Token generated
   ↓
Token sent with protected requests
   ↓
User authenticated
   ↓
Role checked where required
```

JWT tokens are used to protect authenticated endpoints.

---

## 🗑️ Soft Delete

Students use a soft-delete mechanism instead of immediately removing records from the database.

The student record contains:

```text
is_deleted
```

When a student is deleted, the record is marked as deleted rather than permanently removed.

This preserves the database record while preventing deleted students from appearing in normal student listings.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ritikrai7/student-management-api.git
cd student-management-api
```

### 2. Create a virtual environment

```bash
python -m venv myenv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\myenv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/std_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the database username and password with your local MySQL credentials.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 📖 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to:

* Register users
* Login
* Test authentication
* Manage students
* Manage courses
* Manage enrollments
* Manage attendance
* Manage assignments
* Manage notifications
* Manage activity logs

---

## 🔌 Major API Modules

| Module           | Purpose                              |
| ---------------- | ------------------------------------ |
| `/users`         | User registration and authentication |
| `/students`      | Student management                   |
| `/courses`       | Course management                    |
| `/enrollment`    | Student-course enrollment            |
| `/attendance`    | Attendance management                |
| `/assignments`   | Assignment management                |
| `/notifications` | User notifications                   |
| `/activity-logs` | Activity and audit logging           |

For the complete endpoint list and request/response schemas, use the Swagger documentation at `/docs`.

---

## 🧠 Key Backend Concepts Implemented

This project demonstrates practical implementation of:

* REST API development
* FastAPI routing
* Dependency Injection
* Pydantic validation
* SQLAlchemy ORM
* MySQL relationships
* Foreign Keys
* One-to-many relationships
* Many-to-many relationships
* JWT authentication
* Password hashing
* Role-based authorization
* Query filtering
* Search
* Sorting
* Pagination
* Soft deletion
* Database joins
* Attendance calculations
* API response models
* Exception handling
* Environment-based configuration
* Activity/audit logging
* Swagger/OpenAPI documentation

---

## 📌 Example: Student Assignment Query

Assignments are connected to students through enrollment.

Conceptually:

```text
Student
   ↓
Enrollment
   ↓
Course
   ↓
Assignment
```

The application can therefore retrieve assignments for a student using a database join between `Assignment` and `Enrollment`.

---

## 🔒 Security

The project includes:

* Hashed passwords
* JWT-based authentication
* Role-based authorization
* Environment variables for sensitive configuration
* Pydantic request validation
* Protected routes

Sensitive values such as database credentials and secret keys should not be committed to GitHub.

---

## 👨‍💻 Author

**Ritik Rai**

GitHub:
https://github.com/Ritikrai7

Project Repository:
https://github.com/Ritikrai7/student-management-api

---

## 🚀 Future Improvements

Possible next improvements include:

* Automated unit and integration testing
* API test coverage
* Deployment to a cloud platform
* Docker support
* CI/CD pipeline
* Database migrations using Alembic
* More advanced dashboard analytics
* Improved automated audit logging
* Production-level logging and monitoring

---

## ⭐ Project Status

**Core Student Management API: Complete ✅**

The project currently contains authentication, authorization, student and course management, enrollment, attendance, assignments, notifications, statistics, and activity/audit logging.

