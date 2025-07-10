# app/models/sitcom.py
from app import db
from datetime import datetime, timezone # To handle created_at and updated_at timestamps
from sqlalchemy import func
from app.models.review import Review

class Sitcom(db.Model):
    """
    Represents a sitcom in the Sitcomverse API
    This model defines the 'sitcoms' table in the database
    """

    __tablename__ = 'sitcoms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    creator = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    years_active = db.Column(db.String(50)) # e.g., "2001-2010" or "2010-Present"
    number_of_seasons = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Foreign key to link to the User who created this sitcom entry
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Define the relationship to the User model
    creator_user = db.relationship('User', backref=db.backref('sitcoms', lazy=True))

    def __repr__(self):
        """
        String representation of the Sitcom object
        """
        return f'<Sitcom {self.title}>'
    
    def to_dict(self):
        """
        Converts the Sitcom object to a dictionary, excluding sensitive information
        Returns user data useful in API responses
        """
        
        # calculate the average rating
        # scalar() executes the query and returns a single value
        avg_score = db.session.query(func.avg(Review.score)).filter(Review.sitcom_id == self.id).scalar()
        if avg_score is not None:
            avg_score = round(float(avg_score), 1)
        else:
            avg_score = None

        return {
            'id': self.id,
            'title': self.title,
            'creator': self.creator,
            'genre': self.genre,
            'years_active': self.years_active,
            'number_of_seasons': self.number_of_seasons,
            'synopsis': self.synopsis,
            'user_id': self.user_id, # The ID of the user who added this sitcom
            'average_rating': avg_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }