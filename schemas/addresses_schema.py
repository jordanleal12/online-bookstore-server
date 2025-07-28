"""Schema for Address using Marshmallow"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Address
from extensions import db


class AddressSchema(SQLAlchemyAutoSchema):
    """Schema for Address model using Auto Schema"""

    class Meta:
        """Sets metadata and controls behavior of the schema"""

        model = Address
        load_instance = True  # Automatically converts json data to python object
        # Links SQLAlchemy session to the schema, allowing it to validate and load objects
        # from foreign key/relationships when converting json to python objects (deserialization)
        sqla_session = db.session
        # Relationships to be defined later when Customer model is created


address_schema = (
    AddressSchema()
)  # Instance of schema for use in routes on single address
addresses_schema = AddressSchema(
    many=True
)  # Instance of schema for use in routes on multiple addresses
