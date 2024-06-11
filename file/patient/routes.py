from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from file import db, bcrypt
import datetime
from file.models import User, Patient, Booking, Doctor
from file.patient.forms import (AfterEmailValidatePatientDetailsForm, SelectDepartmentLocationForm,
                                 PatientRegistrationForm, UpdatePatientAccountForm, SchedulingForm)
from file.main.forms import (LoginForm, PasswordResetForm, VerifiedPasswordResetForm)
from file.patient.utils import patient_save_picture
from file.token import generate_confirmation_token, confirm_token
from file.email import send_email
from file.decorators import is_confirmed, is_updated

patient = Blueprint('patient', __name__)

# Patient login form starts
@patient.route("/login", methods = ['GET', 'POST'])
def home():
    form = LoginForm()
    if current_user.is_authenticated and current_user.role=='patient':
        return redirect(url_for('patient.patin'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.email == form.email.data and user.role == "patient" and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have been logged in as {user.email}!', 'green')
            return redirect(url_for("patient.patin"))
        else:
            flash('Login Unsuccessful. Please check username and password. Try again!', 'red')
    return render_template('index.html', title='Home', form=form)



@patient.route("/patientregistration", methods = ['GET', 'POST'])
def patireg():
    form = PatientRegistrationForm()
    if current_user.is_authenticated and current_user.role == 'patient':
        return redirect(url_for('patient.patin'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password = form.password.data, role="patient", confirmed=False, verified=False)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('patient.patientverification', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)


        flash(f'Your account has been created {form.email.data}! Mail has been sent to you for the confirmation. Please confirm and login.', 'green')
        return redirect(url_for("patient.home"))
    
    return render_template('Patient/patireg.html', title="Patient's Portal", form = form)


@patient.route("/patientverification/<token>", methods = ['GET', 'POST'])
def patientverification(token):
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('The confirmation link is invalid or has expired.', 'red')
        return redirect(url_for('patient.unconfirmed'))
    if user.confirmed and user.is_authenticated:
        flash('Account already confirmed! Please update the details.', 'green')
        return redirect(url_for("patient.verifiedpatireg"))
    if user.confirmed:
        flash('Account already confirmed! Please login.', 'green')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(f'You have confirmed your account. Thanks!', 'green')
    return redirect(url_for("patient.home"))


@patient.route("/verifiedpatientupdatedetails", methods = ['GET', 'POST'])
@login_required
@is_confirmed
def verifiedpatireg():
    form = AfterEmailValidatePatientDetailsForm()
    if form.validate_on_submit():
        current_user.verified = True
        current_user.verified_on = datetime.datetime.now()
        db.session.add(current_user)
        db.session.commit()
        patinfo = Patient(user_id = current_user.id, mobileno=form.mobileno.data, age=form.age.data,address=form.address.data)
        db.session.add(patinfo)
        db.session.commit()

        flash(f'Congratulations! your account has been completed successfully. You can now able to book your appointment.', 'green')
        return redirect(url_for("patient.patin"))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('Patient/verifiedpatireg.html', title="Patient's Account", form = form)


@patient.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("patient.verifiedpatireg"))
    return render_template('unconfirmed.html', title = "Patient's Account")

@patient.route("/resend")
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('patient.patientverification', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'green')
    return redirect(url_for('patient.unconfirmed'))


@patient.route("/resetpassword", methods = ['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated and current_user.role == 'patient':
        return redirect(url_for('patient.patin'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('patient.reset_link', token=token, _external=True)
        html = render_template('reset_request.html', confirm_url=confirm_url)
        subject = "Password reset request"
        send_email(user.email, subject, html)


        flash(f'An email has been sent to {form.email.data} with instructions to reset your password.', 'green')
        return redirect(url_for("patient.home"))
    return render_template('reset_password.html', title="Patient's Reset", form = form)

@patient.route("/reset_link/<token>", methods = ['GET', 'POST'])
def reset_link(token):
    if current_user.is_authenticated and current_user.role == 'patient':
        return redirect(url_for('patient.patin'))
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('That is an invalid or expired token.', 'red')
        return redirect(url_for('patient.reset_password'))
    form = VerifiedPasswordResetForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.session.commit()

        flash(f'Your password has been updated. You are now able to login.', 'green')
        return redirect(url_for("patient.home"))
    return render_template('passwordchange.html', title="Patient's Account", form = form)


@patient.route("/patientlogout")
def patlogout():
    logout_user()
    flash('You have been logged out!', 'green')
    return redirect(url_for("patient.home"))


@patient.route("/account")
@login_required
@is_confirmed
@is_updated
def patin():
    pat = Patient.query.filter_by(user_id = current_user.id).first()
    image_file = url_for('static', filename='p_profile_pics/' + pat.image_file)
    return render_template('/Patient/patin.html', title="Patient's Account", image_file=image_file)

@patient.route("/account/update", methods = ['GET', 'POST'])
@login_required
@is_confirmed
@is_updated
def patupdate():
    form = UpdatePatientAccountForm()
    pat = Patient.query.filter_by(user_id = current_user.id).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = patient_save_picture(form.picture.data)
            pat.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        pat.mobileno = form.mobileno.data
        db.session.commit()
        flash('Your account has been updated!', 'green')
        return redirect(url_for('patient.patin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.mobileno.data = pat.mobileno
    image_file = url_for('static', filename='p_profile_pics/' + pat.image_file)
    return render_template('/Patient/patupdate.html', title="Patient's Update", image_file=image_file, form=form )


@patient.route("/account/booking/selectdepartment", methods = ['GET', 'POST'])
@login_required
@is_confirmed
@is_updated
def selectdepartment():
    form = SelectDepartmentLocationForm()
    if form.validate_on_submit():
        booking = Booking(department=form.department.data, clinicplace=form.clinicplace.data)
        if form.department.data == Doctor.department and form.clinicplace.data == Doctor.clinicplace:
            db.session.add(booking)
            flash(f'Data Saved!', 'green')
            return redirect(url_for('patient.bookingschedule'))
        elif form.department.data != Doctor.department:
            flash(f"Sorry! No Doctor's are available in this specialization. Try again.", 'red')
            return redirect(url_for('patient.selectdepartment'))
        elif form.clinicplace.data != Doctor.clinicplace:
            flash(f"Sorry! No Doctor's are available in this place. Try again.", 'red')
            return redirect(url_for('patient.selectdepartment'))
    return render_template('/Patient/selectdepaandloc.html', form=form )


@patient.route("/account/booking/schedule", methods = ['GET', 'POST'])
@login_required
@is_confirmed
@is_updated
def bookingschedule():
    form = SchedulingForm()
    if form.validate_on_submit():
        pat = Patient.query.filter_by(user_id = current_user.id).first()
        booking = Booking(user_id = pat.id, mobileno=pat.mobileno, age=pat.age, address=pat.address, image_file=pat.image_file, department=form.department.data, clinicplace=form.clinicplace.data, doctor=form.doctor.data, date=form.date.data, time=form.time.data, content=form.content.data)
        db.session.add(booking)
        db.session.commit()
        flash(f'Your booking has been done.', 'green')
        return redirect(url_for('patient.patin'))
    elif request.method == 'GET':
        form.department.data = booking.department
        form.clinicplace.data = booking.clinicplace
    return render_template('/Patient/book_apntment.html', form=form )