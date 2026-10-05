from domain.entities.category import Category
from infrastructure.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def add_category(self, category: Category) -> None:
        self.repository.add(category)

    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)

    def get_categories(self):
        return self.repository.get_all()

    def update_category(self, category: Category) -> None:
        self.repository.update(category)

    def delete_category(self, category_id: int) -> None:
        self.repository.delete(category_id)
