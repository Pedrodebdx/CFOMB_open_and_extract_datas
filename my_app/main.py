# main.py

from flask import Blueprint, render_template
from flask_table import Table, Col
from flask_login import login_required, current_user
import csv
from cfonb import StatementReader
import os
from flask import *  
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
#import pandas as pd

main = Blueprint('main', __name__)


 ## create csv, if user want to download it ###    
def create_csv(liste_sortie):
    '''
    df = pd.DataFrame(liste_sortie)  
    csv_data = df.to_csv(header=False)
    df.to_csv('./project/resultat.csv', index=False) 
  ''' 
    print('debut creation csv')
    import csv
    with open("resultat.csv", "w") as myfile:
        #print(myfile)
        wr = csv.writer(myfile)
        #print(liste_sortie)
        for word in liste_sortie:
            wr.writerow([word])
        
    print('fin creation csv')


## function allowing extraction
def script(file='4.dat'): 
   
    ### suppression d'un éventuel précédent fichier csv, généré à la fin
    try:
        os.remove("resultat.csv") #remove temp file
    except:
        pass    
    ##########################################    
    
    
    statement_file = open(file)
    reader = StatementReader() #reader of library

    try: # for classics files  with carriage return
        result =reader.parse(statement_file)
        print('on est dans le try')
    except: # for files without carriage return
        statement_file = open(file).readlines()
        statement_file = statement_file[0] # firt because just a long string
        tmp = '\r\n'.join(statement_file[i:i+120] for i in range(0, len(statement_file), 120)) # add a carriage return every 120 characters
        print('on est dans le except')
        with open('tmp.txt', 'w+') as fh:
            fh.write(tmp)   
            statement_file = open('tmp.txt')
            result =reader.parse(statement_file)
            os.remove("tmp.txt") #remove temp file
    
    liste_sortie = []        
    for j in list(range(0,len(result))):

        ligne1 = f'Compte numéro : {result[j].header["bank_code"]} {result[j].header["desk_code"]} {result[j].header["account_nb"]}'
        liste_sortie.append(ligne1)
        ligne2 = f'Solde début ({result[j].header["prev_date"]}) : {result[j].header["prev_amount"]}'
        liste_sortie.append(ligne2)
        ligne3 = f'Solde fin ({result[j].footer["next_date"]}) : {result[j].footer["next_amount"]}'
        liste_sortie.append(ligne3)
        ligne4 = ' '
        liste_sortie.append(ligne4)
     
    ## create csv, if user want to download it ###   
    print('appel de la fonction CSV') 
    create_csv(liste_sortie)
    print('apres appel de la fonction CSV') 

    
    return liste_sortie


@main.route('/')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/ofx')
@login_required
def ofx():
    return render_template('profile.html', name=current_user.name)

  
@main.route('/success', methods = ['POST'])
@login_required  
def success():   
    try:
        if request.method == 'POST':  
            f = request.files['file']  
            f.save(f.filename)
            liste_sortie= script(file=f.filename)
            os.remove(f.filename)  # delate file uploaded
        return render_template("success4.html", name = f.filename, liste_sortie=liste_sortie)   

    except:
        return redirect(url_for('auth.upload'))
    
@main.route('/upload')  
@login_required
def upload():  
    return render_template("profile.html")    