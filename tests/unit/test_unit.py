import pytest

from domain.entities.unit import Unit


def test_unit_validates_and_normalizes_repository_values():
    unit = Unit("kg", "Kilogram", "mass", 1000.0)
    assert unit.code == "kg"
    assert unit.dimension == "mass"


def test_unit_rejects_non_positive_factor():
    with pytest.raises(ValueError, match="Unit conversion factor"):
        Unit("KG", "Kilogram", "MASS", 0)
