"""Model for creating Customer instances."""

from sqlalchemy.orm import validates
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
    phone = db.Column(db.String(20))  # 15 is max length of E.164, + formatting chars
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
