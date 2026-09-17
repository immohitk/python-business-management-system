from pathlib import Path

from domain.entities.stock_movement import StockMovement, StockMovementType
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.stock_movement_repository import (
    StockMovementRepository,
)


def create_repository(tmp_path: Path) -> tuple[StockMovementRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    return StockMovementRepository(connection), connection


def create_product(connection) -> int:
    cursor = connection.execute(
        """
        INSERT INTO products (
            name,
            description,
            sku,
            price,
            quantity,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "Paint",
            "Interior wall paint",
            "PAINT-001",
            450.0,
            10,
            "2026-09-07T20:00:00",
        ),
    )
    connection.commit()

    return cursor.lastrowid


def create_movement(
    movement_type: StockMovementType = StockMovementType.ADD,
    quantity: int = 5,
    resulting_stock: int = 15,
    created_at: str = "2026-08-10T10:00:00",
) -> StockMovement:
    return StockMovement(
        movement_type=movement_type,
        quantity=quantity,
        resulting_stock=resulting_stock,
        created_at=created_at,
    )


def test_add_movement(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)
        movement = create_movement()

        repository.add_movement(product_id, movement)

        row = connection.execute(
            """
            SELECT
                product_id,
                movement_type,
                quantity,
                resulting_stock,
                created_at
            FROM stock_movements
            """
        ).fetchone()

        assert row == (
            product_id,
            "ADD",
            5,
            15,
            "2026-08-10T10:00:00",
        )
    finally:
        connection.close()


def test_get_movements(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)

        first_movement = create_movement(
            StockMovementType.ADD,
            5,
            15,
            "2026-08-10T10:00:00",
        )
        second_movement = create_movement(
            StockMovementType.DEDUCT,
            3,
            12,
            "2026-08-10T11:30:00",
        )

        repository.add_movement(product_id, first_movement)
        repository.add_movement(product_id, second_movement)

        result = repository.get_movements(product_id)

        assert result == [first_movement, second_movement]
    finally:
        connection.close()


def test_get_movements_returns_empty_list_for_product_without_movements(
    tmp_path,
):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)

        result = repository.get_movements(product_id)

        assert result == []
    finally:
        connection.close()


def test_get_by_id_returns_persisted_movement(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)
        movement = create_movement()

        repository.add_movement(product_id, movement)

        movement_id = connection.execute(
            "SELECT id FROM stock_movements"
        ).fetchone()[0]

        result = repository.get_by_id(movement_id)

        assert result == movement
    finally:
        connection.close()


def test_get_by_id_returns_none_for_missing_movement(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        result = repository.get_by_id(999)

        assert result is None
    finally:
        connection.close()


def test_get_all_returns_movements_in_id_order(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)

        first_movement = create_movement(
            StockMovementType.ADD,
            5,
            15,
        )
        second_movement = create_movement(
            StockMovementType.ADJUST,
            20,
            20,
        )

        repository.add_movement(product_id, first_movement)
        repository.add_movement(product_id, second_movement)

        result = repository.get_all()

        assert result == [first_movement, second_movement]
    finally:
        connection.close()


def test_delete_movement(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)
        movement = create_movement()

        repository.add_movement(product_id, movement)

        movement_id = connection.execute(
            "SELECT id FROM stock_movements"
        ).fetchone()[0]

        repository.delete(movement_id)

        assert repository.get_by_id(movement_id) is None
    finally:
        connection.close()


def test_add_movement_persists_created_at(tmp_path):
    repository, connection = create_repository(tmp_path)

    try:
        product_id = create_product(connection)
        movement = create_movement(
            created_at="2026-08-10T15:30:00",
        )

        repository.add_movement(product_id, movement)

        persisted_movements = repository.get_movements(product_id)

        assert len(persisted_movements) == 1
        assert persisted_movements[0].created_at == "2026-08-10T15:30:00"
    finally:
        connection.close()
