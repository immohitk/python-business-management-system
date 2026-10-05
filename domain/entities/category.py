from dataclasses import dataclass

from domain.rules.category_rules import validate_category_name


@dataclass
class Category:
    id: int | None
    name: str
    description: str | None = None

    def __post_init__(self) -> None:
        validate_category_name(self.name)
