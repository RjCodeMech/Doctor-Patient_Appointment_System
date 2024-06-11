from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.confirmed is False and current_user.role == "patient":
            flash('Please confirm your account!', 'red')
            return redirect(url_for('patient.unconfirmed'))
        elif current_user.is_authenticated and current_user.confirmed is False and current_user.role == "doctor":
            flash('Please confirm your account!', 'red')
            return redirect(url_for('doctor.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def is_updated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.verified is False and current_user.role == "patient":
            flash('Please update your account first!', 'red')
            return redirect(url_for('patient.verifiedpatireg'))
        elif current_user.is_authenticated and current_user.verified is False and current_user.role == "doctor":
            flash('Please update your account first!', 'red')
            return redirect(url_for('doctor.confirmeddoctordetailsupdate'))
        return func(*args, **kwargs)
 
    return decorated_function