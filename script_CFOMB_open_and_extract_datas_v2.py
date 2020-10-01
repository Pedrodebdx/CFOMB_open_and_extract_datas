import csv
from cfonb import StatementReader
import os

def script(file='4.dat'): 
    
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
        #print(f'Compte numéro : {result[j].header["bank_code"]} {result[j].header["desk_code"]} {result[j].header["account_nb"]}')
        #print(f'Solde début ({result[j].header["prev_date"]}) : {result[j].header["prev_amount"]}')
        #print(f'Solde fin ({result[j].footer["next_date"]}) : {result[j].footer["next_amount"]}')
        #print(' ')
        ligne1 = f'Compte numéro : {result[j].header["bank_code"]} {result[j].header["desk_code"]} {result[j].header["account_nb"]}'
        liste_sortie.append(ligne1)
        ligne2 = f'Solde début ({result[j].header["prev_date"]}) : {result[j].header["prev_amount"]}'
        liste_sortie.append(ligne2)
        ligne3 = f'Solde fin ({result[j].footer["next_date"]}) : {result[j].footer["next_amount"]}'
        liste_sortie.append(ligne3)
        ligne4 = ' '
        liste_sortie.append(ligne4)
    return liste_sortie
 



from flask import *  
from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)  
app.config['MAX_CONTENT-PATH'] = 99999999999
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')  
def upload():  
    return render_template("fileuploadform1.html")  

@app.route('/success', methods = ['POST'])  
def success():   
    try:
        if request.method == 'POST':  
            f = request.files['file']  
            f.save(f.filename)
            liste_sortie= script(file=f.filename)
            os.remove(f.filename)  # delate file uploaded
        return render_template("success4.html", name = f.filename, liste_sortie=liste_sortie)
    except:
        return redirect(url_for('upload'))

if __name__ == '__main__':
    app.run(debug = True) 