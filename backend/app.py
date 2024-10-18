#  This is the entry point of our application
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from src.config import Config
from src.models import ReadingList, User, db, Task, MovieList, Quicknote
from src.utils import with_user_middleware
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, decode_token, create_access_token, get_jwt_identity, create_refresh_token
import datetime


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://projectfour-groupfour-frontend.onrender.com"]}})

blacklist = set()

@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, password=hashed_password,
                    created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    user_data = {
        "id": user.id,
        "email": user.email
    }

    access_token = create_access_token(identity=user_data)
    refresh_token = create_refresh_token(identity=user_data)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)
    return jsonify(msg="Successfully logged out"), 200

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"msg": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Password reset email sent!"}), 200

    user_data = {
        "id": user.id,
        "email": user.email
    }

    # Create a password reset token that expires in 15 minutes
    reset_token = create_access_token(identity=user_data, expires_delta=datetime.timedelta(minutes=15))

    # Send email with reset link
    msg = Message(subject="Password Reset",
                  sender="noreply@yourapp.com",
                  recipients=[email])
    msg.body = f"Please click the link to reset your password: https://projectfour-groupfour-frontend.onrender.com/reset-password/{reset_token}"
    mail.send(msg)

    return jsonify({"msg": "Password reset email sent!"}), 200

