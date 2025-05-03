# Task Management Service

A RESTful API service for managing tasks built with FastAPI, PostgreSQL, and JWT authentication.

## 📋 Features

- **User Authentication**
  - Registration with secure password hashing
  - JWT-based authentication with access and refresh tokens
  - Token refresh mechanism

- **Task Management**
  - Create, retrieve, update and search tasks
  - Task prioritization
  - Task status tracking

- **Security**
  - Password hashing with bcrypt
  - JWT token validation
  - Protected API endpoints

## 🏗️ Tech Stack

- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation and settings management
- **JWT**: JSON Web Tokens for authentication
- **Docker & Docker Compose**: Containerization and multi-container orchestration
- **Pytest**: Testing framework

## 🏛️ Architecture

```
app/
├── api/              # API endpoints
│   ├── auth.py       # Authentication routes
│   └── tasks.py      # Task management routes
├── core/             # Core functionality
│   └── security.py   # Security utilities (JWT, password hashing)
├── crud/             # CRUD operations
│   ├── task.py       # Task database operations
│   └── user.py       # User database operations
├── db/               # Database configuration
│   ├── base.py       # Database connection setup
│   └── session.py    # Database session management
├── models/           # SQLAlchemy models
│   ├── task.py       # Task model
│   └── user.py       # User model
├── schemas/          # Pydantic schemas/models
│   ├── auth.py       # Authentication schemas
│   ├── task.py       # Task schemas
│   └── user.py       # User schemas
└── main.py           # FastAPI application entry point
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-service.git
   cd task-service
   ```

2. Create a `.env` file in the root directory (optional, defaults are provided in config.py):
   ```
   DATABASE_URL=postgresql://postgres:123456@db:5432/task_service
   JWT_SECRET_KEY=your-secret-key-change-in-production
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

3. Build and run the containers:
   ```bash
   docker-compose up -d
   ```

4. The API is now running at `http://localhost:8000`

## 📝 API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### Authentication

- `POST /register` - Register a new user
- `POST /login` - Login and get access/refresh tokens  
- `POST /refresh` - Refresh access token

#### Task Management

- `GET /tasks` - Get all tasks for authenticated user
- `GET /tasks/{task_id}` - Get a specific task
- `GET /tasks/search?q={query}` - Search tasks by title or description
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task

## 🔒 Authentication Flow

1. **Registration**: Create a user account with email and password
2. **Login**: Exchange credentials for access and refresh tokens
3. **API Access**: Include the access token in the Authorization header
   ```
   Authorization: Bearer <access_token>
   ```
4. **Token Refresh**: When the access token expires, use the refresh token to get a new one

## 🧪 Running Tests

```bash
# Inside the container
docker-compose exec web pytest

# Or directly if you have the dependencies installed locally
pytest
```

## 🛠️ Development Environment

For local development without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL locally and update the DATABASE_URL in `.env`

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📊 Database Schema

### Users Table
```
id: Integer (PK)
name: String(100)
email: String(100) (Unique)
hashed_password: String(100)
created_at: DateTime
```

### Tasks Table
```
id: Integer (PK)
title: String(200)
description: Text
status: Enum('pending', 'done')
priority: Integer
created_at: DateTime
owner_id: Integer (FK to users.id)
```

## 🔧 Configuration

Configuration settings are managed via environment variables and the `config.py` file:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `JWT_ALGORITHM`: Algorithm for JWT token (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token lifetime
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token lifetime

## 🔍 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
