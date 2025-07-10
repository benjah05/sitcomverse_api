# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config # Import Config class


# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """
    Factory function to create and configure the Flask application.
    This function initializes the Flask app and its extensions.
    """
    app = Flask(__name__)

    # Load configurations from the Config class
    app.config.from_object(Config)

    # Initialize extensions with the app instance
    db.init_app(app)
    jwt.init_app(app)

    # Import the auth blueprint
    from app.routes.auth_routes import auth_bp
    # Register the blueprint with a URL prefix (/api/auth)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Import the sitcom blueprint
    from app.routes.sitcom_routes import sitcom_bp
    app.register_blueprint(sitcom_bp, url_prefix='/api')

    # Import the Character blueprint
    from app.routes.character_routes import character_bp
    app.register_blueprint(character_bp, url_prefix='/api')

    # Import the Review blueprint
    from app.routes.review_routes import review_bp
    app.register_blueprint(review_bp, url_prefix='/api')

    # Home route
    @app.route('/')
    def hello_sitcomverse():
        return "Hello, Sitcomverse API is running!"

    return app

