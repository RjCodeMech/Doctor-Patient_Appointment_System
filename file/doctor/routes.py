from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from file import db, bcrypt
import datetime
from file.models import Doctor, User, Booking
from file.doctor.forms import (DoctorRegistrationForm, AfterEmailValidateDoctorDetailsForm, UpdateDoctorAccountForm)
from file.main.forms import (LoginForm, PasswordResetForm, VerifiedPasswordResetForm)
from file.doctor.utils import doctor_save_picture
from file.token import generate_confirmation_token, confirm_token
from file.email import send_email
from file.decorators import is_confirmed, is_updated

doctor = Blueprint('doctor', __name__)


# Doctor login form starts
@doctor.route("/login", methods=['GET', 'POST'])
def docpor():
    # Form Validation Starts
    if current_user.is_authenticated and current_user.role == 'doctor':
        return redirect(url_for('doctor.docin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.email == form.email.data and user.role =="doctor" and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have been logged in as {user.email}!', 'green')
            return redirect(url_for("doctor.docin"))
        else:
            flash('Login Unsuccessful. Please check username and password. Try again!', 'red')

    return render_template('Doctor/docpor.html', title="Doctor's Portal", form = form)



@doctor.route("/registration", methods=['GET', 'POST'])
def docreg():
    form = DoctorRegistrationForm()

    if current_user.is_authenticated and current_user.role == 'doctor':
        return redirect(url_for('doctor.docin'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role="doctor", confirmed=False, verified=False)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('doctor.doctorverification', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        flash(f'Your account has been created {form.email.data}! Mail has been sent to you for the confirmation. Please confirm and login.', 'green')
        return redirect(url_for("doctor.docpor"))

    return render_template('Doctor/docreg.html', title="Doctor's Portal", form = form)


@doctor.route("/doctorverification/<token>", methods = ['GET', 'POST'])
def doctorverification(token):
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('The confirmation link is invalid or has expired.', 'red')
        return redirect(url_for('doctor.unconfirmed'))
    if user.confirmed and user.is_authenticated:
        flash('Account already confirmed! Please update the details.', 'green')
        return redirect(url_for("doctor.confirmeddoctordetailsupdate"))
    elif user.confirmed:
        flash('Account already confirmed! Please login.', 'green')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash(f'You have confirmed your account. Thanks!', 'green')
    return redirect(url_for("doctor.docpor"))


@doctor.route('/confirmeddoctordetailsupdate', methods=['GET', 'POST'])
@login_required
@is_confirmed
def confirmeddoctordetailsupdate():
    form = AfterEmailValidateDoctorDetailsForm()
    if form.validate_on_submit():
        current_user.verified = True
        current_user.verified_on = datetime.datetime.now()
        db.session.add(current_user)
        db.session.commit()
        docinfo = Doctor(user_id = current_user.id, mobileno=form.mobileno.data, qualification=form.qualification.data, experience=form.experience.data, department=form.department.data, clinicplace=form.clinicplace.data, address=form.address.data)
        db.session.add(docinfo)
        db.session.commit()
        flash(f'Congratulations! your account has been completed successfully. You can now able to book your appointment.', 'green')
        return redirect(url_for("doctor.docin"))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('Doctor/verifieddocreg.html', title="Doctor's Account", form = form)


@doctor.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("doctor.confirmeddoctordetailsupdate"))
    flash('Please confirm your account!', 'red')
    return render_template('unconfirmed.html', title = "Doctor's Account")

@doctor.route("/resend")
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('doctor.doctorverification', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'green')
    return redirect(url_for('doctor.unconfirmed'))

@doctor.route("/resetpassword", methods = ['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated and current_user.role == 'doctor':
        return redirect(url_for('doctor.docin'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('doctor.reset_link', token=token, _external=True)
        html = render_template('reset_request.html', confirm_url=confirm_url)
        subject = "Password reset request"
        send_email(user.email, subject, html)


        flash(f'An email has been sent to {form.email.data} with instructions to reset your password.', 'green')
        return redirect(url_for("doctor.docpor"))
    return render_template('reset_password.html', title="Doctor's Reset", form = form)

@doctor.route("/reset_link/<token>", methods = ['GET', 'POST'])
def reset_link(token):
    if current_user.is_authenticated and current_user.role == 'doctor':
        return redirect(url_for('doctor.docin'))
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('That is an invalid or expired token.', 'red')
        return redirect(url_for('doctor.reset_password'))
    form = VerifiedPasswordResetForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.session.commit()

        flash(f'Your password has been updated. You are now able to login.', 'green')
        return redirect(url_for("doctor.docpor"))
    return render_template('passwordchange.html', title="Doctor's Account", form = form)

@doctor.route(" /logout")
def doclogout():
    logout_user()
    flash('You have been logged out!', 'green')
    return redirect(url_for("doctor.docpor"))


@doctor.route("/account")
@login_required
@is_confirmed
@is_updated
def docin():
    bookings = Booking.query.all()
    doc = Doctor.query.filter_by(user_id = current_user.id).first()
    image_file = url_for('static', filename='profile_pics/' + doc.image_file)
    return render_template('/Doctor/docin.html', title="Doctor's Account", image_file=image_file, bookings =bookings)
 
@doctor.route("/account/update", methods = ['GET', 'POST'])
@login_required
@is_confirmed
@is_updated
def docupdate():
    form = UpdateDoctorAccountForm()
    doc = Doctor.query.filter_by(user_id = current_user.id).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = doctor_save_picture(form.picture.data)
            doc.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        doc.mobileno = form.mobileno.data
        db.session.commit()
        flash('Your account has been updated!', 'green')
        return redirect(url_for('doctor.docin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.mobileno.data = doc.mobileno
    image_file = url_for('static', filename='profile_pics/' + doc.image_file)
    return render_template('/Doctor/docupdate.html', title="Doctor's Update", image_file=image_file, form=form )