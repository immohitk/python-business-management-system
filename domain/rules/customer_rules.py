def validate_customer_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Customer name cannot be empty.")


def validate_customer_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Customer creation timestamp cannot be empty.")