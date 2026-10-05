def validate_category_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Category name cannot be empty.")
