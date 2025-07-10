# Sitcomverse API

## Project Overview
- The Sitcomverse API is a robust Restful backend application designed to manage and serve comprehensive data about sitcoms, their characters, and user-submitted reviews. It provides a structured and secure way to interact with data related to your favorite TV comedies.
- This API will serve as the robust, scalable backend for a potential future community-driven web application dedicated to sitcom enthusiasts.

## Features
This project demonstrates a strong understanding of backend development principles, database design, and advanced API concepts, going beyond basic CRUD operations.

### Core Functionality
- **User Authentication & Authorization:**
    * Secure user registration and login using JWT (JSON Web Tokens).
    * Protected routes ensuring only authenticated users can perform certain actions.
- **Sitcom Management (CRUD):**
    * Full Create, Read, Update, and Delete operations for sitcoms.
- **Character Management (CRUD):**
    * Full Create, Read, Update, and Delete operations for characters, specifically nested under their respective sitcoms.
- **Review/Rating System (CRUD):**
    * Users can submit, view, update, and delete reviews and star ratings for sitcoms.

### Advanced Features & Design Choices
- **Fine-Grained Authorization & Ownership:**
    * Users can only create, update, or delete sitcoms that they themselves own.
    * Users can only add characters to sitcoms they created.
    * Users can only update or delete reviews that they personally submitted.
- **Composite Unique Constraint for Reviews:**
    * Implemented a database-level unique constraint (*_user_sitcom_review_uc*) ensuring that a single user can submit only one review per sitcom. This guarantees data integrity and prevents spamming.
- **Dynamic Average Rating Calculation:**
    * Sitcoms dynamically display an *average_rating* field, calculated on-the-fly from all associated user reviews using SQL aggregation functions.
- **Nested Resource Design:**
    * Characters and Reviews are logically nested under Sitcoms in the API routes (e.g., /sitcoms/<id>/characters), reflecting their hierarchical relationship and improving API clarity.
- **Structured Error Handling:**
    * The API provides clear and consistent JSON error responses with appropriate HTTP status codes (e.g., 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict).

## Technologies Used
- **Backend Framework:** Flask
- **ORM (Object-Relational Mapper):** SQLAlchemy
- **Database:** MySQL (via pymysql driver)
- **Authentication:** Flask-JWT-Extended
- **Development Tools:** Visual Studio Code (for programming), MySQL Workbench (for database management), Postman (for API testing)
- **Python Libraries:** datetime, sqlalchemy.func

## Setup and Installation
Step-by-step instructions on how to get the Sitcomverse API running locally.
1. **Prerequisites:**
    - Python 3.x (Ensure you have a recent version like python 3.11.5, but 3.8+ is also fine)
    - MySQL Server (and optionally MySQL Workbench for database management)
    - pip: Python package installer (usually comes with Python)
2. **Clone the Repository:**
```
git clone https://github.com/benjah05/sitcomverse_api.git
cd sitcomverse_api
```
3. **Create And Activate Virtual Environment:**
```
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
4. **Install Dependencies:**
```
pip install -r requirements.txt
# If requirements.txt is not present, run:
# pip install flask flask-sqlalchemy pymysql flask-jwt-extended
```
After installing, you can create a *requirements.txt* file by running *pip freeze > requirements.txt* in your activated virtual environment for future use.
5. **Database Configuration:**
- Create a MySQL Database: Connect to your MySQL server (e.g., via MySQL Workbench or command line) and create a new database. We used sitcomverse in development.
```
CREATE DATABASE sitcomverse;
```
- Update app/config.py: Open app/config.py and configure your database connection string and JWT secret key.
```
# app/config.py
import os

