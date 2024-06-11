
from file.extentions import db


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    mobileno = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(420), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    
    

    def __repr__(self):
        return f"Patient('{self.mobileno}', '{self.age}', '{self.address}', '{self.image}')"
