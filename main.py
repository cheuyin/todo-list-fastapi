from fastapi import FastAPI, HTTPException
import uuid
from pathlib import Path
from models.todo import Todo, TodoCreate, TodoUpdate
from repository.todo_repository import TodoRepository

project_root = Path(__file__).resolve().parent
STORE_PATH = project_root / "store" / "todo.json"

todoRepo = TodoRepository(STORE_PATH)

app = FastAPI()


@app.get("/todos", response_model=list[Todo])
def read_todos():
    return todoRepo.get_all()


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str):
    try:
        return todoRepo.get(todo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item not found")


@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = str(uuid.uuid4())
    new_todo_dict = todo.model_dump()
    new_todo_dict["id"] = new_todo_id
    new_todo = Todo(**new_todo_dict)
    todoRepo.add(new_todo)
    return new_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoUpdate):
    try:
        existing_todo_dict = todoRepo.get(todo_id).model_dump()
        existing_todo_dict.update(todo.model_dump(exclude_unset=True))
        return todoRepo.update(Todo(**existing_todo_dict))
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
