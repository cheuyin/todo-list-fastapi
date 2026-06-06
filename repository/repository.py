from abc import ABC, abstractmethod


class Repository[T](ABC):
    @abstractmethod
    def get(self, item_id: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, item: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, item: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: str) -> T:
        raise NotImplementedError
