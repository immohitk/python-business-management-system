VALID_CUSTOMER_STATUSES = {"ACTIVE", "INACTIVE"}


def validate_customer_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Customer name cannot be empty.")


def validate_customer_status(status: str) -> None:
    if status not in VALID_CUSTOMER_STATUSES:
        raise ValueError("Customer status must be ACTIVE or INACTIVE.")


def validate_customer_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Customer creation timestamp cannot be empty.")
