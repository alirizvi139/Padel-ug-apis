# PadelUG API

A FastAPI-based REST API for PadelUG with MongoDB integration and CRUD operations.

## Features

- FastAPI framework for high-performance API
- MongoDB integration with Motor (async driver)
- User CRUD operations with name, title, and points
- Environment-based configuration
- Docker support

## Project Structure

```
PadelUG/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── api/
│   │   └── users.py
│   └── services/
│       ├── __init__.py
│       └── crud_service.py
├── requirements.txt
├── env.example
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PadelUG
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your MongoDB connection details
   ```

5. **Start MongoDB**
   ```bash
   # Make sure MongoDB is running on your system
   # Or use Docker: docker run -d -p 27017:27017 mongo:latest
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## Environment Variables

- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `API_HOST`: API host address
- `API_PORT`: API port number
- `DEBUG`: Debug mode flag

## API Endpoints

### Users (`/api/users`)
- `POST /` - Create a new user
- `GET /` - Get all users (with pagination)
- `GET /{id}` - Get a specific user
- `PUT /{id}` - Update a user
- `DELETE /{id}` - Delete a user

## Development

The project follows a clean architecture pattern:
- **Models**: Database models (User with name, title, points)
- **Services**: Business logic layer
- **API**: Route handlers and endpoints
- **Config**: Application configuration 