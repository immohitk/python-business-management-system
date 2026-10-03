def validate_tax_charge_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Tax or charge name cannot be empty.")


def validate_tax_charge_type(tax_charge_type: str) -> None:
    if tax_charge_type not in {"Tax", "Charge"}:
        raise ValueError("Tax or charge type must be Tax or Charge.")


def validate_tax_charge_calculation(calculation: str) -> None:
    if calculation not in {"Percentage", "Fixed Amount"}:
        raise ValueError(
            "Tax or charge calculation must be Percentage or Fixed Amount."
        )


def validate_tax_charge_value(value: float) -> None:
    if value < 0:
        raise ValueError("Tax or charge value cannot be negative.")


def validate_tax_charge_scope(
    scope: str,
    product_id: int | None,
) -> None:
    if scope not in {"Overall", "Product"}:
        raise ValueError("Tax or charge scope must be Overall or Product.")

    if scope == "Product" and product_id is None:
        raise ValueError("Product scope requires a product ID.")

    if scope == "Overall" and product_id is not None:
        raise ValueError("Overall scope cannot have a product ID.")


def validate_tax_charge_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Tax or charge creation timestamp cannot be empty.")