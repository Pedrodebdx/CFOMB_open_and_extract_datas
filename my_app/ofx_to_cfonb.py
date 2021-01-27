from datetime import datetime
from cfonb_modifiee.writer.common import write, date_format, save, BR_LINE
from cfonb_modifiee.writer.statement import Statement
from ofxtools.Parser import OFXTree

############# Lire fichier OFX ########
def read_ofx(file):
   
    parser = OFXTree()



    ############# preprocessing des fichiers avec des changement de domiciliation #############
    with open(file, "r+") as f:
        d = f.readlines()
        indices = [i for i, x in enumerate(d) if x == "<TRNTYPE>null\n"] # récupération des indexs des lignes '<TRNTYPE>null', de changement de domiciliation, qui font buguer la librairie
        for position in reversed(indices): #pour commencer de la fin , sinon les indices ne sont plus bons
            del d[position+7]   #remove '</STMTTRN>'         
            del d[position+6]   #remove '<MEMO>...' 
            del d[position+5]   #remove '<NAME>...'   
            del d[position+4]   #remove '<FITID>.....'  
            del d[position+3]   #remove '<TRNAMT>.....'
            del d[position+2]   #remove '<DTUSER>.....'
            del d[position+1]   #remove '<DTPOSTED>.....'        
            del d[position]     #remove '<TRNTYPE>null'
            del d[position-1]   #remove '<STMTTRN>'

        f.seek(0)
        for i in d:
            f.write(i)
        f.truncate()

    ############# lecture du fichier ofx et extraction des infos #############
    with open(file, 'rb') as f:  # N.B. need to open file in binary mode
        t = parser.parse(f)

    

    ofx = parser.convert()

    stmts = ofx.statements  # statements
    stmts[0]

    acct = stmts[0].account   # The relevant ``*ACCTFROM
    acct
    acct.bankid


    txs = stmts[0].transactions
    return txs,acct,stmts

############# crédit ou débit ? ########
def debit_ou_credit(x):
    if x == "CREDIT":
        return '09'
    else:
        return '08'    

############# Ecriture du fichier CFONB depuis OFX via cfonb_modifiee ########
def write_cfonb_from_ofx(txs,acct,stmts):



    ###  écriture en 01(header)-> statement ###
    statement = Statement()

    statement.header(   acct.bankid,
                        acct.branchid,
                        stmts[0].curdef,
                        acct.acctid, 
                        stmts[0].banktranlist.dtstart , 
                        stmts[0].ledgerbal.balamt)


    ###  écriture en 04 et 05 ###
    for i in range(0,len(txs)): #len TXS pour le nbre de transactions
        print(txs[i])
        statement.add(  acct.bankid,                    #bank code
                        'RLV ',                         #operation_code
                        acct.branchid,                  #agency_code
                        stmts[0].curdef,                #currency
                        acct.acctid,                    #account_number
                        debit_ou_credit(txs[i].trntype),#interbank_code
                        stmts[0].banktranlist.dtstart,  #date
                        txs[i].name,                    #(label, 31)
                        txs[i].trnamt,                  # amount
                        txs[i].memo)                    # reference


        statement.addline05(    acct.bankid,                    #bank code
                                'RLV ',                         #operation_code
                                acct.branchid,                  #agency_code
                                stmts[0].curdef,                #currency
                                acct.acctid,                    #account_number
                                debit_ou_credit(txs[i].trntype),#interbank_code
                                stmts[0].banktranlist.dtstart,  #date
                                txs[i].memo)                    #comment


    ###  écriture en 07(footer) -> statement ###
    statement.footer(acct.bankid,acct.branchid,stmts[0].curdef,acct.acctid, stmts[0].banktranlist.dtend , stmts[0].availbal.balamt)

    # enregistrement du fichier
    statement.render(filename='./ofx-to-cfonb.cfonb')    
    
    
    
txs,acct,stmts = read_ofx(file = "./datas/3.ofx")

write_cfonb_from_ofx(txs,acct,stmts)


