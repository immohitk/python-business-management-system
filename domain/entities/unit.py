from dataclasses import dataclass

from domain.rules.unit_rules import validate_unit_code, validate_unit_name, validate_unit_factor


@dataclass
class Unit:
    code: str
    name: str
    dimension: str
    to_base_factor: float
    id: int | None = None

    def __post_init__(self) -> None:
        validate_unit_code(self.code)
        validate_unit_name(self.name)
        validate_unit_code(self.dimension)
        validate_unit_factor(self.to_base_factor)