class Config:
    # Replace 'your_mysql_user', 'your_mysql_password', and 'sitcomverse'
    # with your actual MySQL credentials and database name.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_mysql_user:your_mysql_password@localhost/sitcomverse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Generate a strong, unique secret key for JWT.
    # For production, use an environment variable (e.g., os.environ.get('JWT_SECRET_KEY')).
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a_very_secret_and_complex_key_for_your_jwt_tokens_12345'
```
- **Security Note:** For production deployments, JWT_SECRET_KEY and database credentials should be managed via environment variables, not hardcoded.
6. **Run the Application:**
```
python run.py
```
- This command will start the Flask development server.
- Upon the first run, db.create_all() will automatically create the necessary database tables (users, sitcoms, characters, reviews) based on your SQLAlchemy models.
- The API will be accessible at http://127.0.0.1:5000.

### Testing the API with Postman
Postman is a powerful tool for interacting with and testing the API endpoints.

1. **Download and Install Postman:** If you don't have it, download Postman from https://www.postman.com/downloads/.
2. **Import the Postman Collection JSON file:**
    - Download the Postman Collection JSON file from the repository: postman/Sitcomverse_API.postman_collection.json
    - Open Postman.
    - Click the Import button in the top-left corner.
    - Select File and choose the downloaded *Sitcomverse_API.postman_collection.json* file.
    - Click Import. This will add a collection named "SitcomVerse API" (or similar) to your Postman sidebar, containing all pre-configured requests.
3. **Using Pre-Configured Requests**  
Once the collection is imported, you can immediately start testing:
    - **Expand the Collection:** In the left sidebar, expand the "SitcomVerse API" collection.
    - **Browse Endpoints:** You will find all API endpoints (Auth, Sitcoms, Characters, Reviews) organized by folders, each with pre-configured HTTP methods, URLs, example request bodies (for POST/PATCH), and header setups (e.g., Authorization: Bearer <access_token>).
    - **Execute a Request:** Simply click on the desired request (e.g., POST Register User).
    - **Update Placeholders:** For requests requiring dynamic data (like access_token after login, or specific sitcom_id/character_id/review_id), remember to update the placeholder values in the URL or Headers/Body tab as needed.
    - **Send Request:** Click the blue Send button to execute the request and view the response in the lower panel.
3. **Creating Your Own Requests (Manual Testing):**  
If you prefer to build requests from scratch or want to experiment further:
    - **Start a New Request:** Click the + icon in Postman to create a new HTTP Request.
    - **Select HTTP Method:** Choose the appropriate method from the dropdown (e.g., GET, POST, PATCH, DELETE).
    - **Enter URL:** Input the full API URL (e.g., http://127.0.0.1:5000/api/auth/register).
    - **Configure Body (for POST/PUT):**  
        * Select the Body tab, choose raw, and set the type to JSON.
        * Enter your JSON payload in the text area.
    - **Add Headers (for Authentication):**
        * For protected endpoints, go to the Headers tab.* Add a Key of Authorization and a Value of Bearer <your_access_token>.
    - **Send Request:** Click Send to execute.

**Important:** Ensure your Flask API is running (python run.py) before sending any requests.

## API Endpoints
All API endpoints are prefixed with /api. Authentication-required endpoints expect a Bearer token in the Authorization header. Variable parts of the URL are indicated by {} (e.g., {sitcom_id}).

### Authentication Endpoints (/api/auth)
- **POST** /api/auth/register
    + **Description:** Registers a new user with a unique username and email.
    + **Request Body:**
    ```
    {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    ```
    + **Response (201 Created):**
    ```
    {"message": "User registered successfully"}
    ```
    + **Error (409 Conflict):** If username or email already exists.
- **POST** /api/auth/login
    + **Description:** Authenticates a user and returns a JWT access token.
    + Request Body:
    ```
    {
        "username": "testuser",
        "password": "password123"
    }
    ```
    + **Response (200 OK):**
    ```
    {"access_token": "eyJhbGciOiJIUzI1Ni..."}
    ```
    + **Error (401 Unauthorized):** For invalid credentials.
- **GET** /api/auth/protected (Requires JWT) 
    + **Description:** A sample protected route to verify JWT validity.
    + **Headers:** Authorization: Bearer <your_access_token>
    + **Response (200 OK):**
    ```
    {"logged_in_as": 1, "message": "Access granted!"}
    ```
    + **Error (401 Unauthorized):** For missing or invalid token.

### Sitcom Endpoints (/api/sitcoms)
- **POST** /api/sitcoms (Requires JWT)
    + **Description:** Creates a new sitcom, owned by the authenticated user.
    + **Headers:** Authorization: Bearer <access_token>
    + **Request Body:**
    ```
    {
        "title": "The Office (US)",
        "creator": "Greg Daniels",
        "genre": "Mockumentary Sitcom",
        "years_active": "2005-2013",
        "number_of_seasons": 9,
        "synopsis": "A group of eccentric office workers at a paper company."
    }
    ```
    + **Response (201 Created):**
    ```
    {
        "message": "Sitcom created successfully",
        "sitcom": {
            "id": 1,
            "title": "The Office (US)",
            "creator": "Greg Daniels",
            "genre": "Mockumentary Sitcom",
            "years_active": "2005-2013",
            "number_of_seasons": 9,
            "synopsis": "A group of eccentric office workers at a paper company.",
            "user_id": 1,
            "average_rating": null,
            "created_at": "2025-07-09T10:00:00.000000+00:00",
            "updated_at": "2025-07-09T10:00:00.000000+00:00"
        }
    }
    ```
    + **Error (409 Conflict):** If a sitcom with the same title already exists.

- **GET** /api/sitcoms
    + **Description:** Retrieves a list of all sitcoms, including their calculated average ratings.
    + **Response (200 OK):**
    ```
    [
        {
            "id": 1,
            "title": "The Office (US)",
            "average_rating": 4.5,
            "genre": "Mockumentary Sitcom",
            "user_id": 1,
            "created_at": "...",
            "updated_at": "...",
            "creator": "Greg Daniels",
            "number_of_seasons": 9,
            "synopsis": "A group of eccentric office workers at a paper company.",
            "years_active": "2005-2013"
        },
        {
            "id": 2,
            "title": "Friends",
            "average_rating": 4.0,
            "genre": "Sitcom",
            "user_id": 2,
            "created_at": "...",
            "updated_at": "...",
            "creator": "David Crane, Marta Kauffman",
            "number_of_seasons": 10,
            "synopsis": "Six young adults living in Manhattan as they navigate life and love."
        }
    ]
    ```

- **GET** /api/sitcoms/{sitcom_id}
    + **Description:** Retrieves details of a specific sitcom by ID, including its average rating.
    + **Response (200 OK):**
    ```
    {
        "id": 1,
        "title": "The Office (US)",
        "average_rating": 4.5,
        "genre": "Mockumentary Sitcom",
        "user_id": 1,
        "created_at": "...",
        "updated_at": "...",
        "creator": "Greg Daniels",
        "number_of_seasons": 9,
        "synopsis": "A group of eccentric office workers at a paper company.",
        "years_active": "2005-2013"
    }
    ```
    + **Error (404 Not Found):** If sitcom ID does not exist.

- **PUT** /api/sitcoms/{sitcom_id} (Requires JWT, Ownership)
    + **Description:** Updates an existing sitcom. Only the sitcom's creator can update it.
    + **Headers:** Authorization: Bearer <access_token>
    + **Request Body (partial updates allowed):**
    ```
    {"number_of_seasons": 10, "synopsis": "The beloved American sitcom..."}
    ```
    + **Response (200 OK):**
    ```
    {"message": "Sitcom updated successfully", "sitcom": {...updated_sitcom_data...}}
    ```
    + **Error (403 Forbidden):** If user is not the sitcom's creator.

- **DELETE** /api/sitcoms/{sitcom_id} (Requires JWT, Ownership)
    + **Description:** Deletes a sitcom. Only the sitcom's creator can delete it.
    + **Headers:** Authorization: Bearer <access_token>
    + **Response (200 OK):**
    ```
    {"message": "Sitcom deleted successfully"}
    ```
    + **Error (403 Forbidden):** If user is not the sitcom's creator.

### Other Endpoints (Characters & Reviews)
**NOTE:** The API also includes full CRUD operations for Characters and Reviews. These endpoints are designed with similar principles as the Sitcom endpoints, including nested routing (/api/sitcoms/{sitcom_id}/characters and /api/sitcoms/{sitcom_id}/reviews), JWT authentication, and fine-grained ownership/authorization checks. Once you are familiar with the authentication and sitcom endpoints, interacting with the character and review endpoints will be intuitive.

## Error Handling
* The API provides clear and consistent JSON error responses with appropriate HTTP status codes to facilitate easier debugging and consumption by client applications. Common error responses include:
    - **400 Bad Request:** Invalid input data (e.g., missing required fields, incorrect data types).
    - 401 Unauthorized: Missing or invalid JWT access token.
    - **403 Forbidden:** User does not have permission to perform the action (e.g., trying to update another user's sitcom).
    - **404 Not Found:** The requested resource (user, sitcom, character, review) does not exist.
    - **409 Conflict:** A resource already exists (e.g., registering with an existing username/email, submitting a duplicate review).
    - **500 Internal Server Error:** Unexpected server-side issues.

## Future Enhancements
- **Pagination for all list endpoints:** Implement pagination for /api/sitcoms/<id>/characters and /api/sitcoms/<id>/reviews to handle large datasets more efficiently.
- **Search Functionality:** Add the ability to search for sitcoms, characters, or reviews by keywords.
- **User Profiles:** Expand user model with more profile information.
- **Image Uploads:** Allow users to upload cover images for sitcoms or profile pictures.
- **Frontend UI:** Develop a web-based or mobile application to consume this API.
- **More Complex Relationships:** Implement a many-to-many relationship for "Creators" to allow multiple creators per sitcom, and a creator to be associated with multiple sitcoms.