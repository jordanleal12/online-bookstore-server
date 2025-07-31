from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from psycopg2 import errorcodes, IntegrityError as PGIntegrityError
import sqlite3
from extensions import db
from schemas import customer_schema

customers = Blueprint("customers", __name__, url_prefix="/customers")


@customers.route("", methods=["POST"])
def create_customer():
    """Create a new customer from a POST request."""

    try:
        data = request.get_json()  # Allows custom arguments, request.json does not
        if not data:  # Validate that request contains data
            abort(
                400, description="No input data provided."
            )  # Abort invokes error handler whereas returning 400 with dict would not

        customer = customer_schema.load(
            data,
            session=db.session,  # Lets marshmallow validate relationships and foreign keys
        )
        db.session.add(customer)  # Adds customer instance to db session
        db.session.commit()  # Commits current session to the database
        return (
            jsonify(customer_schema.dump(customer)),
            201,
        )  # Returns the created customer as JSON with 201 status

    except ValidationError as e:  # Marshmallow validation of missing or invalid fields
        # when loading data with schema
        return {"error": "Invalid format", "messages": str(e.messages)}, 400

    except ValueError as e:  # Catch custom @validates errors defined in the model
        return {"error": "Invalid Content", "message": str(e)}, 400

    except IntegrityError as e:  # Database constraint errors like NOT NULL or UNIQUE
        db.session.rollback()  # Rollback required as IntegrityError occurs after adding to session

        if isinstance(e.orig, sqlite3.IntegrityError):  # Checks if sqlite db
            if "UNIQUE constraint failed" in str(e.orig):
                # Checks if db unique violation
                return {"error": "Email already exists", "message": str(e.orig)}, 409

        elif isinstance(e.orig, PGIntegrityError):  # Checks if PostgreSQL db
            if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {  # if NOT NULL violation
                    "error": "Required field missing",
                    "field": str(e.orig.diag.column_name),
                }, 400
            elif e.orig.pgcode == errorcodes.UNIQUE_VIOLATION:  # If UNIQUE violation
                return {"error": "Email already exists", "message": str(e.orig)}, 409
        return {  # Catch missed IntegrityError's
            "error": "Database Integrity Error",
            "message": str(e.orig),
        }, 400  # General error message for miscellaneous integrity issues
