import pytest

from infrastructure.repositories.base import Repository


class SampleRepository(Repository[str]):
    def add(self, entity: str) -> None:
        pass

    def get_by_id(self, entity_id: int) -> str | None:
        return None

    def get_all(self) -> list[str]:
        return []

    def delete(self, entity_id: int) -> None:
        pass


def test_repository_can_be_implemented():
    repository = SampleRepository()

    assert repository.get_by_id(1) is None
    assert repository.get_all() == []


def test_repository_base_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Repository()