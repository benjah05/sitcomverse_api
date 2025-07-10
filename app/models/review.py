# app/models/review.py
from app import db
from datetime import datetime, timezone


class Review(db.Model):
    """
    Represents the sitcom reviews in the Sitcomverse API
    This model defines the 'reviews' table in the database
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False) # e.g., 1-5
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Foreign key to link to the User who wrote the review
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    # Foreign key to the link to the Sitcom being reviewed
    sitcom_id = db.Column(db.Integer, db.ForeignKey('sitcoms.id'), nullable=False)
    sitcom = db.relationship('Sitcom', backref=db.backref('reviews', lazy=True))

    # Composite Unique Constraint: A User can only review a specific sitcom once
    __table_args__ = (db.UniqueConstraint('user_id', 'sitcom_id', name='_user_sitcom_review_uc'),)

    def __repr__(self):
        """
        String representation of the Review object
        """
        return f'<Review ID: {self.id} | User: {self.user_id} | Sitcom: {self.sitcom_id} | Score: {self.score}>'
    
    def to_dict(self):
        """
        Converts the Review object to a dictionary
        Returns user data useful in API responses
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sitcom_id': self.sitcom_id,
            'score': self.score,
            'text': self.text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }