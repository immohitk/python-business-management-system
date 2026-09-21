from pathlib import Path

from application.services.sale_service import SaleService
from domain.entities.sale import Sale
from domain.entities.sale_line import SaleLine
from infrastructure.database.connection import get_connection
from infrastructure.database.initialization import initialize_database
from infrastructure.repositories.sale_repository import SaleRepository


def create_service(
    tmp_path: Path,
) -> tuple[SaleService, SaleRepository, object]:
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    connection = get_connection(database_path)

    sale_repository = SaleRepository(connection)
    service = SaleService(sale_repository)

    return service, sale_repository, connection


def create_sale() -> Sale:
    return Sale(
        id=None,
        customer_id=1,
        sale_date="2026-09-21",
        total_amount=0.0,
        created_at="2026-09-21T20:00:00",
        lines=[
            SaleLine(
                product_id=1,
                quantity=2,
                unit_price=100.0,
            ),
            SaleLine(
                product_id=2,
                quantity=3,
                unit_price=50.0,
            ),
        ],
    )


def test_create_sale_persists_sale(tmp_path):
    service, sale_repository, connection = create_service(tmp_path)

    try:
        sale = create_sale()

        result = service.create_sale(sale)

        assert result.id is not None

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert stored_sale.customer_id == 1
        assert stored_sale.total_amount == 350.0
    finally:
        connection.close()


def test_create_sale_persists_sale_items(tmp_path):
    service, sale_repository, connection = create_service(tmp_path)

    try:
        sale = create_sale()

        result = service.create_sale(sale)

        assert result.id is not None

        items = sale_repository.get_items(result.id)

        assert len(items) == 2

        assert items[0].product_id == 1
        assert items[0].quantity == 2
        assert items[0].unit_price == 100.0

        assert items[1].product_id == 2
        assert items[1].quantity == 3
        assert items[1].unit_price == 50.0
    finally:
        connection.close()


def test_create_sale_applies_calculated_total(tmp_path):
    service, _, connection = create_service(tmp_path)

    try:
        sale = create_sale()

        assert sale.total_amount == 0.0

        result = service.create_sale(sale)

        assert result.total_amount == 350.0
    finally:
        connection.close()


def test_create_sale_reconstructs_sale_lines(tmp_path):
    service, sale_repository, connection = create_service(tmp_path)

    try:
        sale = create_sale()

        result = service.create_sale(sale)

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert len(stored_sale.lines) == 2

        assert stored_sale.lines[0].product_id == 1
        assert stored_sale.lines[0].quantity == 2
        assert stored_sale.lines[0].unit_price == 100.0

        assert stored_sale.lines[1].product_id == 2
        assert stored_sale.lines[1].quantity == 3
        assert stored_sale.lines[1].unit_price == 50.0
    finally:
        connection.close()


def test_create_sale_without_lines_persists_zero_total(tmp_path):
    service, sale_repository, connection = create_service(tmp_path)

    try:
        sale = Sale(
            id=None,
            customer_id=1,
            sale_date="2026-09-21",
            total_amount=0.0,
            created_at="2026-09-21T20:00:00",
            lines=[],
        )

        result = service.create_sale(sale)

        assert result.id is not None
        assert result.total_amount == 0.0

        stored_sale = sale_repository.get_by_id(result.id)

        assert stored_sale is not None
        assert stored_sale.lines == []
    finally:
        connection.close()
