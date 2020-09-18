import csv
from cfonb import StatementReader
import os

file='4.dat' #choose your cfonb file
statement_file = open(file)
reader = StatementReader()

try:
    result =reader.parse(statement_file)
    print('dans le try')

except: 
    print('dans le except')
    statement_file = open(file).readlines()
    statement_file = statement_file[0]
    tmp = '\r\n'.join(statement_file[i:i+120] for i in range(0, len(statement_file), 120))

    with open('tmp.txt', 'w+') as fh:
        fh.write(tmp)   
        statement_file = open('tmp.txt')
        result =reader.parse(statement_file)
        os.remove("tmp.txt")
        
for j in list(range(0,len(result))):
    print(result[j].header["account_nb"])
    print(result[j].footer["account_nb"])

