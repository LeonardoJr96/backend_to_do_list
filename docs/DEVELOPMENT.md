# Development Guidelines

Best practices, coding standards, and contribution guidelines for the Backend To-Do List project.

## Table of Contents

1. [Code Style & Standards](#code-style--standards)
2. [Development Workflow](#development-workflow)
3. [Testing](#testing)
4. [Common Tasks](#common-tasks)
5. [Debugging](#debugging)
6. [Performance Tips](#performance-tips)
7. [Security](#security)

## Code Style & Standards

### Python Code Style

Follow **PEP 8** standards:

```python
# Good - Clear variable names, proper spacing
def create_task(title: str, description: str, status: bool) -> Task:
    task = Task(title=title, description=description, status=status)
    session.add(task)
    session.commit()
    return task


# Bad - Unclear naming, improper spacing
def ct(t,d,s):
    tsk=Task(title=t,description=d,status=s)
    session.add(tsk);session.commit()
    return tsk
```

### File Organization

```python
# 1. Imports (stdlib, third-party, local)
import os
from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import create_engine

from src.backend_to_do_list.config import DATABASE_URL

# 2. Constants
APP_VERSION = "0.1.0"
MAX_TITLE_LENGTH = 100

# 3. Classes
class Task:
    pass

# 4. Functions
def create_task():
    pass

# 5. Main execution
if __name__ == "__main__":
    app.run()
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | snake_case | `user_id`, `task_title` |
| Functions | snake_case | `create_task()`, `delete_item()` |
| Classes | PascalCase | `TaskSchema`, `Task` |
| Constants | UPPER_SNAKE_CASE | `MAX_TASKS`, `DATABASE_URL` |
| Private | _leading_underscore | `_internal_function()` |

### Documentation

#### Docstrings

```python
def create(payload):
    """
    Create a new task in the database.
    
    Args:
        payload (TaskSchema): Task data to create
        
    Returns:
        None
        
    Raises:
        SQLAlchemyError: If database operation fails
    """
    data = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status
    )
    session.add(data)
    session.commit()
```

#### Comments

```python
# Good - Explains WHY, not WHAT
# Filter active tasks only to improve performance
active_tasks = session.query(Task).filter(Task.status == True).all()

# Bad - Explains WHAT (obvious from code)
# Get tasks where status is True
active_tasks = session.query(Task).filter(Task.status == True).all()
```

### Type Hints

Always use type hints:

```python
# Good
def read_item(id: int) -> Task | None:
    return session.query(Task).filter(Task.id == id).first()

# Acceptable (older Python)
def read_item(id: int) -> Optional[Task]:
    return session.query(Task).filter(Task.id == id).first()

# Avoid
def read_item(id):
    return session.query(Task).filter(Task.id == id).first()
```

## Development Workflow

### Local Development Setup

```bash
# 1. Clone repository and navigate
cd backend_to_do_list

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -e .

# 4. Create .env file
echo "DATABASE_URL=sqlite:///database.db" > .env

# 5. Run development server
uvicorn src.backend_to_do_list.main:app --reload
```

### Creating a New Endpoint

#### 1. Define Schema (model/schemas.py)
```python
from pydantic import BaseModel

class TaskCreateSchema(BaseModel):
    title: str
    description: str
    status: bool
```

#### 2. Create Service Function (services/sqlite.py)
```python
def create_task_advanced(payload: TaskCreateSchema) -> Task:
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status
    )
    session.add(task)
    session.commit()
    return task
```

#### 3. Add Route (main.py)
```python
@app.post("/api/v1/tasks", response_model=TaskSchema)
async def create_new_task(payload: TaskCreateSchema):
    task = create_task_advanced(payload)
    return task
```

#### 4. Test the Endpoint
```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","description":"Test","status":true}'
```

### Adding a New Database Column

#### 1. Update Model (services/sqlite.py)
```python
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    description = Column("description", String)
    status = Column("status", Boolean)
    created_at = Column("created_at", DateTime, default=datetime.now)  # NEW
```

#### 2. Update Schema (model/schemas.py)
```python
class TaskSchema(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    status: bool
    created_at: datetime | None = None  # NEW
```

#### 3. Update CRUD Functions
```python
def create(payload):
    data = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        # created_at is auto-populated
    )
    session.add(data)
    session.commit()
```

#### 4. Verify
```bash
# Database will be recreated with new schema
rm database.db  # Delete old DB
# Restart server - new DB created automatically
```

## Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:8000/

# Create task
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test task","status":true}'

# Get all tasks
curl http://localhost:8000/items/

# Get specific task
curl http://localhost:8000/items/1

# Update task
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","description":"Updated task","status":false}'

# Delete task
curl -X DELETE http://localhost:8000/items/1

# Delete all
curl -X DELETE http://localhost:8000/items/
```

### Testing with Python

```python
# test_api.py
import requests

BASE_URL = "http://localhost:8000"

def test_get_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_task():
    payload = {
        "title": "Test Task",
        "description": "A test task",
        "status": True
    }
    response = requests.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    return data["id"]

def test_get_all_tasks():
    response = requests.get(f"{BASE_URL}/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    task_id = test_create_task()
    payload = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": False
    }
    response = requests.put(f"{BASE_URL}/items/{task_id}", json=payload)
    assert response.status_code == 200

def test_delete_task():
    task_id = test_create_task()
    response = requests.delete(f"{BASE_URL}/items/{task_id}")
    assert response.status_code == 200

if __name__ == "__main__":
    test_get_root()
    test_create_task()
    test_get_all_tasks()
    test_update_task()
    test_delete_task()
    print("All tests passed!")
```

Run tests:
```bash
python test_api.py
```

### Testing with pytest (Recommended)

```python
# tests/test_api.py
import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture
def setup_teardown():
    # Setup
    yield
    # Teardown - clean up test data
    requests.delete(f"{BASE_URL}/items/")

def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200

def test_create_and_retrieve_task(setup_teardown):
    # Create
    task_data = {
        "title": "Test Task",
        "description": "Test",
        "status": True
    }
    create_response = requests.post(f"{BASE_URL}/", json=task_data)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]
    
    # Retrieve
    get_response = requests.get(f"{BASE_URL}/items/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
```

Install and run:
```bash
pip install pytest
pytest tests/
```

## Common Tasks

### Update Dependencies

```bash
# Check outdated packages
pip list --outdated

# Update one package
pip install --upgrade fastapi

# Update all packages
pip install --upgrade -r requirements.txt

# Freeze current versions
pip freeze > requirements.txt
```

### Reset Database

```bash
# Delete the database file
rm database.db  # Linux/macOS
del database.db # Windows

# Restart the server - new DB will be created
uvicorn src.backend_to_do_list.main:app --reload
```

### Change Database

Edit `.env`:
```env
# SQLite
DATABASE_URL=sqlite:///database.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/db_name

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/db_name
```

## Debugging

### Enable Debug Mode

```python
# main.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/")
def create_item(payload: TaskSchema):
    logger.debug(f"Creating task: {payload}")
    # ... rest of code
```

### Log Database Queries

```python
# services/sqlite.py
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Now all SQL queries will be logged
```

### Debug with Print Statements

```python
# Temporary debugging
def create(payload):
    print(f"DEBUG: Creating task with payload: {payload}")
    data = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status
    )
    print(f"DEBUG: Task object created: {data}")
    session.add(data)
    session.commit()
    print(f"DEBUG: Task committed with id: {data.id}")
```

### Using Python Debugger (pdb)

```python
def create(payload):
    import pdb; pdb.set_trace()
    # Execution pauses here
    data = Task(...)
    # Commands: n (next), s (step), c (continue), p (print var)
```

### Check Database Contents

```bash
# SQLite shell
sqlite3 database.db

# Commands:
# .tables              - List tables
# .schema tasks        - Show table structure
# SELECT * FROM tasks; - View all data
# .exit               - Exit
```

## Performance Tips

### Query Optimization

```python
# Bad - Inefficient
def get_status_count():
    all_tasks = session.query(Task).all()
    return len([t for t in all_tasks if t.status])

# Good - Efficient with database filtering
def get_status_count():
    count = session.query(Task).filter(Task.status == True).count()
    return count
```

### Add Indexes

```python
# services/sqlite.py
class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_title', 'title'),
    )
```

### Connection Pooling

```python
# services/sqlite.py
from sqlalchemy.pool import QueuePool

db = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Pagination for Large Results

```python
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):
    items = session.query(Task).offset(skip).limit(limit).all()
    return items

# Usage: /items/?skip=0&limit=10
```

## Security

### Environment Variables

✅ **Always use environment variables for sensitive data:**

```python
# Good
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")

# Bad - Don't hardcode!
database_url = "postgresql://user:password@localhost:5432/db"
```

### Input Validation

✅ **Pydantic validates automatically:**

```python
class TaskSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    status: bool  # Required
    
    # Custom validation
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        return v
```

### SQL Injection Prevention

✅ **SQLAlchemy ORM prevents SQL injection:**

```python
# Safe - ORM handles parameterization
task = session.query(Task).filter(Task.id == id).first()

# Avoid - Raw SQL (vulnerable!)
query = f"SELECT * FROM tasks WHERE id = {id}"
```

### HTTPS in Production

```bash
# Use certificates (Let's Encrypt free)
uvicorn src.backend_to_do_list.main:app \
  --ssl-keyfile=/path/to/key.pem \
  --ssl-certfile=/path/to/cert.pem \
  --host 0.0.0.0 \
  --port 443
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/", dependencies=[Depends(limiter.limit("5/minute"))])
def create_item(payload: TaskSchema):
    # Limited to 5 requests per minute
    pass
```

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

## Getting Help

- Read the [README.md](README.md)
- Check [API.md](API.md) for endpoint details
- Review [SETUP.md](SETUP.md) for installation
- Study [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## Questions?

Contact: leo70x7000@gmail.com
