# Online Course Management System (OCMS)

A robust and scalable Online Course Management System built with Django REST Framework (DRF) and PostgreSQL. It uses JWT Authentication for secure API access and provides role-based authorization for Students, Instructors, and Admins.

## Features

- **Role-Based Authorization:**
  - **Student:** Can view courses, enroll in courses, and leave reviews.
  - **Instructor:** Can create, update, and delete only their own courses, and view their dashboard.
  - **Admin:** Has full access to all resources and user management.
- **Instructor Dashboard API:** Comprehensive dashboard returning metrics such as total courses created, student enrollments, average ratings, total reviews, recent enrollments, and most popular courses.
- **Enrollment Notifications:** Automated email notifications sent to students upon successful enrollment.
- **JWT Authentication:** Secure user authentication using JSON Web Tokens.
- **API Documentation:** Interactive Swagger and ReDoc documentation powered by `drf-spectacular`.

## Architecture

The system is built on a monolithic architecture using Django and Django REST Framework. 
- **Database:** PostgreSQL is used as the primary relational database.
- **Authentication:** `rest_framework_simplejwt` handles JWT-based authentication.
- **Authorization:** Custom DRF permissions enforce role-based access control.
- **Apps:** The project is modularized into several Django apps:
  - `accounts`: Manages user profiles and roles.
  - `courses`: Manages course creation, details, and listing.
  - `enrollments`: Handles student enrollments and email notifications.
  - `reviews`: Manages course ratings and feedback.
  - `dashboard`: Aggregates metrics for the instructor dashboard.

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd ONLINE_COURSE_MANAGEMENT_SYSTEM/OCMS
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure `python-dotenv`, `drf-spectacular`, and `psycopg2` are included in your requirements)*

4. **Configure Environment Variables:**
   Create a `.env` file in the `OCMS` directory:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   
   # Database Configurations
   DB_NAME=ocms_database
   DB_USER=postgres
   DB_PASSWORD=1234
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email Configurations
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

5. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

## Docker Setup

You can easily run the application using Docker and Docker Compose.

1. **Create `Dockerfile`:**
   Ensure you have a Dockerfile at the root of the project.
2. **Create `docker-compose.yml`:**
   Configure a web service and a postgres db service.
3. **Build and Run:**
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

### Courses
- `GET /courses/` - List courses (with pagination & filtering)
- `POST /courses/` - Create a course (Instructor/Admin)
- `GET /courses/<id>/` - Retrieve a course
- `PUT/PATCH /courses/<id>/` - Update a course (Instructor/Admin)
- `DELETE /courses/<id>/` - Delete a course (Instructor/Admin)

### Enrollments
- `GET /enrollments/` - List enrollments
- `POST /enrollments/` - Create a manual enrollment
- `POST /enrollments/course/<course_id>/` - Enroll in a course (triggers email)

### Reviews
- `GET /reviews/` - List reviews
- `POST /reviews/` - Create a review

### Instructor Dashboard
- `GET /dashboard/` - Retrieve instructor metrics

### Documentation
- `GET /api/schema/swagger-ui/` - Interactive Swagger UI
- `GET /api/schema/redoc/` - ReDoc API documentation

## Screenshots

*(Add screenshots of your Swagger UI, Insomnia/Postman tests, or any frontend implementation here.)*

## Future Scope

- **Payment Gateway Integration:** Integrate Stripe or PayPal to handle paid courses.
- **Video Hosting:** Support uploading and streaming course lectures using AWS S3 or similar services.
- **Progress Tracking:** Allow students to track their progress per module.
- **Frontend Integration:** Build a robust SPA (Single Page Application) using React or Next.js to consume the DRF APIs.
- **Caching:** Implement Redis caching for high-traffic endpoints like course listings.
