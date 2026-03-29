# Backend To-Do List API

A RESTful API for managing to-do list items built with FastAPI and SQLite.

## Project Information

- **Name**: backend-to-do-list
- **Version**: 0.1.0
- **Author**: Leonardo de Almeida (leo70x7000@gmail.com)
- **Python Version**: ≥ 3.14

## Overview

This is a simple but efficient backend API for managing tasks/to-do items. It provides endpoints for creating, reading, updating, and deleting tasks. The API is built with FastAPI for high performance and includes CORS middleware support for cross-origin requests.

## Features

- ✅ Create new tasks
- ✅ Read all tasks or a specific task
- ✅ Update existing tasks
- ✅ Delete tasks individually or all at once
- ✅ SQLite database persistence
- ✅ CORS enabled for frontend integration
- ✅ Pydantic validation for request/response schemas

## Tech Stack

- **Framework**: FastAPI ≥ 0.135.2
- **Server**: Uvicorn ≥ 0.42.0
- **ORM**: SQLAlchemy ≥ 2.0.48
- **Database**: SQLite
- **Validation**: Pydantic ≥ 2.13.1
- **Environment**: python-dotenv ≥ 1.2.2
- **Database Driver**: psycopg2 ≥ 2.9.11

## Project Structure

```
backend_to_do_list/
├── src/
│   └── backend_to_do_list/
│       ├── __init__.py
│       ├── main.py                 # FastAPI application and routes
│       ├── config.py               # Configuration and environment validation
│       ├── model/
│       │   ├── __init__.py
│       │   └── schemas.py          # Pydantic schemas for validation
│       └── services/
│           ├── __init__.py
│           └── sqlite.py           # Database models and CRUD operations
├── pyproject.toml                  # Project metadata and dependencies
├── .env                            # Environment variables
└── README.md                       # This file
```

## Installation

### Prerequisites

- Python 3.14 or higher
- pip or Poetry package manager

### Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd backend_to_do_list
   ```

2. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

3. **Configure environment variables**:
   Create or update the `.env` file:
   ```env
   DATABASE_URL=sqlite:///database.db
   ```

## Running the Application

### Start the development server

```bash
python -m poetry run uvicorn src.backend_to_do_list.main:app --reload
```

The API will be available at `http://localhost:8000`

### Access Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

#### GET /
Returns a welcome message.

**Response** (200):
```json
{
  "message": "Hello World"
}
```

---

### Tasks Management

#### POST /
Create a new task.

**Request Body**:
```json
{
  "id": null,
  "title": "Task Title",
  "description": "Task description",
  "status": true
}
```

**Response** (200):
```json
{
  "details": "Item criado",
  "id": 1,
  "description": "Task description",
  "status": true
}
```

---

#### GET /items/
Retrieve all tasks.

**Response** (200):
```json
[
  {
    "id": 1,
    "title": "Task 1",
    "description": "Description 1",
    "status": true
  },
  {
    "id": 2,
    "title": "Task 2",
    "description": "Description 2",
    "status": false
  }
]
```

---

#### GET /items/{id}
Retrieve a specific task by ID.

**Parameters**:
- `id` (integer, required): Task ID

**Response** (200):
```json
{
  "id": 1,
  "title": "Task 1",
  "description": "Description 1",
  "status": true
}
```

---

#### PUT /items/{id}
Update a task by ID.

**Parameters**:
- `id` (integer, required): Task ID

**Request Body**:
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "status": false
}
```

**Response** (200):
```json
{
  "details": "item atualizado",
  "id": 1,
  "description": "Updated description",
  "status": false
}
```

---

#### DELETE /items/{id}
Delete a specific task by ID.

**Parameters**:
- `id` (integer, required): Task ID

**Response** (200):
```json
{
  "details": "item deletado",
  "id": 1
}
```

---

#### DELETE /items/
Delete all tasks.

**Response** (200):
```json
{
  "message": "All items deleted"
}
```

## Database Schema

### Tasks Table

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | INTEGER | Unique task identifier | Primary Key, Auto-increment |
| title | VARCHAR | Task title | - |
| description | VARCHAR | Task description | - |
| status | BOOLEAN | Task completion status | - |

The table is automatically created when the application starts.

## Data Models

### TaskSchema

Pydantic schema for request/response validation:

```python
class TaskSchema(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    status: bool
```

**Fields**:
- `id`: Optional task identifier
- `title`: Optional task title
- `description`: Optional task description
- `status`: Task completion status (required)

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///database.db`)

### CORS Configuration

The application allows requests from the following origins:
- `http://localhost.com`
- `https://localhost.com`
- `http://localhost`
- `http://localhost:8080`

**CORS Methods**: All methods allowed (`*`)
**CORS Headers**: All headers allowed (`*`)

## Error Handling

### Validation Error

If required environment variables are missing during startup:
```
Error during startup: {error message}
```

### Database Errors

Database operations are handled by SQLAlchemy. Ensure the database URL is correctly configured in the `.env` file.

## Development

### Running Tests

To run tests (if available):
```bash
pytest
```

### Code Style

The project follows standard Python conventions. Consider using:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

## Troubleshooting

### Issue: `DATABASE_URL` not found
**Solution**: Ensure the `.env` file exists in the project root with the correct `DATABASE_URL` configuration.

### Issue: Port 8000 already in use
**Solution**: Specify a different port:
```bash
uvicorn src.backend_to_do_list.main:app --reload --port 8001
```

### Issue: Module not found errors
**Solution**: Ensure you're running the command from the project root directory and Poetry dependencies are installed.

## License

This project is part of academic coursework for a DevOps class.

## Contact

For questions or support, contact the author:
- **Name**: Leonardo de Almeida
- **Email**: leo70x7000@gmail.com
