from pydantic import BaseModel


class Todo(BaseModel):
    id: str
    title: str
    description: str | None = None
    is_completed: bool


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
