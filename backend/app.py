#  This is the entry point of our application
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from src.config import Config
from src.models import ReadingList, db


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


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
