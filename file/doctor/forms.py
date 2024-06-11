from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from file.models import User, Doctor

class DoctorRegistrationForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Validate Email')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data,role="doctor").first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        

class AfterEmailValidateDoctorDetailsForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobileno = StringField('Mobile Number', 
                           validators=[DataRequired(), Length(min=10, max=10, message='Mobile number must be 10 digits.'), Regexp('^\d+$', message='Mobile number must contain only digits.')])
    qualification = StringField('Qualification',
                        validators=[DataRequired()])
    experience = FloatField('Experience',
                        validators=[DataRequired()])
    department = SelectField('Select Speciality',
                        choices=[('cardiology', 'Cardiology'), ('dermatology', 'Dermatology'), 
                                              ('endocrinology', 'Endocrinology'), ('gastroenterology', 'Gastroenterology'),('neurology', 'Neurology'),('oncology', 'Oncology'),('orthopedics', 'Orthopedics'),('pediatrics', 'Pediatrics'),('psychiatry', 'Psychiatry'),('urology', 'Urology')])
    clinicplace = SelectField('Select Location',
                        choices=[('Mahaveer Nagar', 'Mahaveer Nagar'), ('Talwandi', 'Talwandi'), 
                                              ('Chhawni', 'Chhawni'), ('Anantpura', 'Anantpura'),('DCM Road', 'DCM Road'),('Vigyan Nagar', 'Vigyan Nagar'),('Keshavpura', 'Keshavpura'),('Basant Vihar', 'Basant Vihar'),('Dadabari', 'Dadabari'),('Rampura', 'Rampura'), ('Gumanpura', 'Gumanpura')])
    address = StringField('Full Address',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_mobileno(self, mobileno):
        docinfo = Doctor.query.filter_by(mobileno=mobileno.data).first()
        if docinfo:
            raise ValidationError('That mobile number is taken. Please choose a different one.')

        

class UpdateDoctorAccountForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobileno = StringField('Mobile Number', 
                           validators=[DataRequired(), Length(min=10, max=10, message='Mobile number must be 10 digits.'), Regexp('^\d+$', message='Mobile number must contain only digits.')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')