def validate_supplier_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Supplier name cannot be empty.")


def validate_supplier_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Supplier creation timestamp cannot be empty.")
