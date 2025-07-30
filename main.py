"""Main application file for creating and configuring Flask app."""

from sqlite3 import Connection as SQLiteConnection
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from extensions import db


def create_app(config_class="config.DevConfig"):
    """Create and configure Flask application instance using DevConfig configuration"""

    app = Flask(__name__)  # Create Flask app instance
    app.config.from_object(config_class)  # Loads the relevant config from config.py
    # after being passed as a string as an argument in create_app()
    db.init_app(app)  # Initialize database using app instance

    @event.listens_for(Engine, "connect")  # Listens for database engine connection
    def set_sqlite_pragma(
        dbapi_connection,  # Represents the database connection object
        connection_record,  # Connection_record required as listener function expects it
    ):
        """Allows SQLite to use FK relationships by executing PRAGMA statement each time
        db connection is made (such as query or transaction) and db instance is SQLite.
        """
        # Executes if db connection object is an sqlite connection object
        if isinstance(dbapi_connection, SQLiteConnection):
            cursor = dbapi_connection.cursor()  # Create cursor object for SQL commands
            cursor.execute("PRAGMA foreign_keys=ON")  # Executes command per connection
            cursor.close()  # Close cursor to free resources

    from controllers import controller_blueprints  # Import all controllers as a list

    for controller in controller_blueprints:  # Register each controller blueprint
        app.register_blueprint(controller)

    return app  # Return the configured app instance
