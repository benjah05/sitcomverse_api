# app/models/character.py
from app import db
from datetime import datetime, timezone


class Character(db.Model):
    """
    Represents a character in the Sitcomverse API
    This model defines the 'characters' table in the database
    """

    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    actor = db.Column(db.String(255))
    role = db.Column(db.String(100)) # e.g, "Lead", "Supporting", "Recurring", "Character", "Background", "Cameo"
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    # Foreign key to link to the Sitcom this character belongs to
    sitcom_id = db.Column(db.Integer, db.ForeignKey('sitcoms.id'), nullable=False)
    # Define the relationship to the Sitcom model
    sitcom = db.Relationship('Sitcom', backref=db.backref('characters', lazy=True))

    def __repr__(self):
        """
        String representation of the Character object
        """
        return f'<Character {self.name} from Sitcom ID {self.sitcom_id}>'
    

    def to_dict(self):
        """
        Converts the Character object to a dictionary, excluding sensitive information
        Returns user data useful in API responses
        """
        return {
            'id': self.id,
            'name': self.name,
            'actor': self.actor,
            'role': self.role,
            'description': self.description,
            'sitcom_id': self.sitcom_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }