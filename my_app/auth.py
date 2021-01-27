# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, Response,send_from_directory,send_file
from flask_table import Table, Col
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
import os
import datetime
import random
import string
from flask_mail import Mail, Message # pour l'envoie du mdp par mail
from . import create_app
import script_ofx_to_cfonb

auth = Blueprint('auth', __name__)


# mot de passe aleatoire 
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Merci de  vérifier votre identifiant et/ou mot de passe.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    if "@exco.fr" not in email: # @exco.fr is not in mail registered, reject  
        flash("Utilisez votre adresse profesionnelle pour vous enregistrer")
        return redirect(url_for('auth.signup'))
    
    name = request.form.get('name')
    password = get_random_string(6)

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Cet email est déjà enregistré dans la base de données...')
        return redirect(url_for('auth.signup'))
    

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # sent message
    mail = Mail(create_app()) 
    body = "Merci de vous être enregistré. Votre mot de passe pour vous connecter à l'application est "+password
    recipients = []
    recipients.append(email)
    msg = Message(subject='Mot de passe application EXCO', sender = 'digital@myexco.fr', recipients = recipients, body=body)
    mail.connect()
    mail.send(msg)

    flash('Le mot de passe a été envoyé sur votre boite mail')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
'''
@auth.route('/success')
@login_required
def success():   
    try:
        if request.method == 'POST':  
            
            f = request.files['file']  
            f.save(f.filename)
            liste_sortie= script(file=f.filename)
            #os.remove(f.filename)  # delate file uploaded

        return render_template("success4.html", name = f.filename, liste_sortie=liste_sortie)   

    except:
        return redirect(url_for('auth.upload'))
'''    

@auth.route('/upload')  
@login_required
def upload():  
    return render_template("profile.html")      


@auth.route('/download', methods=['GET', 'POST'])
@login_required
def download():

    file_path = "../datas/resultat_extrait_cfonb.csv"
    resp = send_file(file_path,as_attachment=True,attachment_filename="resultat.csv")
    return resp

############################# Ofx to cfonb ############################
@auth.route('/ofx')
@login_required
def ofx():
    return render_template('ofx.html')


@auth.route('/transform_ofx_to_cfonb', methods=['GET', 'POST'])
@login_required
def transform_ofx_to_cfonb():
    try:
        if request.method == 'POST':  
            f = request.files['file']  
            f.save(f.filename)
            file=f.filename

            txs,acct,stmts = script_ofx_to_cfonb.read_ofx(file = file) #fonction 1 du script
            script_ofx_to_cfonb.write_cfonb_from_ofx(txs,acct,stmts)   #fonction 2 du script

            file_path = "../datas/fichier_converti.cfonb"
            resp = send_file(file_path,as_attachment=True,attachment_filename="fichier_converti.cfonb")  # renvoi du fichier sur la meme page
            return resp     


    except:
        return redirect(url_for('auth.ofx'))    