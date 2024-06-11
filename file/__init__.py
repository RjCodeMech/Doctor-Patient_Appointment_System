from flask import Flask


from file.extentions import db, bcrypt, login_manager, mail

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1930c69ab4d63f89219322784fb38f9c'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
    app.config["SECURITY_PASSWORD_SALT"] = 'my_precious_two'
    app.config['DEBUG'] = False
    app.config['BCRYPT_LOG_ROUNDS'] = 13
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['DEBUG_TB_ENABLED'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # configuration of mail 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'XXXX'
    app.config['MAIL_PASSWORD'] = 'XXXX'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'from@example.com'

    db.init_app(app)
    with app.app_context():
        from file.models import User, Doctor, Patient, Booking
        db.create_all()


    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'patient.home'
    login_manager.login_message_category = 'orange'
    

    from file.doctor.routes import doctor
    app.register_blueprint(doctor, url_prefix='/doctor')

    from file.patient.routes import patient
    app.register_blueprint(patient, url_prefix='/patient')

    from file.main.routes import main
    app.register_blueprint(main)

    return app
