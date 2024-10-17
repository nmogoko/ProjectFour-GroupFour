#  This is the entry point of our application
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
from src.models import ReadingList, User, db, Task
from src.utils import with_user_middleware
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, create_access_token
import datetime


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)


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
    new_user = User(email=email, password=hashed_password, created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
    return jsonify(access_token=access_token), 200

@app.route('/logout', methods=['POST'])
def logout():
    # Client-side token removal approach, no server-side revocation needed
    return jsonify({"msg": "Logout successful."}), 200


@app.route('/reading-list', methods=['GET'])
def get_reading_list():
    reading_list = ReadingList.query.all()
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
        status=data.get('status'),  # Optional, if status is not provided it can be None
        created_at=datetime.datetime.utcnow().isoformat(),  # Using ISO format for created_at
        user_id=g.user_id
    )

    # Add the new item to the database session and commit
    db.session.add(new_reading_item)
    db.session.commit()

    # Return the serialized representation of the new reading list item
    return jsonify(new_reading_item.reading_list_serializer()), 201




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

    new_task = Task(task_title=data['task_title'], user_id=g.user_id, created_at=datetime.datetime.now(datetime.timezone.utc))
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




if __name__ == "__main__":
    app.run(debug=True)
