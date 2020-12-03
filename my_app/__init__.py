# init.py
# coding: utf-8


import csv
from cfonb import StatementReader
import os
from flask import *  
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message # pour l'envoie du mdp par mail
 


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    mail= Mail(app) # pour l'envoie du mdp par mail

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['MAX_CONTENT-PATH'] = 99999999999
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    app.config['MAIL_SERVER']='smtp.office365.com'               # pour l'envoie du mdp par mail
    app.config['MAIL_USE_TLS'] = True                             # pour l'envoie du mdp par mail
    app.config['MAIL_USE_SSL'] = False                             # pour l'envoie du mdp par mail    
    app.config['MAIL_PORT'] = 25                             # pour l'envoie du mdp par mail    
    app.config['MAIL_USERNAME'] = 'pierre-vincent.ferrat@exco.fr'     # pour l'envoie du mdp par mail
    app.config['MAIL_PASSWORD'] = 'Exco1pass!'               # pour l'envoie du mdp par mail
    mail = Mail(app)                                        # pour l'envoie du mdp par mail
    
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    if __name__ == '__main__':
        app.run(debug = True)     
