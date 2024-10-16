# Database models go in here
from flask_sqlalchemy import SQLAlchemy
from serializers import SerializerMixin
import enum

db = SQLAlchemy()


class Status(enum.Enum):
    Read = "Read"
    Unread = "Unread"


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    reading_list = db.relationship('ReadingList', backref='reading_list',
                                   cascade="all, delete-orphan")
    tasks = db.relationship('Task', backref='daily_tasks_list', cascade="all, delete-orphan")

    def user_serializer(self):
        user_data = super().serialize()
        user_data['reading_list'] = [reading_list_item.reading_list_serializer()
                                     for reading_list_item in self.reading_list]
        user_data['tasks'] = [task_item.tasks_serializer()
                                     for task_item in self.tasks]
        return user_data


class ReadingList(db.Model, SerializerMixin):
    __tablename__ = 'reading_list'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String)
    status = db.Column(db.Enum(Status), nullable=True)
    created_at = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def reading_list_serializer(self):
        return super().serialize()

    # def reading_list_serializer(self):
    #     return {
    #         'book_id': self.id,
    #         'book_title': self.title,
    #         'status': self.status,
    #         'created_at': self.created_at
    #     }

class Task(db.Model):
    __tablename__ = 'daily_tasks_list'

    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(Status), nullable=True)
    created_at = db.Column(db.DateTime)

    def tasks_serializer(self):
        return super().serialize()
    
    