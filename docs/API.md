# API Documentation

Detailed documentation of all endpoints in the Backend To-Do List API.

## Base URL

```
http://localhost:8000
```

## Response Format

All responses are in JSON format. Each response includes the appropriate HTTP status code.

## Endpoints

### 1. Health Check

#### GET /

Check if the API is running.

**Description**: Returns a welcome message to verify the API is accessible.

**Method**: GET

**URL**: `/`

**Request Headers**: None

**Request Body**: None

**Response Status**: 200 OK

**Response Example**:
```json
{
  "message": "Hello World"
}
```

---

### 2. Create Task

#### POST /

Create a new task in the database.

**Description**: Adds a new task to the to-do list. The `id` field is optional (server generates it automatically).

**Method**: POST

**URL**: `/`

**Request Headers**:
```
Content-Type: application/json
```

**Request Body Schema**:
```typescript
{
  "id": number | null,        // Optional, auto-generated
  "title": string | null,     // Optional
  "description": string | null, // Optional
  "status": boolean           // Required
}
```

**Request Example**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": true
}
```

**Response Status**: 200 OK

**Response Body**:
```json
{
  "details": "Item criado",
  "id": 1,
  "description": "Milk, eggs, bread",
  "status": true
}
```

**Error Cases**:
- Missing required field `status`: 422 Unprocessable Entity

---

### 3. Get All Tasks

#### GET /items/

Retrieve all tasks from the database.

**Description**: Returns a list of all tasks stored in the database.

**Method**: GET

**URL**: `/items/`

**Request Headers**: None

**Request Body**: None

**Query Parameters**: None

**Response Status**: 200 OK

**Response Body**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": true
  },
  {
    "id": 2,
    "title": "Complete project",
    "description": "Finish documentation",
    "status": false
  }
]
```

**Empty Response** (no tasks):
```json
[]
```

---

### 4. Get Specific Task

#### GET /items/{id}

Retrieve a single task by its ID.

**Description**: Returns details of a specific task.

**Method**: GET

**URL**: `/items/{id}`

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | The ID of the task to retrieve |

**Request Headers**: None

**Request Body**: None

**Response Status**: 200 OK

**Response Example**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": true
}
```

**Error Cases**:
- Task not found: Returns `null`
- Invalid ID (non-integer): 422 Unprocessable Entity

---

### 5. Update Task

#### PUT /items/{id}

Update an existing task.

**Description**: Modifies a task's properties. All fields in the request body will be updated.

**Method**: PUT

**URL**: `/items/{id}`

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | The ID of the task to update |

**Request Headers**:
```
Content-Type: application/json
```

**Request Body Schema**:
```typescript
{
  "id": number | null,
  "title": string | null,
  "description": string | null,
  "status": boolean
}
```

**Request Example**:
```json
{
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread, vegetables",
  "status": false
}
```

**Response Status**: 200 OK

**Response Body**:
```json
{
  "details": "item atualizado",
  "id": 1,
  "description": "Milk, eggs, bread, vegetables",
  "status": false
}
```

**Error Cases**:
- Task not found: Will return an error
- Invalid ID: 422 Unprocessable Entity
- Invalid request body: 422 Unprocessable Entity

---

### 6. Delete Specific Task

#### DELETE /items/{id}

Delete a single task by its ID.

**Description**: Removes a specific task from the database.

**Method**: DELETE

**URL**: `/items/{id}`

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | The ID of the task to delete |

**Request Headers**: None

**Request Body**: None

**Response Status**: 200 OK

**Response Example**:
```json
{
  "details": "item deletado",
  "id": 1
}
```

**Error Cases**:
- Task not found: May return an error
- Invalid ID: 422 Unprocessable Entity

---

### 7. Delete All Tasks

#### DELETE /items/

Delete all tasks from the database.

**Description**: Removes all tasks permanently. This action cannot be undone.

**Method**: DELETE

**URL**: `/items/`

**Request Headers**: None

**Request Body**: None

**Response Status**: 200 OK

**Response Example**:
```json
{
  "message": "All items deleted"
}
```

⚠️ **Warning**: This operation deletes all tasks. Use with caution.

---

## Common Response Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 422 | Unprocessable Entity - Invalid request data or missing required fields |
| 500 | Internal Server Error - Server error occurred |

## Request/Response Examples

### Complete Workflow

**1. Create a task**:
```bash
POST /
Content-Type: application/json

{
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "status": true
}
```

Response:
```json
{
  "details": "Item criado",
  "id": 1,
  "description": "Complete the FastAPI tutorial",
  "status": true
}
```

**2. Get all tasks**:
```bash
GET /items/
```

Response:
```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "status": true
  }
]
```

**3. Update the task**:
```bash
PUT /items/1
Content-Type: application/json

{
  "title": "Learn FastAPI and Advanced Concepts",
  "description": "Complete the full FastAPI tutorial and learn advanced patterns",
  "status": false
}
```

Response:
```json
{
  "details": "item atualizado",
  "id": 1,
  "description": "Complete the full FastAPI tutorial and learn advanced patterns",
  "status": false
}
```

**4. Delete the task**:
```bash
DELETE /items/1
```

Response:
```json
{
  "details": "item deletado",
  "id": 1
}
```

## CORS Policy

The API is configured to accept requests from the following origins:
- `http://localhost.com`
- `https://localhost.com`
- `http://localhost`
- `http://localhost:8080`

All HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, etc.) are allowed from these origins.

To add more origins, modify the `origins` list in [main.py](src/backend_to_do_list/main.py).

## Testing the API

### Using cURL

```bash
# Get all tasks
curl http://localhost:8000/items/

# Create a task
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","description":"Task details","status":true}'

# Get a specific task
curl http://localhost:8000/items/1

# Update a task
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","description":"Updated description","status":false}'

# Delete a task
curl -X DELETE http://localhost:8000/items/1

# Delete all tasks
curl -X DELETE http://localhost:8000/items/
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a task
response = requests.post(f"{BASE_URL}/", json={
    "title": "My Task",
    "description": "Task details",
    "status": True
})
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/items/")
print(response.json())

# Get a specific task
response = requests.get(f"{BASE_URL}/items/1")
print(response.json())

# Update a task
response = requests.put(f"{BASE_URL}/items/1", json={
    "title": "Updated Title",
    "description": "Updated description",
    "status": False
})
print(response.json())

# Delete a task
response = requests.delete(f"{BASE_URL}/items/1")
print(response.json())
```

## Rate Limiting

Currently, there is no rate limiting implemented. The API will process all requests as they arrive.

## Authentication

Currently, the API has no authentication mechanism. All endpoints are publicly accessible.

## Versioning

The current API version is `0.1.0` (development version).

Future versions may include:
- API versioning (v1, v2, etc.)
- Authentication and authorization
- Enhanced filtering and pagination
- Rate limiting
