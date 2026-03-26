from fastapi import FastAPI
from .services.sqlite import Task, create, read, read_item, update, delete, delete_item
from fastapi.middleware.cors import CORSMiddleware
from .config import validation
from .model.schemas import TaskSchema


app = FastAPI()

origins = [
    "http://localhost.com",
    "https://localhost.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    try:
        validation()
    except ValueError as e:
        print(f"Error during startup: {e}")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/", response_model=TaskSchema)
def create_item(payload: TaskSchema):
    create(payload)
    return {
        "details": "Item criado",
        "id": payload.id,
        "description": payload.description,
        "status": payload.status
    }

@app.get("/items/{id}")
def get_item(id: int):
    return read_item(id)

@app.get("/items/")
def get_items():
    return read()

@app.put("/items/{id}", response_model=TaskSchema)
def update_item(id: int, payload: TaskSchema):
    update(id, payload)
    return {
        "details": "item atualizado",
        "id": id,
        "description": payload.description,
        "status": payload.status
    }

@app.delete("/items/{id}")
def remove_item(id: int):
    delete_item(id)
    return {
        "details": "item deletado",
        "id": id,
    }

@app.delete("/items/")
def remove_all_items():
    delete()
    return {"message": "All items deleted"}