# app/model/user.py
from app import db # Import the SQLAlchemy db instance
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Represents a user in the Sitcomverse API
    This model defines the 'users' table in the database
    """

    # Explicitly set the name of the table to 'users'
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))

    # Relationships
    # sitcoms = db.relationship('Sitcom', backref='creator', lazy=True)
    # votes = db.relationship('Vote', backref='voter', lazy=True)

    def __repr__(self):
        """
        String representation of the User object
        """
        return f'<User {self.username}>'
    

    def set_password(self, password):
        """
        Hashes the given plain-text password and stores it
        """
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        """
        Checks if the provided plain-text password matched the stored hash
        """
        return check_password_hash(self.password_hash, password)
    

    def to_dict(self):
        """
        Converts the User object to a dictionary, excluding sensitive information
        Returns user data useful in API responses
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }    