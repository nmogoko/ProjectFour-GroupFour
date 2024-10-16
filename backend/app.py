#  This is the entry point of our application
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
from src.models import ReadingList, User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
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
    

@app.route('/reading-list', methods=['GET'])
def get_reading_list():
    reading_list = ReadingList.query.all()
    return jsonify([reading_list_item.reading_list_serializer() for reading_list_item in reading_list])


@app.route('/get_reading_list/<int:reading_list_id>', methods=['GET', 'DELETE'])
def get_single_reading_list(reading_list_id):
    reading_list = ReadingList.query.get(reading_list_id)

    if request.method == "GET":
        if reading_list is None:
            return jsonify({"message": f"reading list with id {reading_list_id} not found."}), 404

        return jsonify(reading_list.reading_list_serializer())
    elif request.method == "DELETE":
        db.session.delete(reading_list)
        db.session.commit()

        return {"message": f"artist with id {reading_list_id} has been deleted"}


if __name__ == "__main__":
    app.run(debug=True)
