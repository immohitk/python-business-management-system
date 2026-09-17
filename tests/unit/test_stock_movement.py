import pytest

from domain.entities.stock_movement import (
    StockMovement,
    StockMovementType,
)


def test_stock_movement_add():
    movement = StockMovement(
        movement_type=StockMovementType.ADD,
        quantity=5,
        resulting_stock=15,
        created_at="2026-08-10T10:30:00",
    )

    assert movement.movement_type == StockMovementType.ADD
    assert movement.quantity == 5
    assert movement.resulting_stock == 15
    assert movement.created_at == "2026-08-10T10:30:00"


def test_stock_movement_adjust():
    movement = StockMovement(
        movement_type=StockMovementType.ADJUST,
        quantity=8,
        resulting_stock=8,
        created_at="2026-08-10T10:30:00",
    )

    assert movement.movement_type == StockMovementType.ADJUST
    assert movement.quantity == 8
    assert movement.resulting_stock == 8
    assert movement.created_at == "2026-08-10T10:30:00"


def test_stock_movement_deduct():
    movement = StockMovement(
        movement_type=StockMovementType.DEDUCT,
        quantity=3,
        resulting_stock=12,
        created_at="2026-08-10T10:30:00",
    )

    assert movement.movement_type == StockMovementType.DEDUCT
    assert movement.quantity == 3
    assert movement.resulting_stock == 12
    assert movement.created_at == "2026-08-10T10:30:00"


def test_stock_movement_rejects_negative_quantity():
    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        StockMovement(
            movement_type=StockMovementType.ADD,
            quantity=-1,
            resulting_stock=10,
            created_at="2026-08-10T10:30:00",
        )


def test_stock_movement_rejects_negative_resulting_stock():
    with pytest.raises(
        ValueError,
        match="Stock quantity cannot be negative",
    ):
        StockMovement(
            movement_type=StockMovementType.DEDUCT,
            quantity=5,
            resulting_stock=-1,
            created_at="2026-08-10T10:30:00",
        )


def test_stock_movement_rejects_empty_created_at():
    with pytest.raises(
        ValueError,
        match="Product creation timestamp cannot be empty",
    ):
        StockMovement(
            movement_type=StockMovementType.ADD,
            quantity=5,
            resulting_stock=15,
            created_at="",
        )
