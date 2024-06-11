from flask import render_template, Blueprint, redirect, url_for

main = Blueprint('main', __name__)


@main.route("/", methods = ['GET', 'POST'])
def mainhome():
    return redirect(url_for('patient.home'))

@main.route("/about")
def aboutus():
    return render_template('about.html', title='About')

@main.route("/pharmacy")
def pharmacy():
    return render_template('pharmacy.html', title='Pharmacy')

@main.route("/hospitalization")
def hospitalization():
    return render_template('hospitalization.html', title='Hospitalization')

@main.route("/contactus")
def contactus():
    return render_template('contactus.html', title='Contact us')