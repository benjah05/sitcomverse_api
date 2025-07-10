# run.py
from app import create_app, db
from app.models.user import User
from app.models.sitcom import Sitcom
from app.models.character import Character
from app.models.review import Review

# Create the Flask app instance
app = create_app()

# Ensure that database tables are created when the app starts
with app.app_context():
    # Connect to MySQL to create tables for the model
    db.create_all()


if __name__ == '__main__':
    # Run the Flask development server
    # Enable auto-reloading and a debugger with debug=True
    app.run(debug=True)