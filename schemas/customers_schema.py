"""Schema for Customer using Marshmallow"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Customer
from extensions import db


class CustomerSchema(SQLAlchemyAutoSchema):
    """Schema for Customer model using Auto Schema"""

    class Meta:
        """Sets metadata and controls behavior of the schema"""

        model = Customer
        load_instance = True  # Automatically converts json data to python object
        sqla_session = db.session  # Links SQLAlchemy session to schema to validate
        include_fk = True
        # and load objects from foreign key/relationships when converting json to python objects

        # Relationships to be defined later when Order model is created


customer_schema = (
    CustomerSchema()
)  # Instance of schema for use in routes on single customer
customers_schema = CustomerSchema(
    many=True
)  # Instance of schema for use in routes on multiple customers
