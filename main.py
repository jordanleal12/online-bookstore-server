"""Main application file for creating and configuring Flask app."""

from flask import Flask
from extensions import db


def create_app(config_class="config.DevConfig"):
    """Create and configure Flask application instance using DevConfig configuration"""

    app = Flask(__name__)  # Create Flask app instance
    app.config.from_object(config_class)  # Loads the DevConfig from config.py
    # after being passed as a string as an argument in create_app()
    db.init_app(app)  # Initialize database using app instance
    return app  # Return the configured app instance
