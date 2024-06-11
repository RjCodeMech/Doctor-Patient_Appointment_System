# from datetime import datetime
from flask_login import UserMixin
from file.extentions import db, login_manager, bcrypt
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10),nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_on = db.Column(db.DateTime, nullable=True)
    

    def __init__(self, username, email, password, role, confirmed, verified, confirmed_on=None, verified_on=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.role = role
        self.registered_on = datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.verified = verified
        self.verified_on = verified_on
        

        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"