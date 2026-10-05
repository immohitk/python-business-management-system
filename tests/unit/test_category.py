import pytest

from domain.entities.category import Category


def test_valid_category_can_be_created():
    category = Category(id=None, name="Groceries", description="Food items")
    assert category.name == "Groceries"


def test_category_name_cannot_be_empty():
    with pytest.raises(ValueError, match="Category name cannot be empty"):
        Category(id=None, name="   ")
