from pydantic import BaseModel, ConfigDict

class TaskSchema(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    status: bool

    model_config = ConfigDict(from_attributes=True)