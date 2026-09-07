from abc import ABC, abstractmethod
from typing import Generic, TypeVar


EntityType = TypeVar("EntityType")


class Repository(ABC, Generic[EntityType]):
    """Base contract for repository implementations."""

    @abstractmethod
    def add(self, entity: EntityType) -> None:
        """Persist an entity."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: int) -> EntityType | None:
        """Return an entity by ID, or None if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[EntityType]:
        """Return all persisted entities."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Delete an entity by ID."""
        raise NotImplementedError