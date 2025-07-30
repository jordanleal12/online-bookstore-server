"""Model for creating Customer instances."""

from sqlalchemy.orm import validates
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from extensions import db


class Customer(db.Model):
    """Model for storing customer information."""

    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50))  # Nullable as some names are one name only
    email = db.Column(
        db.String(254),  # Max email length per RFC 5321
        unique=True,  # Must be unique as order information is sent to email
        nullable=False,  # Required for customer invoicing etc.
    )
    phone = db.Column(db.String(20))  # 15 is max length of E.164, + whitespace
    address_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "addresses.id", ondelete="SET NULL"
        ),  # 'ondelete' tells database to set null on parent (address) deletion
        nullable=True,  # address_id needs to allow nullable for address deletion/change
    )

    address = db.relationship("Address", back_populates="customers")

    @validates("email")
    def validate_email(self, key, email):
        """Validates email has correct formatting and returns normalized version."""

        if not email:
            raise ValueError("No email provided")
        try:
            # test_environment becomes check_deliverability=True on deployment to check valid domain
            email_info = validate_email(email, test_environment=True)
            return email_info.normalized  # Returns normalized version of address
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}") from e

    @validates("phone")
    def validate_phone(self, key, phone):
        """Validates phone has correct formatting, expecting E.164 formatted number"""

        if phone:
            try:
                number = phonenumbers.parse(
                    phone, None  # None as E.164 doesn't require region
                )
            except phonenumbers.NumberParseException as e:  # Error if can't be parsed
                raise ValueError(f"Invalid phone number: {e}") from e

            if not phonenumbers.is_possible_number(number):  # Checks correct format
                raise ValueError("Invalid number format, ensure E.164 formatting")

            if not phonenumbers.is_valid_number(number):  # Checks number in use
                raise ValueError("Number is correct format but not in use")

            return phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164,  # Ensures number is saved to database as E.164
            )
        return None
