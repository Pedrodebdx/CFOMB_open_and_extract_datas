import csv
from pythoncfonb import StatementReader
import os

file='2.dat' #choose your cfonb file
statement_file = open(file)
reader = StatementReader() #reader of library

try: # for classics files  with carriage return
    result =reader.parse(statement_file)

except: # for files without carriage return
    statement_file = open(file).readlines()
    statement_file = statement_file[0] # firt because just a long string
    tmp = '\r\n'.join(statement_file[i:i+120] for i in range(0, len(statement_file), 120)) # add a carriage return every 120 characters

    with open('tmp.txt', 'w+') as fh:
        fh.write(tmp)   
        statement_file = open('tmp.txt')
        result =reader.parse(statement_file)
        os.remove("tmp.txt") #remove temp file
        
for j in list(range(0,len(result))):
    print(f'Compte numéro : {result[j].header["bank_code"]} {result[j].header["desk_code"]} {result[j].header["account_nb"]}')
    print(f'Solde début ({result[j].header["prev_date"]}) : {result[j].header["prev_amount"]}')
    print(f'Solde fin ({result[j].footer["next_date"]}) : {result[j].footer["next_amount"]}')
    print(' ')
