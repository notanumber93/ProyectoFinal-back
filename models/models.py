from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import *
db = SQLAlchemy(app)

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# db= SQLAlchemy()

class Movie(db.Models):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer)
    director = db.Column((db.String(50), nullable=False)
    comment_text= Column(String(250), nullable=False)
    id_category = db.Column()
    id_rate = db.Column(Integer, primary_key=True)
    
#     def __repr__(self):
#         return "<Movie %r>" % self.name

# class Favorites(db.Models):
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id =  db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.String(100), nullable=True, unique=True)

#     def __repr__(self):
#         return "<Favorites %r>" % self.name

# class Comment(Base):
#     __tablename__ = 'comment'
#     id = Column(Integer, primary_key=True)
#     user_id = db.Column(db.String(100), nullable=True, unique=True)
#     movie_id =  db.Column(db.String(50), nullable=False)
#     comment_text= Column(String(250), nullable=False)

#     def __repr__(self):
#         return "<Comment %r>" % self.name

class Rate(db.Model):
    #__tablename__ = 'rate'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id =  db.Column(db.String(10), db.ForeignKey('movie.id'),nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    user= db.relationship('User',
        backref=db.backref('rate', lazy=True))
    movie= db.relationship('Movie',
        backref=db.backref('rate', lazy=True))
    
    def __repr__(self):
        return "<Rate %r>" % self.rate
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "rate": self.rate,
        }
    
    def rate_movie(self,_idUser, _idMovie, _rate):
        new_rate = Rate(user_id=_idUser, movie_id=_idMovie, rate=_rate)
        db.session.add(new_rate)
        db.session.commit()

    # def to_dict(self):
#     return{}

#     def to_dict(self):
#         return{}


        
# ## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')


 
