from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from psycopg2 import errorcodes
from extensions import db
from schemas import address_schema

addresses = Blueprint("addresses", __name__, url_prefix="/addresses")


@addresses.route("", methods=["POST"])
def create_address():
    """Create a new address from a POST request."""

    try:
        data = request.get_json()  # Allows custom arguments, request.json does not
        if not data:  # Validate that request contains data
            abort(
                400, description="No input data provided."
            )  # Abort invokes error handler whereas returning 400 with dict would not

        address = address_schema.load(
            data,
            session=db.session,  # Lets marshmallow validate relationships and foreign keys
        )
        db.session.add(address)  # Adds address instance to db session
        db.session.commit()  # Commits current session to the database
        return (
            jsonify(address_schema.dump(address)),
            201,
        )  # Returns the created address as JSON with 201 status

    except ValidationError as e:  # Marshmallow validation of missing or invalid fields
        # when loading data with schema
        return {"error": "Invalid format", "messages": str(e.messages)}, 400

    except ValueError as e:  # Catch custom @validates errors defined in the model
        return {"error": "Invalid Content", "message": str(e)}, 400

    except IntegrityError as e:  # Database constraint errors like NOT NULL or UNIQUE
        db.session.rollback()  # Rollback required as IntegrityError occurs after adding to session
        if (
            e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION
        ):  # Custom message for NOT NULL violations
            return {
                "error": "Required field missing",
                "field": str(e.orig.diag.column_name),
            }, 400
        return {
            "error": "Database Integrity Error",
            "message": str(e.orig),
        }, 400  # General error message for miscellaneous integrity issues
