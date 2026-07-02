from fastapi import FastAPI, HTTPException
from .services.database import Task, create, read, read_item, update, delete, delete_item
from fastapi.middleware.cors import CORSMiddleware
from .config import validation
from .model.schemas import TaskSchema


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
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


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ATENÇÃO: rota sem parâmetro DEVE vir antes da rota com parâmetro
# para o FastAPI não interpretar /items/ como /items/{id}
@app.get("/items/")
def get_items():
    return read()


@app.delete("/items/")
def remove_all_items():
    delete()
    return {"message": "All items deleted"}


@app.post("/")
def create_item(payload: TaskSchema):
    item = create(payload)          # create() agora retorna o objeto com id gerado
    return {
        "details": "Item criado",
        "id": item.id,              # id real do banco, não payload.id
        "description": item.description,
        "status": item.status
    }


@app.get("/items/{id}")
def get_item(id: int):
    item = read_item(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@app.put("/items/{id}")
def update_item(id: int, payload: TaskSchema):
    item = read_item(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    update(id, payload)
    return {
        "details": "item atualizado",
        "id": id,
        "description": payload.description,
        "status": payload.status
    }


@app.delete("/items/{id}")
def remove_item(id: int):
    item = read_item(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    delete_item(id)
    return {
        "details": "item deletado",
        "id": id,
    }
