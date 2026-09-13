from domain.entities.customer import Customer


def create_customer() -> Customer:
    return Customer(
        id=None,
        name="Rahul Sharma",
        phone="9876543210",
        email="rahul@example.com",
        address="Delhi",
        created_at="2026-09-13T10:00:00",
    )


def test_valid_customer_can_be_created():
    customer = create_customer()

    assert customer.name == "Rahul Sharma"
    assert customer.phone == "9876543210"
    assert customer.email == "rahul@example.com"
    assert customer.address == "Delhi"


def test_customer_name_cannot_be_empty():
    try:
        Customer(
            id=None,
            name="",
            phone=None,
            email=None,
            address=None,
            created_at="2026-09-13T10:00:00",
        )
    except ValueError as error:
        assert str(error) == "Customer name cannot be empty."
    else:
        raise AssertionError("Expected empty customer name to fail.")


def test_customer_name_cannot_be_whitespace():
    try:
        Customer(
            id=None,
            name="   ",
            phone=None,
            email=None,
            address=None,
            created_at="2026-09-13T10:00:00",
        )
    except ValueError as error:
        assert str(error) == "Customer name cannot be empty."
    else:
        raise AssertionError("Expected whitespace-only customer name to fail.")


def test_customer_created_at_cannot_be_empty():
    try:
        Customer(
            id=None,
            name="Rahul Sharma",
            phone=None,
            email=None,
            address=None,
            created_at="",
        )
    except ValueError as error:
        assert str(error) == "Customer creation timestamp cannot be empty."
    else:
        raise AssertionError("Expected empty creation timestamp to fail.")


def test_customer_created_at_cannot_be_whitespace():
    try:
        Customer(
            id=None,
            name="Rahul Sharma",
            phone=None,
            email=None,
            address=None,
            created_at="   ",
        )
    except ValueError as error:
        assert str(error) == "Customer creation timestamp cannot be empty."
    else:
        raise AssertionError(
            "Expected whitespace-only creation timestamp to fail."
        )


def test_customer_allows_optional_fields_to_be_none():
    customer = Customer(
        id=None,
        name="Rahul Sharma",
        phone=None,
        email=None,
        address=None,
        created_at="2026-09-13T10:00:00",
    )

    assert customer.phone is None
    assert customer.email is None
    assert customer.address is None


def test_customer_id_can_be_none_before_persistence():
    customer = create_customer()

    assert customer.id is None
