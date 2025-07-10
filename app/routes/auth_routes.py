# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app import db, jwt
from app.models.user import User # Loads the model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Create a Blueprint for the authentication routes
# Groups related routes and register them with the main app
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """
    Handles user registration
    Expects JSON data with 'username', 'email', and 'password'
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic input validation
    if not username or not email or not password:
        return jsonify({"message": "Missing username, email, or password"}), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409
    
    # Create new user instance and hash password with Werkzeug
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()

        # Return the dictionary represenation of the user
        return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201

    except Exception as e:
        db.session.rollback() # Rollback in case of an error
        print(f"Error during user registration: {e}")
        return jsonify({"message": "Error registering user", "error": str(e)}), 500
    

@auth_bp.route('/login', methods=['POST'])
def login_user():
    """
    Handles user login and issues a JWT access token
    Expects JSON data with 'username' or 'email', and 'password'
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username_or_email = data.get('username') or data.get('email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({"message": "Missing username/email or password"}), 400
    
    # Find the user by username or email
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    # Check if user exists and password is correct
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    

@auth_bp.route('/protected', methods=['GET'])
@jwt_required() # Decorator to protect this route, requiring a valid JWT
def protected_route():
    """
    A protected route that requires a valid JWT
    Returns the identity of the current user (user ID)
    """
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id, message="You have access to this protected route!"), 200