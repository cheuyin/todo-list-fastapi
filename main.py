from fastapi import FastAPI, HTTPException, status
import uuid
from pathlib import Path
from models.todo import Todo, TodoCreate, TodoUpdate
from repository.todo_repository import TodoRepository

project_root = Path(__file__).resolve().parent
STORE_PATH = project_root / "store" / "todo.json"

todo_repo = TodoRepository(STORE_PATH)

app = FastAPI(title="Todo API")


@app.get("/todos", response_model=list[Todo])
def read_todos():
    return todo_repo.get_all()


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: str):
    try:
        return todo_repo.get(todo_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    new_todo = Todo(id=str(uuid.uuid4()), **todo.model_dump())
    todo_repo.add(new_todo)
    return new_todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoUpdate):
    try:
        existing_todo_dict = todo_repo.get(todo_id).model_dump()
        existing_todo_dict.update(todo.model_dump(exclude_unset=True))
        return todo_repo.update(Todo(**existing_todo_dict))
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: str):
    try:
        return todo_repo.delete(todo_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
