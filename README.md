# Student Management API

A backend REST API built with **FastAPI** for managing students and users with **JWT authentication** and **role-based authorization**.

## 🚀 Features

* User registration
* Secure password hashing with bcrypt
* User login
* JWT access token authentication
* Current user profile
* Role-based authorization
* Admin and Teacher permissions
* Student CRUD operations
* User–Student relationship using SQLAlchemy
* Swagger API documentation
* MySQL database integration

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **MySQL**
* **PyMySQL**
* **Pydantic**
* **JWT**
* **python-jose**
* **Passlib / bcrypt**
* **Uvicorn**

## 📁 Project Structure

```text
student_management _api/
│
├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── student.py
│   │
│   ├── routers/
│   │   ├── user.py
│   │   └── student.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── student.py
│   │
│   ├── utils/
│   │   └── security.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔐 Authentication

The API uses **JWT Bearer Authentication**.

### Login Flow

```text
User Login
    ↓
Verify Email & Password
    ↓
Generate JWT Access Token
    ↓
Send Token to Client
    ↓
Use Bearer Token for Protected APIs
```

Protected endpoints require a valid JWT token.

## 👥 Role-Based Authorization

The API supports different user roles:

| Role    | Create Student | Read Students | Update Student | Delete Student |
| ------- | -------------- | ------------- | -------------- | -------------- |
| Admin   | ✅              | ✅             | ✅              | ✅              |
| Teacher | ✅              | ✅             | ✅              | ❌              |
| Student | ❌              | ❌             | ❌              | ❌              |

Unauthorized users receive:

* `401 Unauthorized` → missing/invalid authentication
* `403 Forbidden` → authenticated but insufficient permissions

## 🎓 Student CRUD

The API provides the following student operations:

### Create Student

```http
POST /students/
```

Allowed roles:

```text
admin
teacher
```

### Get All Students

```http
GET /students/
```

Allowed roles:

```text
admin
teacher
```

### Get Student By ID

```http
GET /students/{student_id}
```

Allowed roles:

```text
admin
teacher
```

### Update Student

```http
PUT /students/{student_id}
```

Allowed roles:

```text
admin
teacher
```

### Delete Student

```http
DELETE /students/{student_id}
```

Allowed role:

```text
admin
```

## 🔗 User–Student Relationship

The project uses a SQLAlchemy relationship between users and students.

```text
User
 │
 │  user_id
 ↓
Student
```

The `students` table contains:

```text
user_id
```

which references:

```text
users.id
```

When an authorized user creates a student, the logged-in user's ID is automatically stored:

```python
user_id=current_user.id
```

This connects the student with the user who created it.

## 👤 User APIs

### Register

```http
POST /users/register
```

Creates a new user with a hashed password.

New users are assigned the default role:

```text
student
```

### Login

```http
POST /users/login
```

Returns:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Current User

```http
GET /users/me
```

Returns the currently authenticated user's profile.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ritikrai7/student-management-api.git
```

### 2. Navigate to the project

```bash
cd student-management-api
```

### 3. Create a virtual environment

```bash
python -m venv myenv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_mysql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit your real `.env` file to GitHub.

## 🗄️ Database

The project uses **MySQL** with SQLAlchemy.

The main tables are:

```text
users
students
```

The relationship is:

```text
users.id
   ↑
   │
students.user_id
```

## ▶️ Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test authentication, authorization and CRUD APIs directly from Swagger UI.

## 🧪 Testing

The following authorization scenarios have been tested:

* Admin CRUD operations
* Teacher create/read/update operations
* Teacher delete restriction
* Student CRUD restrictions
* Missing JWT token
* Invalid JWT token
* User–Student relationship
* Student–User relationship

Expected security responses:

```text
401 → Authentication failure
403 → Authorization failure
404 → Resource not found
200 → Successful request
```

## 🔮 Future Improvements

* Automated unit and integration tests
* Better API error handling
* Pagination and filtering
* Search students
* Improved API documentation
* Production deployment
* CI/CD pipeline

## 👨‍💻 Author

**Ritik Rai**

GitHub: `Ritikrai7`
