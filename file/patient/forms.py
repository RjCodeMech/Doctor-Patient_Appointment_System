from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,
IntegerField, TextAreaField, SelectField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                 ValidationError, InputRequired, NumberRange, Regexp)
from file.models import User, Patient

class PatientRegistrationForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Validate Email')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data, role='patient').first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

     
class AfterEmailValidatePatientDetailsForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    mobileno = StringField('Mobile Number', 
    validators=[DataRequired(), Length(min=10, max=10, message='Mobile number must be 10 digits.'), Regexp('^\d+$', message='Mobile number must contain only digits.')])
    age = IntegerField('Age', 
                       validators=[InputRequired(message='Age is required'), NumberRange(min=10, max=100, message='Age must be between 10 and 100')])
    address = StringField('Full Address',
                        validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_mobileno(self, mobileno):
        patinfo = Patient.query.filter_by(mobileno=mobileno.data).first()
        if patinfo:
            raise ValidationError('That mobile number is taken. Please choose a different one.')

        

class UpdatePatientAccountForm(FlaskForm):
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


class SelectDepartmentLocationForm(FlaskForm):
    department = SelectField('Select Speciality',
                        choices=[('cardiology', 'Cardiology'), ('dermatology', 'Dermatology'), 
                                              ('endocrinology', 'Endocrinology'), ('gastroenterology', 'Gastroenterology'),('neurology', 'Neurology'),('oncology', 'Oncology'),('orthopedics', 'Orthopedics'),('pediatrics', 'Pediatrics'),('psychiatry', 'Psychiatry'),('urology', 'Urology')])
    clinicplace = SelectField('Select Location',
                        choices=[('Mahaveer Nagar', 'Mahaveer Nagar'), ('Talwandi', 'Talwandi'), 
                                              ('Chhawni', 'Chhawni'), ('Anantpura', 'Anantpura'),('DCM Road', 'DCM Road'),('Vigyan Nagar', 'Vigyan Nagar'),('Keshavpura', 'Keshavpura'),('Basant Vihar', 'Basant Vihar'),('Dadabari', 'Dadabari'),('Rampura', 'Rampura'), ('Gumanpura', 'Gumanpura')])
    submit = SubmitField('Save')


class SchedulingForm(FlaskForm):
    doctor = SelectField('Select Doctor', choices=[('IN', 'India'), ('US', 'United States'), ('UK', 'United Kingdom')])
    date = StringField('Select Date', validators=[DataRequired()])
    time = StringField('Select Time Slot', validators=[DataRequired()])
    content = TextAreaField('Reason for Appointment', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')