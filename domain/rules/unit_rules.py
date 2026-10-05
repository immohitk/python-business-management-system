def validate_unit_code(code: str) -> None:
    if not code.strip():
        raise ValueError("Unit code cannot be empty.")


def validate_unit_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Unit name cannot be empty.")


def validate_unit_factor(factor: float) -> None:
    if factor <= 0:
        raise ValueError("Unit conversion factor must be greater than zero.")
