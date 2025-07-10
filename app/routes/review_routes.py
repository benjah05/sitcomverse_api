# app/routes/review_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.review import Review
from app.models.sitcom import Sitcom
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError # To catch unique constraint violation


# Create a Blueprint for review routes
review_bp = Blueprint('review', __name__)

# CREATE a Review for a specific sitcom
@review_bp.route('/sitcoms/<int:sitcom_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(sitcom_id):
    """
    Creates a new Review for a specific sitcom
    Expects JSON data
    """
    current_user_id = get_jwt_identity()

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    # Validate required fields for a review
    score = data.get('score')
    if score is None:
        return jsonify({"message": "Score is required"}), 400
    try:
        score = int(score)
        if not (1 <= score <= 5): # Using 1-5 star rating
            return jsonify({"message": "Score must be an integer between 1 and 5"}), 400
    except ValueError:
        return jsonify({"message": "Score must be an integer"}), 400
    
    text = data.get('text')

    new_review = Review(
        user_id=int(current_user_id),
        sitcom_id=sitcom_id,
        score=score,
        text=text
    )

    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review created successfully", "review": new_review.to_dict()}), 201
    except IntegrityError: # Catch the _user_sitcom_review_uc unique constraint violation
        db.session.rollback()
        return jsonify({"message": "You have already submitted a review for this sitcom"}), 409
    except Exception as e:
        db.session.rollback()
        print(f'Error creating review: {e}')
        return jsonify({"message": "Error creating review", "error": str(e)}), 500


# READ all Reviews for a specific Sitcom
@review_bp.route('/sitcoms/<int:sitcom_id>/reviews', methods=['GET'])
def get_all_reviews_for_sitcom(sitcom_id):
    """
    GET all the Reviews for sitcom with sitcom_id
    """
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    reviews = sitcom.reviews
    reviews_data = [review.to_dict() for review in reviews]
    return jsonify(reviews_data), 200

# READ a single Review for a specific Sitcom
@review_bp.route('/sitcoms/<int:sitcom_id>/reviews/<int:review_id>', methods=['GET'])
def get_review(sitcom_id, review_id):
    """
    GET a single Review for a Sitcom by Review ID
    """
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    review = Review.query.filter_by(id=review_id, sitcom_id=sitcom_id).first()
    if review:
        return jsonify(review.to_dict()), 200
    return jsonify({"message": "Review not found or does not belong to this sitcom"}), 404

# UPDATE an existing Review
@review_bp.route('/sitcoms/<int:sitcom_id>/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(sitcom_id, review_id):
    """
    Update an exisitng Review by ID
    Only authenticated users can update reviews
    """
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    review = Review.query.filter_by(id=review_id, sitcom_id=sitcom_id, user_id=int(current_user_id)).first()
    if not review:
        return jsonify({"message": "Review not found or you do not have permission to update it"}), 404
    
    score = data.get('score')
    if score is not None:
        try:
            score = int(score)
            if not (1 <= score <= 5):
                return jsonify({"message": "Score must be an integer between 1 and 5"}), 400
            review.score = score # Update only if valid
        except ValueError:
            return jsonify({"message": "Score must be an integer"}), 400
        
    review.text = data.get('text', review.text)

    try:
        db.session.commit()
        return jsonify({"message": "Review updated successfully", "review": review.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Error updating review: {e}')
        return jsonify({"message": "Error updating review", "error": str(e)})
    
# DELETE a Review
@review_bp.route('/sitcoms/<int:sitcom_id>/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(sitcom_id, review_id):
    """
    Delete a Review for a Sitcom by ID
    """
    current_user_id = get_jwt_identity()

    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    review = Review.query.filter_by(id=review_id, sitcom_id=sitcom_id, user_id=int(current_user_id)).first()
    if not review:
        return jsonify({"message": "Review not found or you do not have permission to delete it"}), 404
    
    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Error deleting review: {e}')
        return jsonify({"message": "Error deleting review", "error": str(e)}), 500