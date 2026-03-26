# Setup and Installation Guide

Complete guide to set up and run the Backend To-Do List application.

## System Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python Version**: 3.14 or higher
- **RAM**: Minimum 2GB (recommended 4GB)
- **Storage**: At least 500MB free space
- **Database**: SQLite (automatic, no separate installation needed)

## Installation Steps

### Step 1: Prerequisites

Ensure you have Python 3.14+ installed:

```bash
python --version
```

If not, download from [python.org](https://www.python.org/downloads/)

### Step 2: Clone/Navigate to Project

```bash
cd path/to/backend_to_do_list
```

### Step 3: Create Virtual Environment (Recommended)

Using venv:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

The project uses Poetry for dependency management, but supports both Poetry and pip.

#### Option A: Using Poetry (Recommended)

```bash
# Install Poetry if not already installed
pip install poetry

# Install dependencies
poetry install
```

#### Option B: Using pip

```bash
# Install from pyproject.toml
pip install fastapi uvicorn sqlalchemy psycopg2 psycopg2-binary pydantic-settings python-dotenv
```

Or create a `requirements.txt` first:

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

1. Create a `.env` file in the project root (if it doesn't exist):

```bash
# On Windows
type nul > .env

# On Linux/macOS
touch .env
```

2. Add the following content:

```env
DATABASE_URL=sqlite:///database.db
```

### Step 6: Verify Installation

Run the following to verify all dependencies are installed:

```bash
python -c "import fastapi, sqlalchemy, uvicorn; print('All dependencies installed!')"
```

## Running the Application

### Start the Development Server

```bash
# Using Poetry
poetry run uvicorn src.backend_to_do_list.main:app --reload

# Or directly with Python
uvicorn src.backend_to_do_list.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Access the Application

**API Base URL**: `http://localhost:8000`

**Interactive Endpoints**:
- **Swagger UI (Recommended)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Stop the Server

Press `CTRL+C` in the terminal.

## Database Setup

The database is automatically created on first run:

1. A `database.db` file will be created in the project root
2. Required tables are automatically initialized
3. No manual database setup is needed

### Verify Database Creation

```bash
# Check if database.db exists
ls -la database.db   # Linux/macOS
dir database.db      # Windows
```

## Configuration Options

### Custom Database Location

Edit `.env`:

```env
DATABASE_URL=sqlite:///path/to/your/database.db
```

### Custom Port

```bash
uvicorn src.backend_to_do_list.main:app --reload --port 8001
```

### Production Mode (without auto-reload)

```bash
uvicorn src.backend_to_do_list.main:app
```

### Host Binding

```bash
# Listen on all network interfaces
uvicorn src.backend_to_do_list.main:app --host 0.0.0.0 --port 8000
```

## Using Different Databases (Alternative Setup)

While the default is SQLite, you can use other databases by changing `DATABASE_URL`:

### PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

Install additional driver:
```bash
pip install psycopg2-binary
```

### MySQL

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
```

Install additional driver:
```bash
pip install pymysql
```

## Testing the Installation

### Test Basic Endpoints

**Using cURL**:

```bash
# Health check
curl http://localhost:8000/

# Expected: {"message": "Hello World"}

# Create a task
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test Task\",\"description\":\"Testing installation\",\"status\":true}"

# Get all tasks
curl http://localhost:8000/items/
```

**Using Python**:

```python
import requests

# Test connection
response = requests.get("http://localhost:8000/")
print(response.json())  # {"message": "Hello World"}

# Create a task
task_data = {
    "title": "Test Task",
    "description": "Testing installation",
    "status": True
}
response = requests.post("http://localhost:8000/", json=task_data)
print(response.json())
```

## Troubleshooting

### Issue: "Module not found" Error

**Solution**: Ensure you're in the correct directory and dependencies are installed:

```bash
# Verify current directory
pwd  # Linux/macOS
cd   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Address already in use" Error

**Solution**: The port is in use. Use a different port:

```bash
uvicorn src.backend_to_do_list.main:app --reload --port 8001
```

Or kill the process using port 8000:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

### Issue: "DATABASE_URL not found" Error

**Solution**: Ensure `.env` file exists with the correct content:

```bash
# Windows
echo DATABASE_URL=sqlite:///database.db > .env

# Linux/macOS
echo "DATABASE_URL=sqlite:///database.db" > .env
```

Restart the server.

### Issue: Database Permission Denied

**Solution**: Ensure the directory has write permissions:

```bash
# Linux/macOS
chmod 755 .

# Windows - Run as Administrator or change folder properties
```

### Issue: Python Version Not Compatible

Make sure you have Python 3.14+:

```bash
python --version

# If you have multiple Python versions
python3.14 -m venv venv
```

## Uninstallation

To remove the application:

```bash
# Remove virtual environment
rmvirtualenv venv  # If using virtualenvwrapper
rm -rf venv        # Or manually delete the folder

# Remove database
rm database.db     # Linux/macOS
del database.db    # Windows

# Remove project folder
rm -rf backend_to_do_list  # Entire project
```

## Next Steps

1. Read the [API Documentation](API.md)
2. Explore the [README.md](README.md)
3. Check the [Architecture](ARCHITECTURE.md) document

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Uvicorn Documentation**: https://www.uvicorn.org/

## Support

For issues or questions, contact: leo70x7000@gmail.com
