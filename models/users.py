from flask_sqlalchemy import SQLAlchemy
from settings import *
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

    def delete_user(_id):
        User.query.filter_by(id=_id).delete()
        db.session.commit()
