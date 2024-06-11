
from file.extentions import db


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    mobileno = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(420), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    clinicplace = db.Column(db.String(200), nullable=False)
    doctor = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(400),nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    
    

    def __repr__(self):
        return f"Patient('{self.mobileno}', '{self.age}', '{self.address}', '{self.title}', '{self.content}', '{self.location}', '{self.image}')"