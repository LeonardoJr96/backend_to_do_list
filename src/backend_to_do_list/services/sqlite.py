from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from src.backend_to_do_list.config import DATABASE_URL

db = create_engine(DATABASE_URL)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    description = Column("description", String)
    status = Column("status", Boolean)

    def __init__(self, title=None, description=None, status=True):
        self.title = title
        self.description = description
        self.status = status

Base.metadata.create_all(bind=db)

def create(payload):
    'Função de criar tasks no banco'

    data = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status
    )

    session.add(data)
    session.commit()

def read():
    'Função de ler tasks no banco'
    data = session.query(Task).all()
    return data

def read_item(id: int):
    'Função de ler task no banco'

    data = session.query(Task).filter(Task.id == id).first()
    return data

def update(id: int, payload):
    'Função de atualizar tasks no banco'

    data = session.query(Task).filter(Task.id == id).first()

    data.title = payload.title
    data.description = payload.description
    data.status = payload.status

    session.add(data)
    session.commit()

def delete():
    'Função de deletar tasks no banco'

    session.query(Task).delete()
    session.commit()

def delete_item(id: int):
    'Função de deletar tasks no banco'

    data = session.query(Task).filter(Task.id == id).first()
    session.delete(data)
    session.commit()