from infrastructure.repositories.unit_repository import UnitRepository


class UnitConversionService:
    """Convert quantities only between units belonging to the same dimension."""

    def __init__(self, repository: UnitRepository):
        self.repository = repository

    def convert(self, quantity: float, from_unit: str, to_unit: str) -> float:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        source = self.repository.get_by_code(from_unit)
        target = self.repository.get_by_code(to_unit)

        if source is None:
            raise ValueError(f"Unknown unit: {from_unit}")
        if target is None:
            raise ValueError(f"Unknown unit: {to_unit}")
        if source.dimension != target.dimension:
            raise ValueError(
                f"Cannot convert {source.code} to {target.code}: units have different dimensions."
            )

        return quantity * source.to_base_factor / target.to_base_factor
