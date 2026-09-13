from domain.entities.supplier import Supplier


def create_supplier() -> Supplier:
    return Supplier(
        id=None,
        name="ABC Paint Suppliers",
        phone="9876501234",
        email="abc@example.com",
        address="Delhi",
        created_at="2026-09-13T10:00:00",
    )


def test_valid_supplier_can_be_created():
    supplier = create_supplier()

    assert supplier.name == "ABC Paint Suppliers"
    assert supplier.phone == "9876501234"
    assert supplier.email == "abc@example.com"
    assert supplier.address == "Delhi"


def test_supplier_name_cannot_be_empty():
    try:
        Supplier(
            id=None,
            name="",
            phone=None,
            email=None,
            address=None,
            created_at="2026-09-13T10:00:00",
        )
    except ValueError as error:
        assert str(error) == "Supplier name cannot be empty."
    else:
        raise AssertionError("Expected empty supplier name to fail.")


def test_supplier_name_cannot_be_whitespace():
    try:
        Supplier(
            id=None,
            name="   ",
            phone=None,
            email=None,
            address=None,
            created_at="2026-09-13T10:00:00",
        )
    except ValueError as error:
        assert str(error) == "Supplier name cannot be empty."
    else:
        raise AssertionError("Expected whitespace-only supplier name to fail.")


def test_supplier_created_at_cannot_be_empty():
    try:
        Supplier(
            id=None,
            name="ABC Paint Suppliers",
            phone=None,
            email=None,
            address=None,
            created_at="",
        )
    except ValueError as error:
        assert str(error) == "Supplier creation timestamp cannot be empty."
    else:
        raise AssertionError("Expected empty creation timestamp to fail.")


def test_supplier_created_at_cannot_be_whitespace():
    try:
        Supplier(
            id=None,
            name="ABC Paint Suppliers",
            phone=None,
            email=None,
            address=None,
            created_at="   ",
        )
    except ValueError as error:
        assert str(error) == "Supplier creation timestamp cannot be empty."
    else:
        raise AssertionError(
            "Expected whitespace-only creation timestamp to fail."
        )


def test_supplier_allows_optional_fields_to_be_none():
    supplier = Supplier(
        id=None,
        name="ABC Paint Suppliers",
        phone=None,
        email=None,
        address=None,
        created_at="2026-09-13T10:00:00",
    )

    assert supplier.phone is None
    assert supplier.email is None
    assert supplier.address is None


def test_supplier_id_can_be_none_before_persistence():
    supplier = create_supplier()

    assert supplier.id is None
