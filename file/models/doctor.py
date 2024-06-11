
from file.extentions import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),unique=True)
    mobileno = db.Column(db.Integer, unique=True, nullable=False)
    qualification = db.Column(db.String(120), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    clinicplace = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(420), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Doctor('{self.mobileno}','{self.qualification}', '{self.experience}', '{self.department}', '{self.image}')"
