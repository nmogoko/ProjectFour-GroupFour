from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User():
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String(100))
    created_at = Column(DateTime)


class ReadingList():
    __tablename__ = 'reading_list'

    book_id = Column(Integer, primary_key=True)
    book_title = Column(String)
    user_id = Column(ForeignKey('users.id'))
    status = Column(Enum('Read', 'Unread', name='reading_list_status'))
    created_at = Column(DateTime)

    user = relationship('User')