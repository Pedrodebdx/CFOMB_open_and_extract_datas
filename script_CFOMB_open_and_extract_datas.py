import csv
# read flash.dat to a list of lists
datContent = open("GRPID215861116.dat").readlines()
datContent = datContent[0]

code_banque = datContent[2:7]
code_guichet = datContent[11:16]
numero_de_compte = datContent[21:32]

montant = datContent[90:103]

rib = code_banque + code_guichet + numero_de_compte +zone_reservee

montant = float(montant)
montant

celule01 = datContent[0:119]
celule04 = datContent[120:239] 
celule05 = datContent[240:360]
celule07 = datContent[360:480]




########################################################



import csv
# read flash.dat to a list of lists
datContent = open("GRPID215861116.dat").readlines()
datContent = datContent[0]

longeur_fichier = int(len(datContent)/120)
occurence = list(range(0, len(datContent), 120))


list1=list(range(0,longeur_fichier,1))
list2=[]
for x in list1: 
        result = (x * 120)-120
        list2.append(result)

list2.pop(0)
occurence.pop(0)

listedelignes=[]
for i,j in zip(list2,occurence):
    line=datContent[i:j]    
    listedelignes.append(line)

#############################################################


import csv

datContent = open("GRPID215861116.dat").readlines()
datContent[0].split('\n')


filename = "GRPID215861116.dat"
fileContents = open(filename,"r").read()
f = open(filename,"w", newline="\n")
f.write(fileContents)
f.close()