from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, func, Float
from decimal import Decimal
from app import *
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=True)
    lastName = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    userName = db.Column(db.String(100), nullable=False, unique=True)
    userPass = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
   
    def __repr__(self):
        return "<User %r>" % self.userName
    
    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "userName": self.userName,
            "isAdmin": self.isAdmin,
            "bio": self.bio,
        }

    def add_user(_firstName, _lastName, _email, _userName, _userPass, _bio, _isAdmin):
        new_user = User(firstName=_firstName, lastName=_lastName, email=_email, userName=_userName, userPass=_userPass, bio=_bio, isAdmin=_isAdmin)
        db.session.add(new_user)
        db.session.commit()
    
    def get_user(_id):
        return [User.serialize(User.query.filter_by(id=_id).first())]
    
    def get_all_users():
        return [User.serialize(user) for user in User.query.all()]
    
    def update_user(_id, _firstName, _lastName, _email, _userName, _userPass, _bio, _isAdmin):
        user_to_update = User.query.filter_by(id=_id).first()
        user_to_update.firstName = _firstName if _firstName is not None else user_to_update.firstName
        user_to_update.lastName = _lastName if _lastName is not None else user_to_update.lastName
        user_to_update.email = _email if _email is not None else user_to_update.email
        user_to_update.userName = _userName if _userName is not None else user_to_update.userName
        user_to_update.userPass = _userPass if _userPass is not None else user_to_update.userPass
        user_to_update.bio = _bio if _bio is not None else user_to_update.bio
        user_to_update.isAdmin = _isAdmin if _isAdmin is not None else user_to_update.isAdmin
        db.session.commit()

    def delete_user(_username):
        User.query.filter_by(userName=_username).delete()
        db.session.commit()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer)
    director = db.Column(db.String(50), nullable=False)
    comment_text= db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return "<Movie %r>" % self.name

class Favorites(db.Model):
    # __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    movie_id =  db.Column(db.String(50), db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user= db.relationship('User',         
        backref=db.backref('favorites', lazy=True))     
    movie= db.relationship('Movie',         
        backref=db.backref('favorites', lazy=True))

    def __repr__(self):
        return "<Favorites %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "user_id": self.user_id,
        }

   
    
    def add_favorite(self, _movie_id, _user_id):
        new_user = User(movie_id=_movie_id, user_id=_user_id)
        db.session.add(new_favorite)
        db.session.commit()

    def delete_favorite(_id):
        Favorite.query.filter_by(id=_id).delete()
        db.session.commit()

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
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "rate": self.rate,
        }
    
    def rate_movie(self,_idUser, _idMovie, _rate):
        new_rate = Rate(user_id=_idUser, movie_id=_idMovie, rate=_rate)
        db.session.add(new_rate)
        db.session.commit()

    def movies_rates_avgs():
        #print (db.session.query(Rate.movie_id, cast(func.avg(Rate.rate), Float).\
        #            label('rate_avg')).\
        #            group_by(Rate.movie_id).all())
        return [MovieRateAVG.serialize(movierateavg) for movierateavg in db.session.query(Rate.movie_id, cast(func.avg(Rate.rate), Float).\
                     label('rate_avg')).\
                     group_by(Rate.movie_id).all()]


class MovieRateAVG():
    movie_id = db.Column(db.String(10), db.ForeignKey('movie.id'),nullable=False)
    rate_avg = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            "movie_id": self.movie_id,
            "rate_avg": self.rate_avg,
        }

    # def to_dict(self):
#     return{}

#     def to_dict(self):
#         return{}


        
# ## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')


 
