def validate_product_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Product name cannot be empty.")


def validate_product_sku(sku: str) -> None:
    if not sku.strip():
        raise ValueError("Product SKU cannot be empty.")


def validate_product_price(price: float) -> None:
    if price < 0:
        raise ValueError("Product price cannot be negative.")


def validate_product_quantity(quantity: int) -> None:
    if quantity < 0:
        raise ValueError("Product quantity cannot be negative.")


def validate_product_created_at(created_at: str) -> None:
    if not created_at.strip():
        raise ValueError("Product creation timestamp cannot be empty.")


def validate_product_unit(unit: str, field_name: str) -> None:
    if not unit.strip():
        raise ValueError(f"Product {field_name} unit cannot be empty.")


def validate_conversion_factor(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"Product {field_name} conversion must be greater than zero.")


def validate_margin(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"Product {field_name} margin cannot be negative.")


def validate_margin_range(default: float, minimum: float, maximum: float) -> None:
    if minimum > maximum:
        raise ValueError("Product minimum margin cannot exceed maximum margin.")
    if not minimum <= default <= maximum:
        raise ValueError("Product default margin must be between minimum and maximum margin.")


def validate_mrp(mrp_applicable: bool, default_mrp: float | None) -> None:
    if default_mrp is not None and default_mrp < 0:
        raise ValueError("Product default MRP cannot be negative.")
    if mrp_applicable and (default_mrp is None or default_mrp <= 0):
        raise ValueError("Default MRP is required and must be greater than zero when MRP is applicable.")


def validate_default_tax_id(default_tax_id: int | None) -> None:
    if default_tax_id is not None and default_tax_id <= 0:
        raise ValueError("Product default tax ID must be greater than zero.")
