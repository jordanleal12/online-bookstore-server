"""Test cases for Customer model, schema, and CRUD operations.
Using TDD, we will implement the tests first and then the corresponding code."""

import pytest
from sqlalchemy.exc import IntegrityError
from models import Customer  # This will be created after failing the test


def test_customer_creation(db_session):
    """Test the model by creating a new customer instance."""

    # Create customer instance using Customer model
    customer = Customer(
        f_name="John",
        l_name="Smith",
        email="johnsmith@email.com",
        phone="+61412345678",
        address_id=1,
    )

    db_session.add(customer)  # Adds customer to db fixture session from conftest.py
    db_session.commit()

    assert (
        customer.id is not None
    )  # Test customer instance has been created in database
    assert (
        Customer.query.first().email == "johnsmith@email.com"
    )  # Check values saved correctly


# @parametrize decorator runs the test for each set of parameters provided as a list of tuples
# Validation check in model gives value error for missing or invalid field formatting
@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        ("f_name", None, ValueError),  # Model level validation for missing values
        ("email", None, ValueError),
        ("email", "invalid-email", ValueError),  # Invalid email format
        ("phone", "0476301981", ValueError),  # Check invalid E.164 format
        ("phone", "+611111111", ValueError),  # Check valid format but number not in use
        ("address_id", None, IntegrityError),  # DB level validation for missing FK
    ],
)
def test_required_fields(db_session, field, value, expected_error):
    """Test that required fields are enforced in the Customer model."""

    # Create customer data with all required fields
    customer_data = {
        "f_name": "John",
        "l_name": "Smith",
        "email": "johnsmith@email.com",
        "phone": "0412345678",
        "address_id": 1,
    }

    customer_data[field] = value  # Replaces each field with None as the test iterates

    # Checks that an error is raised when a required field is None
    with pytest.raises(expected_error):
        # Uses kwargs to turn customer_data dict into Customer model fields
        # and replace each field with None one by one as the test iterates
        customer = Customer(**customer_data)
        db_session.add(customer)
        db_session.commit()


def test_unique_email(db_session):
    """Test that email field is unique in Customer Model."""

    customer1 = Customer(
        f_name="John",
        l_name="Smith",
        email="johnsmith@email.com",
        phone="0412345678",
        address_id=1,
    )  # Create and add customer to test database
    db_session.add(customer1)
    db_session.commit()

    with pytest.raises(IntegrityError):  # Catch Integrity error
        customer2 = Customer(  # Create 2nd customer with duplicate email
            f_name="Mary",
            l_name="Jane",
            email="johnsmith@email.com",
            phone="0498765432",
            address_id=2,
        )
        db_session.add(customer2)
        db_session.commit()
        db_session.rollback()


def test_create_customer(client):
    """Test customer_schema by creating a new customer from
    a fake json POST request using the test client."""

    response = client.post(  # Retrieve fake json data from Flask test client
        "/customers",
        json={
            "f_name": "John",
            "l_name": "Smith",
            "email": "johnsmith@email.com",
            "phone": "0412345678",
            "address_id": 1,
        },
    )
    assert response.status_code == 201  # Response for successful creation
    assert response.json["email"] == "johnsmith@email.com"  # Check values returned


def test_duplicate_email_post(client):
    """Test that email uniqueness is enforced with POST requests."""
    # Create customer from post request
    client.post(
        "/customers",
        json={
            "f_name": "John",
            "email": "johnsmith@email.com",
            "address_id": 1,
        },
    )
    # Attempt creation with duplicate email
    response = client.post(
        "/customers",
        json={
            "f_name": "Mary",
            "email": "johnsmith@email.com",
            "address_id": 2,
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json["error"]


def test_customer_order_relationship(db_session):
    """Test that Customer is correctly linked to Order model,
    and that order data can be linked through the relationship."""
    from models import Order  # This will be created after failing the test

    # This will fail until Customer & Order models are created, and relationship is established
    customer = Customer(
        f_name="John",
        l_name="Smith",
        email="johnsmith@email.com",
        phone="0423456789",
        address_id=1,
    )
    db_session.add(customer)
    db_session.commit()  # Commit to db so customer can be accessed through order

    order = Order(customer_id=customer.id, order_date="2025-07-28 06:45:49")
    db_session.add(Order)
    db_session.commit()

    # Check that customer can be accessed through order
    assert order.customer.email == "johnsmith@email.com"
    # Check that order can be accessed through customer
    assert customer.orders[0].order_id == 1
