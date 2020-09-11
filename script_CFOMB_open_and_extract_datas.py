import csv
# read flash.dat to a list of lists
datContent = open("GRPID215723796.dat").readlines() # read file
datContent = datContent[0] #open in one element of list > firt element in var

longeur_fichier = int(len(datContent)/120) #120 caracters in one record
occurence = list(range(0, len(datContent), 120))


list1=list(range(0,longeur_fichier,1)) # make liste in function of specific file
list2=[]
for x in list1: 
        result = (x * 120)
        list2.append(result)


occurence.pop(0) 
rajout_occurence = (occurence[-1]+120) #add one more occurence to add same len() and to get las record of file
occurence.append((occurence[-1]+120))

listedelignes=[]
for i,j in zip(list2,occurence): # build list of lines records
    line=datContent[i:j]    
    listedelignes.append(line)


code_banque = listedelignes[0][2:7]
code_guichet = listedelignes[0][11:16]
numero_de_compte = listedelignes[0][21:32]

montant_debut = float(listedelignes[0][90:103]) # get from firt line
montant_fin = float(listedelignes[-1][90:103]) # get from last line
rib = code_banque +' '+ code_guichet+' ' + numero_de_compte 

print(f'RIB: {rib}')
print(f'Montant Début: {montant_debut}€')
print(f'Monant fin: {montant_fin}€')