import csv

# read .dat 
datContent = open("3.dat").readlines() # read file -> choise your file


#traitement des fichiers sans retour chariot de fin de ligne
if datContent[0][-1] !='\n':

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

#traitement des fichiers avec retour chariot de fin de ligne
elif datContent[0][-1] =='\n': 
    listedelignes=[]      
    for line_charriot in datContent:
        listedelignes.append(line_charriot[0:120])# on garde que les 120 premiers char
    
else:
    print("traitement des fichiers à revoir")
    pass

# fonction de récupération du rib dans la ligne
def get_rib(x):
    code_banque = x[2:7]
    code_guichet = x[11:16]
    numero_de_compte = x[21:32]
    rib = code_banque +' '+ code_guichet+' ' + numero_de_compte 
    return rib

#fonction  de récupération du montant/solde de la ligne envoyée
def parse_amount(amount_str, nb_of_dec):
    """ return a numerical amount from the cfonb amount string

    >>> from cfonb.parser.common import parse_amount
    >>> parse_amount('0001234{', 2)
    123.4
    >>> parse_amount('0000004843H', 2)
    484.38
    >>> parse_amount('000000920}', 2)
    -92.0
    >>> parse_amount('000117O', 3)
    -1.176
    """
    amount_str= amount_str[90:104]
    # insert the comma
    nb_of_dec = int(nb_of_dec)
    amount_str = amount_str[:-nb_of_dec] + '.' + amount_str[-nb_of_dec:]
    # translate the last char and set the sign
    credit_trans = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
                    'F': '6', 'G': '7', 'H': '8', 'I': '9', '{': '0'}
    debit_trans  = {'J': '1', 'K': '2', 'L': '3', 'M': '4', 'N': '5',
                    'O': '6', 'P': '7', 'Q': '8', 'R': '9', '}': '0'}
    if amount_str[-1] in debit_trans:
        amount_num = float('-' + amount_str.replace(amount_str[-1], debit_trans[amount_str[-1]]))
    elif amount_str[-1] in credit_trans:
        amount_num = float(amount_str.replace(amount_str[-1], credit_trans[amount_str[-1]]))
    else:
        raise Exception('Bad amount string')
    return amount_num



a = {}
cpt = 1
for line in listedelignes:
    
    if line[0:2] == '01': # lecture des 2 premiers charactères pour type ligne
        a[f"Compte Numéro ({cpt}) :"] = get_rib(line)
        a[f"Solde début ({cpt}) :"] = parse_amount(line,2)
        cpt+=1


    elif line[0:2] == '07': # lecture des 2 premiers charactères pour type ligne
        a[f"Solde fin ({(cpt-1)}) :"] = parse_amount(line,2)

    else:
        pass

# print des résultats
for cle,valeur in a.items():
    print(cle, valeur)