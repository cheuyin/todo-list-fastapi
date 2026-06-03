from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import uuid

app = FastAPI()


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


todos: dict[str, Todo] = {}


@app.get("/todos", response_model=list[Todo])
def read_todos():
    return list(todos.values())


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str):
    try:
        return todos[todo_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item not found")


@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    random_id = str(uuid.uuid4())
    new_todo_json = todo.model_dump()
    new_todo_json["id"] = random_id
    new_todo = Todo(**new_todo_json)
    todos[random_id] = new_todo
    return todos[random_id]


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoUpdate):
    try:
        stored_todo = todos[todo_id]
        update_data = todo.model_dump(exclude_unset=True)
        updated_todo = stored_todo.model_copy(update=update_data)
        todos[todo_id] = updated_todo
        return updated_todo
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
