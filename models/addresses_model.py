"""Model for creating Address instances"""

from sqlalchemy.orm import validates
from extensions import db


class Address(db.Model):
    """Model for storing addresses of customers."""

    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2), nullable=False)  # Enforces max length of 2
    state_code = db.Column(db.String(3), nullable=False)  # Enforces max length of 3
    city = db.Column(db.String(50))  # Optional as not all addresses have city
    street = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)  # Max length of postcodes is 10
    # Relationship to Customer model to be added after creating Customer model

    @validates("country_code")
    def validate_country_code(self, key, value):
        """Validates country_code is 2 alphabetical characters long for IS0 3166 country codes."""

        if not isinstance(value, str) or len(value) != 2:
            raise ValueError("ISO 3166 country code must be 2 alphabetical characters")
        return value.upper()  # Convert to uppercase for consistency

    @validates("state_code")
    def validate_state_code(self, key, value):
        """Validates state_code is 2-3 alphabetical characters long for ISO 3166-2 state codes."""

        if not isinstance(value, str) or len(value) not in (2, 3):
            raise ValueError(
                "ISO 3166-2 subdivision code must be 2 or 3 alphabetical characters"
            )
        return value.upper()  # Convert to uppercase for consistency

    def __repr__(self):
        """String representation of Address instances useful for debugging."""

        # Shorten street output if too long
        shortened_street = (
            self.street[:25] + "..." if len(self.street) > 25 else self.street
        )
        return f"<Address {shortened_street}, {self.city}, {self.country_code}>"