@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"msg": "New password is required"}), 400

    try:
        # Decode the token to get the user identity
        decoded_token = decode_token(token)
        email = decoded_token['sub']['email']
    except Exception as e:
        return jsonify({"msg": "Invalid token"}), 401
    
    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

    # Update the password in the database using SQLAlchemy
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = hashed_password
        db.session.commit()
        return jsonify({"msg": "Password has been reset successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404

@app.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()

    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@app.route('/reading-list', methods=['GET'])
@with_user_middleware
def get_reading_list():
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    reading_list = ReadingList.query.filter_by(user_id=g.user_id).all()
    return jsonify([reading_list_item.reading_list_serializer() for reading_list_item in reading_list])


@app.route('/get_reading_list/<int:reading_list_id>', methods=['GET', 'DELETE'])
def get_single_reading_list(reading_list_id):
    reading_list = ReadingList.query.get(reading_list_id)

    if request.method == "GET":
        if reading_list is None:
            return jsonify({"message": f"Reading list with id {reading_list_id} not found."}), 404

        return jsonify(reading_list.reading_list_serializer())
    elif request.method == "DELETE":
        db.session.delete(reading_list)
        db.session.commit()

        return {"message": f"Reading list with id {reading_list_id} has been deleted"}


@app.route('/create_reading_list', methods=['POST'])
@with_user_middleware
def create_reading_list_item():
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    # Get JSON data from the request
    data = request.get_json()

    # Validate that the required data is present
    if not data or 'book_title' not in data:
        return jsonify({"error": "Bad Request", "message": "Book title is required"}), 400

    # Create a new ReadingList item
    new_reading_item = ReadingList(
        book_title=data['book_title'],
        # Optional, if status is not provided it can be None
        status=data.get('status'),
        # Using ISO format for created_at
        created_at=datetime.datetime.utcnow().isoformat(),
        user_id=g.user_id
    )

    # Add the new item to the database session and commit
    db.session.add(new_reading_item)
    db.session.commit()

    # Return the serialized representation of the new reading list item
    return jsonify(new_reading_item.reading_list_serializer()), 201


@app.route('/delete_reading_list/<int:book_id>', methods=['DELETE'])
@with_user_middleware
def delete_reading_list_item(book_id):
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    # Query the ReadingList item by book_id and user_id to ensure ownership
    reading_item = ReadingList.query.filter_by(
        book_id=book_id, user_id=g.user_id).first()

    # Check if the reading item exists
    if reading_item is None:
        return jsonify({"error": "Not Found", "message": "Reading list item not found"}), 404

    # Delete the reading item from the database
    db.session.delete(reading_item)
    db.session.commit()

    # Return a success message after deletion
    return jsonify({"message": "Reading list item deleted successfully"}), 200


@app.route('/tasks', methods=['GET'])
@with_user_middleware
def get_all_tasks():
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    task_list = Task.query.filter_by(user_id=g.user_id).all()
    return jsonify([task_list_item.tasks_serializer() for task_list_item in task_list])


@app.route('/create_task', methods=['POST'])
@with_user_middleware
def create_task():
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    if not data or 'task_title' not in data:
        return jsonify({"error": "Bad Request", "message": "Task title is required"}), 400

    new_task = Task(task_title=data['task_title'], user_id=g.user_id,
                    created_at=datetime.datetime.now(datetime.timezone.utc))
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.tasks_serializer()), 201


@app.route('/get_task/<int:task_id>', methods=['GET'])
@with_user_middleware
def get_task(task_id):
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    task = Task.query.filter_by(task_id=task_id, user_id=g.user_id).first()
    if task is None:
        return jsonify({"error": "Not Found"}), 404

    return jsonify(task.tasks_serializer()), 200


@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
@with_user_middleware
def delete_task(task_id):
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    task = Task.query.filter_by(task_id=task_id, user_id=g.user_id).first()
    if task is None:
        return jsonify({"error": "Not Found", "message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200

# Route to create a new movie
@app.route('/create_movies', methods=['POST'])
@with_user_middleware
def create_movie():
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401
    
    data = request.get_json()
    if not data or 'movie_title' not in data:
        return jsonify({"error": "Bad Request", "message": "Movie title is required"}), 400
    
    new_movie = MovieList(
        movie_title=data['movie_title'],
        user_id=g.user_id,  # Assuming you set user_id in g
        status=data.get('status', 'NotWatched'),
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    
    db.session.add(new_movie)
    db.session.commit()

    return jsonify(new_movie.movie_serializer()), 201

@app.route('/get_movie/<int:movie_id>', methods=['GET'])
@with_user_middleware
def get_movie(movie_id):
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    # Fetch the movie from the database for the given movie_id and user_id
    movie = MovieList.query.filter_by(movie_id=movie_id, user_id=g.user_id).first()

    # Check if the movie exists and belongs to the current user
    if movie is None:
        return jsonify({"error": "Not Found"}), 404

    # Return the serialized representation of the movie
    return jsonify(movie.movie_serializer()), 200

@app.route('/movies', methods=['GET'])
@with_user_middleware
def get_all_movies():
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    # Fetch all movies from the database for the current user
    movie_list = MovieList.query.filter_by(user_id=g.user_id).all()

    # Serialize the movie data
    return jsonify([movie.movie_serializer() for movie in movie_list]), 200

@app.route('/delete_movie/<int:movie_id>', methods=['DELETE'])
@with_user_middleware
def delete_movie(movie_id):
    # Check if the user is authenticated
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    # Fetch the movie from the database for the given movie_id and user_id
    movie = MovieList.query.filter_by(movie_id=movie_id, user_id=g.user_id).first()

    # Check if the movie exists and belongs to the current user
    if movie is None:
        return jsonify({"error": "Not Found", "message": "Movie not found"}), 404

    # Delete the movie
    db.session.delete(movie)
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Movie deleted successfully"}), 200

@app.route('/quicknotes', methods=['GET'])
@with_user_middleware
def get_all_quicknotes():
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    quicknote_list = Quicknote.query.filter_by(user_id=g.user_id).all()
    return jsonify([quicknote.quicknote_serializer() for quicknote in quicknote_list])

@app.route('/create_quicknote', methods=['POST'])
@with_user_middleware
def create_quicknote():
    print("Hello world")
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Bad Request", "message": "Title and content are required"}), 400

    new_quicknote = Quicknote(
        title=data['title'],
        content=data['content'],
        user_id=g.user_id,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.session.add(new_quicknote)
    db.session.commit()

    return jsonify(new_quicknote.quicknote_serializer()), 201

@app.route('/get_quicknote/<int:quicknote_id>', methods=['GET'])
@with_user_middleware
def get_quicknote(quicknote_id):
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    quicknote = Quicknote.query.filter_by(id=quicknote_id, user_id=g.user_id).first()
    if quicknote is None:
        return jsonify({"error": "Not Found"}), 404

    return jsonify(quicknote.quicknote_serializer()), 200

@app.route('/delete_quicknote/<int:quicknote_id>', methods=['DELETE'])
@with_user_middleware
def delete_quicknote(quicknote_id):
    if g.user_id is None:
        return jsonify({"error": "Unauthorized access"}), 401

    quicknote = Quicknote.query.filter_by(id=quicknote_id, user_id=g.user_id).first()
    if quicknote is None:
        return jsonify({"error": "Not Found", "message": "Quicknote not found"}), 404

    db.session.delete(quicknote)
    db.session.commit()
    return jsonify({"message": "Quicknote deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
