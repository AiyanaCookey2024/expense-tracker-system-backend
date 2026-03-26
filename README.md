# Expense Tracker API (Backend)

## Overview
This project is a Django REST API that powers the Expense Tracker application. It provides secure authentication, budgeting functionality, and expense management through a structured architecture.

The API uses JWT-based authentication and follows a layered design to separate concerns between authentication and business logic.

---

## Features
- User registration and login (JWT authentication)
- Secure protected API endpoints
- Budget creation, update, and deletion
- Expense tracking linked to salary periods
- Password reset functionality using token-based system
- End-to-end tested workflows

---

## Tech Stack
- Python (Django)
- Django REST Framework
- SimpleJWT (authentication)
- SQLite (development database)
- PostgreSQL (production via Render)
- Cloudinary (media handling - optional if used)

---

## Architecture & Design

The backend follows a layered architecture:

- **Views (API Layer)**  
  Handles HTTP requests and responses.

- **Serializers (Validation Layer)**  
  Responsible for input validation and data transformation.

- **Models (Data Layer)**  
  Defines database schema and relationships.

- **Authentication Layer**  
  JWT-based authentication ensures secure access to protected endpoints.

This separation improves maintainability, scalability, and testability.

---

## Key Technical Decisions

### Password Reset via Token
A token-based password reset system was implemented to enhance security and simulate real-world application behaviour.

API endpoints are protected with JWT authentication, so direct browser access without the token with return a 401 error. Backend functionality was demonstrated through Django admin, automated tests, and authenticated API requests.

### Testing Strategy
Automated tests were written to validate:
- Authentication flows
- CRUD operations
- End-to-end user journeys

---

## Setup Instructions

### 1. Create and activate a virtual enviornment 
```bash
python3 -m venv venv 
source venv/bin/activate
```
### 2. Change the directory to backend 
```bash
cd backend
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations if needed
```bash
python manage.py migrate 
```

### 5. Run server
```bash
python manage.py runserver
```

### 6. Running tests
```bash
python manage.py test 
```

### 7. Deployment 
## Backend and frontend are deployed using Render 
### Live API: https://expense-tracker-system-1l5v.onrender.com

### 8. CI/CD 
### Github Actions used to automate testing:

- Runs on every push and pull request 
- Installs dependencies
- Executes test suite


