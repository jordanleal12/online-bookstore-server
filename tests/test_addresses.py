"""Test cases for Address model, schema, and CRUD operations.
Using TDD, we will implement the tests first and then the corresponding code."""

import pytest
from sqlalchemy.exc import IntegrityError
from main import db
from models import Address


def test_address_creation(db_session):
    """Test the model by creating a new address instance."""

    # Create address instance using Address model
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


# @parametrize decorator runs the test for each set of parameters provided as a list of tuples
# Validation check in model gives value error for ISO codes instead, so we define expected errors
@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        ("country_code", None, ValueError),
        ("state_code", None, ValueError),
        ("street", None, IntegrityError),
        ("postcode", None, IntegrityError),
    ],
)
def test_required_fields(db_session, field, value, expected_error):
    """Test that required fields are enforced in the Address model."""

    # Create address data with all required fields
    address_data = {
        "country_code": "US",
        "state_code": "CA",
        "city": "San Francisco",
        "street": "123 Test",
        "postcode": "12345",
    }

    address_data[field] = value  # Replaces each field with None as the test iterates

    # Checks that an error is raised when a required field is None
    with pytest.raises(expected_error):
        # Uses kwargs to turn address_data dict into Address model fields
        # and replace each field with None one by one as the test iterates
        address = Address(**address_data)
        db_session.add(address)
        db_session.commit()


# Create parametrize decorated function to allow iteration of test cases
@pytest.mark.parametrize(
    "field, value",
    [
        ("country_code", "USA"),
        ("country_code", "U"),
        ("state_code", "Perth"),
        ("state_code", "p"),
    ],
)
def test_iso_code_length(db_session, field, value):
    """Test that country_code string length is enforced."""

    # Create valid address data
    address_data = {
        "country_code": "US",
        "state_code": "CA",
        "city": "San Francisco",
        "street": "123 Test",
        "postcode": "12345",
    }

    # Replace each field with each tuple value per iteration
    address_data[field] = value
    # Check that the expected error defined in parametrize is raised
    with pytest.raises(ValueError):
        address = Address(
            **address_data
        )  # Uses kwargs to turn address_data into Address instance per iteration
        db_session.add(address)


def test_create_address(client):
    """Test address_schema by creating a new address from
    a fake json POST request using the test client."""

    response = client.post(  # Retrieve fake json data from Flask test client
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
    assert (
        response.json["street"] == "123 Test St"
    )  # Check that values are returned in response


def test_customer_address_relationship(db_session):
    """Test that Address is correctly linked to Customer model,
    and that address data can be linked through the relationship."""
    from models import Customer  # This will be created after failing the test

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
