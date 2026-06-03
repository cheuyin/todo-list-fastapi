from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import uuid

app = FastAPI()


class Todo(BaseModel):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    is_completed: bool = False


todos = {}


@app.get("/todos")
def read_todos():
    return list(todos.values())


@app.get("/todos/{todo_id}")
def read_todo(todo_id: str):
    try:
        return todos[todo_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Item not found")


@app.post("/todos")
def create_todo(todo: Todo):
    random_id = str(uuid.uuid4())
    incoming_todo = jsonable_encoder(todo)
    incoming_todo["id"] = random_id
    todos[random_id] = incoming_todo
    return todos[random_id]


# @app.patch("/todos/{todo_id}")
# def update_todo(todo_id: str, todo: Todo):
#     stored_todo = todos[todo_id]
#     stored_todo_model = Todo(**stored_todo)
#     update_data = todo.model_dump(exclude_unset=True)
#     updated_todo = stored_todo_model.model_copy(update=update_data)
#     todos[todo_id] = jsonable_encoder(update_todo)
#     return updated_todo
