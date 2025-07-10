# app/routes/sitcom_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.sitcom import Sitcom
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create a Blueprint for sitcom routes
sitcom_bp = Blueprint('sitcom', __name__)

# CREATE a new Sitcom
@sitcom_bp.route('/sitcoms', methods=['POST'])
@jwt_required() # Only authenticated users can create sitcoms
def create_sitcom():
    """
    Adds a sitcom to the database table 'sitcoms'
    Expects JSON data
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    title = data.get('title')
    genre = data.get('genre')
    
    if not title:
        return jsonify({"message": "Title is required"}), 400
    if not genre:
        return jsonify({"message": "Genre is required"}), 400
    

    if Sitcom.query.filter_by(title=title).first():
        return jsonify({"message": "Sitcom with this title already exists"}), 409
    
    # Handle optional fields
    creator = data.get('creator')
    years_active = data.get('years_active')
    synopsis = data.get('synopsis')

    number_of_seasons = data.get('number_of_seasons')
    if number_of_seasons is not None:
        try:
            number_of_seasons = int(number_of_seasons)
            if number_of_seasons < 0:
                return jsonify({"message": "Number of seasons cannot be negative"}), 400
        except ValueError:
            return jsonify({"message": "Number of seasons must be an integer"}), 400

    # Creare a new Sitcom instance with all extracted data
    new_sitcom = Sitcom(
        title=title,
        creator=creator,
        genre=genre,
        years_active=years_active,
        number_of_seasons=number_of_seasons,
        synopsis=synopsis,
        user_id=current_user_id # Link the sitcom to the user who created it
    )

    try:
        db.session.add(new_sitcom)
        db.session.commit()
        return jsonify({"message": "Sitcom created successfully", "sitcom": new_sitcom.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sitcom: {e}")
        return jsonify({"message": "Error creating sitcom", "error": str(e)}), 500
    
# READ all Sitcoms
@sitcom_bp.route('/sitcoms', methods=['GET'])
def get_all_sitcoms():
    """
    Read all Sitcoms in the database
    """
    sitcoms = Sitcom.query.all()
    # Convert list of Sitcom objects to list of dictionaries
    sitcoms_data = [sitcom.to_dict() for sitcom in sitcoms]
    return jsonify(sitcoms_data), 200

# READ a single Sitcom by ID
@sitcom_bp.route('/sitcoms/<int:sitcom_id>', methods=['GET'])
def get_sitcom(sitcom_id):
    """
    Read a single sitcom (from the database) by its ID
    """
    sitcom = Sitcom.query.get(sitcom_id) # get() is efficient for primary key lookup
    if sitcom:
        return jsonify(sitcom.to_dict()), 200
    return jsonify({"message": "Sitcom not found"}), 404

# UPDATE an existing sitcom
@sitcom_bp.route('/sitcoms/<int:sitcom_id>', methods=['PUT'])
@jwt_required()
def update_sitcom(sitcom_id):
    """
    Update a sitcom in the 'sitcoms' table
    """
    current_user_id = get_jwt_identity()
    sitcom = Sitcom.query.get(sitcom_id)

    if not sitcom:
        return jsonify({"message": "Sitcom not found"}, 404)
    
    # Only creator of sitcom can update it
    if sitcom.user_id != int(current_user_id):
        return jsonify({"message": "Forbidden: You can only update sitcoms you created"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    sitcom.title = data.get('title', sitcom.title)
    sitcom.creator = data.get('creator', sitcom.creator)
    sitcom.genre = data.get('genre', sitcom.genre)
    sitcom.years_active = data.get('years_active', sitcom.years_active)
    sitcom.number_of_seasons = data.get('number_of_seasons', sitcom.number_of_seasons)
    sitcom.synopsis = data.get('synopsis', sitcom.synopsis)

    try:
        db.session.commit()
        return jsonify({"message": "Sitcom updated successfully", "sitcom": sitcom.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating sitcom: {e}")
        return jsonify({"message": "Error updating sitcom", "error": str(e)}), 500
    
# DELETE a Sitcom
@sitcom_bp.route('/sitcoms/<int:sitcom_id>', methods=['DELETE'])
@jwt_required()
def delete_sitcom(sitcom_id):
    """
    Delete a Sitcom from the 'sitcom' table
    """
    current_user_id = get_jwt_identity()
    sitcom = Sitcom.query.get(sitcom_id)

    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404

    if sitcom.user_id != int(current_user_id):
        return jsonify({"message": "Forbidden: You can only delete sitcoms you created"}), 403
    
    try:
        db.session.delete(sitcom)
        db.session.commit()
        return jsonify({"message": "Sitcom deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting sitcom: {e}")
        return jsonify({"message": "Error deleting sitcom", "error": str(e)}), 500