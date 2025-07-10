# app/routes/character_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.character import Character
from app.models.sitcom import Sitcom
from flask_jwt_extended import jwt_required, get_jwt_identity


# Create a Blueprint for Character routes
character_bp = Blueprint('character', __name__)


# CREATE a new character for a specific Sitcom
@character_bp.route('/sitcoms/<int:sitcom_id>/characters', methods=['POST'])
@jwt_required()
def create_character(sitcom_id):
    """
    Adds a character to a specific Sitcom
    Expects JSON data
    """
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    if sitcom.user_id != int(current_user_id):
        return jsonify({"message": "Forbidden: You can only add characters to sitcoms you created"}), 403
    
    name = data.get('name')
    if not name:
        return jsonify({"message": "Character name is required"}), 400
    
    actor = data.get('actor')
    role = data.get('role')
    description = data.get('description')

    new_character = Character(
        name=name,
        actor=actor,
        role=role,
        description=description,
        sitcom_id=sitcom_id
    )

    try:
        db.session.add(new_character)
        db.session.commit()
        return jsonify({"message": "Character created successfully", "character": new_character.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating character: {e}")
        return jsonify({"message": "Error creating character", "error": str(e)}), 500
    

# READ all Characters for a specific Sitcom
@character_bp.route('/sitcoms/<int:sitcom_id>/characters', methods=['GET'])
def get_all_characters_for_sitcom(sitcom_id):
    """
    Read all Characters in a specific Sitcom
    """
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    characters = sitcom.characters
    characters_data = [character.to_dict() for character in characters]
    return jsonify(characters_data), 200


# READ a single Character by ID
@character_bp.route('/sitcoms/<int:sitcom_id>/characters/<int:character_id>', methods=['GET'])
def get_character(sitcom_id, character_id):
    """
    Read a single Character in a specific Sitcom (by ID)
    """
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    character = Character.query.filter_by(id=character_id, sitcom_id=sitcom_id).first()
    if character:
        return jsonify(character.to_dict()), 200
    return jsonify({"message": "Character not found or does not belong to this sitcom"}), 404


# UPDATE an existing Character
@character_bp.route('/sitcoms/<int:sitcom_id>/characters/<int:character_id>', methods=['PUT'])
@jwt_required()
def update_character(sitcom_id, character_id):
    """
    Update an existing character in a specific Sitcom
    """
    current_user_id = get_jwt_identity()

    data = request.get_json()
    if not data:
        return ({"message": "No input data provided"}), 400
    
    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    # Only the creator of the sitcom can update its characters
    if sitcom.user_id != int(current_user_id):
        return jsonify({"message": "Forbidden: You can only update characters for sitcoms you created"}), 404
    
    character = Character.query.filter_by(id=character_id, sitcom_id=sitcom_id).first()
    if not character:
        return jsonify({"message": "Character not found or does not belong to this sitcom"}), 404
    
    character.name = data.get('name', character.name)
    character.actor = data.get('actor', character.actor)
    character.role = data.get('role', character.role)
    character.description = data.get('description', character.description)

    try:
        db.session.commit()
        return jsonify({"message": "Character updated successfully", "character": character.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating character: {e}")
        return jsonify({"message": "Error updating character", "error": str(e)}), 500
    

# DELETE a Character
@character_bp.route('/sitcoms/<int:sitcom_id>/characters/<int:character_id>', methods=['DELETE'])
@jwt_required()
def delete_character(sitcom_id, character_id):
    """
    Delete a character in a specific Sitcom
    """
    current_user_id = get_jwt_identity()

    sitcom = Sitcom.query.get(sitcom_id)
    if not sitcom:
        return jsonify({"message": "Sitcom not found"}), 404
    
    # Only the creator of the sitcom can delete its characters
    if sitcom.user_id != int(current_user_id):
        return jsonify({"message": "Forbidden: You can only delete characters for sitcoms you created"}), 404
    
    character = Character.query.filter_by(id=character_id, sitcom_id=sitcom_id).first()
    if not character:
        return jsonify({"message": "Character not found or does not belong to this sitcom"}), 404

    try:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Character deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting character: {e}")
        return jsonify({"message": "Error deleting character", "error": str(e)}), 500