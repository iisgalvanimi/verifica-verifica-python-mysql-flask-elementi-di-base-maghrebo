#Importazioni delle diverse librerie
import mysql.connector
from flask import Flask, jsonify, request

#Connessione al database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="rettili"
)

#Creazione del cursore con cui operare nel database
mycursor = mydb.cursor()

#Creazioned dell'app flask per gestire le richieste HTTP
app = Flask(__name__)



#-----------------------------------------------------------------------------
#Definizione della funzione per il metodo GET

def getAllData():
    mycursor.execute("SELECT * FROM rettili")
    myresult = mycursor.fetchall()
    result = [];
    for x in myresult:
        print(x);
        result.append(x);
    return result


#Indirizzamento delle diverse route che poi richiamano le funzioni correlate
@app.route("/dati")
def stampaDati():
    data = getAllData()
    return jsonify({"La tabella rettili: ": data})


#Creazione della route principale vuota senza errore
@app.route("/")
def homeRoute():
    return "Buongiorno, questa è la route di default. Per avere la lista dei rettili, inserisci come route /dati"