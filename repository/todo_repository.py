import json
from main import Todo
from repository.repository import Repository
from pathlib import Path


class TodoRepository(Repository[Todo]):
    def __init__(self, store_path):
        self.store_path = store_path
        store_file = Path(store_path)
        if not store_file.is_file():
            store_file.parent.mkdir(parents=True, exist_ok=True)
            store_file.write_text("{}", encoding='utf-8')

    def get(self, item_id: str) -> Todo:
        data = json.loads(Path(self.store_path).read_text(encoding="utf-8"))
        return Todo(**data[item_id])

    def get_all(self) -> list[Todo]:
        data = json.loads(Path(self.store_path).read_text(encoding="utf-8"))
        res = []
        for todo_dict in list(data.values()):
            res.append(Todo(**todo_dict))
        return res

    def add(self, item: Todo) -> Todo:
        data = json.loads(Path(self.store_path).read_text(encoding="utf-8"))
        data[item.id] = item.model_dump()
        Path(self.store_path).write_text(json.dumps(data, indent=4))
        return Todo(**data[item.id])

    def update(self, item: Todo) -> Todo:
        data = json.loads(Path(self.store_path).read_text(encoding="utf-8"))

        if item.id not in data:
            raise KeyError(f"Object with id ${item.id} not found")

        data[item.id] = item.model_dump()

        Path(self.store_path).write_text(json.dumps(data, indent=4))

        return Todo(**data[item.id])

    def delete(self, item_id: str) -> Todo:
        data = json.loads(Path(self.store_path).read_text(encoding="utf-8"))
        if item_id not in data:
            raise KeyError(f"Object with id ${item_id} not found")
        todo = data[item_id]
        del data[item_id]
        Path(self.store_path).write_text(json.dumps(data, indent=4))
        return Todo(**todo)
