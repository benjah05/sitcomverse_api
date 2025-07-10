# app/__init__.py
from flask import Flask, jsonify
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

    # Import the auth, sitcom, character, and review blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.sitcom_routes import sitcom_bp
    from app.routes.character_routes import character_bp
    from app.routes.review_routes import review_bp


    # Register the blueprints with a URL prefix
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sitcom_bp, url_prefix='/api')
    app.register_blueprint(character_bp, url_prefix='/api')
    app.register_blueprint(review_bp, url_prefix='/api')

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad Request: The server cannot process the request due to a client error.", "error": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"message": "Unauthorized: Authentication required or invalid credentials.", "error": str(error)}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"message": "Forbidden: You do not have permission to access the requested resource.", "error": str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Not Found: The requested URL was not found on the server.", "error": str(error)}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"message": "Method Not Allowed: The method is not allowed for the requested URL.", "error": str(error)}), 405

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({"message": "Conflict: The request could not be completed due to a conflict with the current state of the resource (e.g., duplicate entry).", "error": str(error)}), 409

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"message": "Internal Server Error: Something went wrong on the server.", "error": str(error)}), 500

    # Home route
    @app.route('/')
    def hello_sitcomverse():
        message = """
        <h1>Welcome to the Sitcomverse API!</h1>
        <p>This project holds a special place for me. As a Computer Science and ALX student, I've faced moments of burnout, losing sight of the passion that first drew me to programming. During those times, sitcoms have always been my go-to comfort, a source of joy and escape.</p>
        <p>Building this Sitcomverse API has been more than just an assignment; it's been a journey of rediscovery. It brought back that feeling of genuine excitement for programming, reminding me why I love to build and learn. It rekindled my desire to continue this path and create more.</p>
        <p>I hope you enjoy exploring the API as much as I enjoyed building it!</p>
        <p>The API is running and ready for interaction at this base URL. Please refer to the README for endpoint details.</p>
        """
        return message, 200

    return app

