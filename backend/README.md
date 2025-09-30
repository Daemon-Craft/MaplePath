# MaplePath FastAPI Backend

Backend API for MaplePath - A Canadian immigration and integration platform built with FastAPI, PostgreSQL, and Firebase Authentication.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust database with SQLAlchemy ORM
- **Firebase Authentication** - Google sign-in integration
- **JWT Authentication** - Secure token-based auth for email/password
- **Alembic** - Database migrations
- **Cloud SQL** - Production deployment on Google Cloud Platform

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Authentication endpoints
│   │       │   └── users.py         # User profile endpoints
│   │       └── api.py               # API router configuration
│   ├── core/
│   │   ├── config.py                # Application settings
│   │   └── security.py              # JWT and password utilities
│   ├── db/
│   │   └── database.py              # Database connection
│   ├── models/
│   │   └── user.py                  # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py                  # Pydantic schemas
│   └── services/
│       └── user_service.py          # Business logic
├── migrations/                      # Alembic database migrations
├── main.py                         # FastAPI application entry point
├── requirements.txt                # Python dependencies
├── alembic.ini                     # Alembic configuration
├── Dockerfile                      # Docker container config
└── cloudbuild.yaml                 # GCP Cloud Build config
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/google-auth` - Login with Google Firebase token
- `GET /api/v1/auth/me` - Get current user profile

### Users
- `POST /api/v1/users/register` - Register new user
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/users/profile/{user_id}` - Get user by ID

## Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Firebase project with Authentication enabled

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/maplepath_dev
SECRET_KEY=your-super-secret-jwt-key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

5. **Setup Firebase**
- Download your Firebase service account key JSON file
- Place it as `firebase-credentials.json` in the backend directory

6. **Create PostgreSQL database**
```sql
CREATE DATABASE maplepath_dev;
```

7. **Run database migrations**
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

8. **Start development server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Production Deployment (Google Cloud)

### CloudSQL Setup
1. Create CloudSQL PostgreSQL instance
2. Create database: `maplepath_prod`
3. Set up connection and environment variables

### Cloud Build & Cloud Run
The project is configured for automatic deployment using Cloud Build:

```bash
gcloud builds submit --config cloudbuild.yaml
```

### Environment Variables (Production)
Set these in Cloud Run:
- `DATABASE_URL_PROD` - CloudSQL connection string
- `SECRET_KEY` - JWT secret key
- `FIREBASE_CREDENTIALS_PATH` - Path to Firebase credentials

## Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email address
- `hashed_password` - Bcrypt hashed password (nullable for Google auth)
- `full_name` - User's full name
- `firebase_uid` - Firebase user ID (for Google auth)
- `is_active` - Account status
- `is_verified` - Email verification status
- `phone_number` - Contact number
- `profile_picture_url` - Profile image URL
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

## Authentication Flow

### Email/Password Registration
1. `POST /api/v1/users/register` with email and password
2. Password is hashed using bcrypt
3. User account created with `is_verified=false`

### Email/Password Login
1. `POST /api/v1/auth/login` with credentials
2. Password verified against hash
3. JWT token returned

### Google Authentication
1. Frontend authenticates with Firebase
2. `POST /api/v1/auth/google-auth` with Firebase token
3. Backend verifies token with Firebase Admin SDK
4. User created/retrieved and JWT token returned

## Development Commands

```bash
# Run development server with auto-reload
uvicorn main:app --reload

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run with Docker
docker build -t maplepath-api .
docker run -p 8000:8080 maplepath-api
```

## Migration from Node.js

This backend was migrated from Node.js/Express/Prisma to FastAPI/SQLAlchemy/Alembic:

### What was removed:
- All Node.js files (package.json, index.js, src/, node_modules/)
- Prisma ORM and schema files
- Express.js routing and middleware

### What was added:
- FastAPI application with modern Python async/await
- SQLAlchemy ORM with Alembic migrations
- Pydantic schemas for request/response validation
- Structured service layer architecture
- Firebase Admin SDK integration
- JWT authentication with python-jose

The new FastAPI backend provides better performance, type safety, automatic API documentation, and easier deployment to Cloud Run.
