from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db= SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=True, unique=True)
    name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(10), nullable=False)
    profile = db.Column(db.String(10), nullable=False)
   

    def __repr__(self):
        return "<User %r>" % self.password
    
    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "email":self.email,
            "username":self.username,
            "profile":self.profile,
        }

class Movie(db.Models):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer)
    director = db.Column((db.String(50), nullable=False)
    comment_text= Column(String(250), nullable=False)
    id_category = db.Column()
    id_rate = db.Column(Integer, primary_key=True)
    
    def __repr__(self):
        return "<Movie %r>" % self.name

class Favorites(db.Models):
    id = db.Column(db.Integer, primary_key=True)
    movie_id =  db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(100), nullable=True, unique=True)

    def __repr__(self):
        return "<Favorites %r>" % self.name

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=True, unique=True)
    movie_id =  db.Column(db.String(50), nullable=False)
    comment_text= Column(String(250), nullable=False)

    def __repr__(self):
        return "<Comment %r>" % self.name

class Rate(Base):
    __tablename__ = 'rate'
    id = Column(Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=True, unique=True)
    movie_id =  db.Column(db.String(50), nullable=False)
    rate = db.Column(Integer)

def to_dict(self):
    return{}

    def to_dict(self):
        return{}


        
## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')


 
