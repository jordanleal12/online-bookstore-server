"""Test cases for Address model, schema, and CRUD operations.
Using TDD, we will implement the tests first and then the corresponding code."""

import pytest
from sqlalchemy.exc import IntegrityError, ValueError
from main import db
from models import Address, Customer  # This will be created after failing the test


def test_address_creation(db_session):
    """Test the model by creating a new address instance."""

    # This will fail until Address model is created
    address = Address(
        country_code="US",
        state_code="CA",
        city="San Francisco",
        street="123 Test St",
        postcode="12345",
    )

    db_session.add(address)  # Adds address to db fixture session from conftest.py
    db_session.commit()

    assert address.id is not None  # Test address instance has been created in database
    assert Address.query.first().street == "123 Test St"  # Check values saved correctly


def test_required_fields(db_session):
    """Test that required fields are enforced in the Address model."""

    # This will fail until Address model is created
    with pytest.raises(IntegrityError):
        address = Address(
            country_code=None,  # Missing required field
            state_code="CA",
            city="San Francisco",
            street="123 Test St",
            postcode="12345",
        )
        db.session.add(address)
        db.session.commit()


def test_country_code_length(db_session):
    """Test that country_code string length is enforced."""

    # This will fail until Address model is created
    with pytest.raises(ValueError):
        address = Address(
            country_code="USA",  # Schema should enforce max length of 2
            state_code="CA",
            city="San Francisco",
            street="123 Test St",
            postcode="12345",
        )
        db.session.add(address)
        db.session.commit()


def test_create_address(client):
    """Test address_schema by creating a new address from
    a fake json POST request using the test client."""

    # This will fail until address schema, model and routes are created
    response = client.post(
        "/addresses",
        json={
            "country_code": "US",
            "state_code": "CA",
            "city": "San Francisco",
            "street": "123 Test St",
            "postcode": "12345",
        },
    )
    assert response.status_code == 201  # Response for successful creation
    assert b"123 Test St" in response.data


def test_customer_address_relationship(db_session):
    """Test that Address is correctly linked to Customer model,
    and that address data can be linked through the relationship."""

    # This will fail until Customer & Address models are created, and relationship is established
    address = Address(
        country_code="US",
        state_code="CA",
        city="San Francisco",
        street="123 Test St",
        postcode="12345",
    )
    customer = Customer(
        f_name="John",
        l_name="Smith",
        email="johnsmith@email.com",
        phone="0423456789",
        address_id=address.id,
    )

    # Check that address can be accessed through customer
    assert customer.address.street == "123 Test St"
    # Check that customer can be accessed through address
    assert address.customers[0].email == "johnsmith@email.com"
